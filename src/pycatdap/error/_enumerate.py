"""Combinatorial slice enumeration with sound support pruning
(H-0014 Phase L, PR-L3).

The discovery engine surfaces multivariable *cells* — conjunctions of
``(column, value)`` conditions — where prediction errors concentrate.
Enumerating every conjunction up to ``max_vars`` is exponential, so we
prune.

Pruning is on **support (cell size)**, NOT ΔAIC. Support is
anti-monotone (Apriori): a cell's size is ``<=`` the size of every
sub-cell, so once a conjunction drops below ``min_support`` no extension
of it can recover — the whole branch is cut soundly. ΔAIC has no such
bound (the ``2*(C_E-1)*C_F`` model-complexity penalty in
:func:`pycatdap._aic.compute_aic_twoway` grows with composite
cardinality), so ΔAIC-based pruning could drop true top-k slices. See
HISTORY H-0014 §C.

Two entry points share one code path via the ``prune`` flag:

- :func:`enumerate_cells` with ``prune=False`` — exhaustive baseline
  (the correctness oracle: every conjunction, with its support).
- :func:`enumerate_cells` with ``prune=True`` — Apriori, returning only
  cells whose support ``>= min_support``.

The invariant tying them together (asserted in the test-suite RED
phase)::

    {c.conditions for c in pruned}
        == {c.conditions for c in exhaustive if c.size >= min_support}
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import pandas as pd

#: A single ``(column, value)`` condition.
Condition = tuple[str, str]


@dataclass(frozen=True)
class CellStat:
    """Support statistics for one discovered cell (conjunction).

    Attributes
    ----------
    conditions : tuple[Condition, ...]
        The AND-ed ``(column, value)`` conditions, sorted by column for
        a canonical identity (so set comparison in the equivalence test
        is order-independent).
    size : int
        Rows matching all conditions (support).
    n_error : int
        Of those, how many fall under the error category.
    """

    conditions: tuple[Condition, ...]
    size: int
    n_error: int


def _condition_masks(
    frame: pd.DataFrame,
    columns: list[str],
) -> dict[str, list[tuple[Condition, npt.NDArray[np.bool_]]]]:
    """Build per-column boolean masks for every observed value.

    Rows with ``NaN`` in a column simply match none of that column's
    values (consistent with the drop-NaN tabulation in
    :mod:`pycatdap._contingency`).
    """
    by_col: dict[str, list[tuple[Condition, npt.NDArray[np.bool_]]]] = {}
    for col in columns:
        series = frame[col]
        values = pd.unique(series.dropna())
        col_masks: list[tuple[Condition, npt.NDArray[np.bool_]]] = []
        arr = series.to_numpy()
        for val in values:
            mask = arr == val
            col_masks.append(((col, str(val)), np.asarray(mask, dtype=np.bool_)))
        by_col[col] = col_masks
    return by_col


def _total_candidates(card_by_col: dict[str, int], max_vars: int) -> int:
    """Count every possible cell up to ``max_vars`` distinct columns.

    Used to report the search-space size so the pruned run can express
    ``n_pruned = total - n_evaluated`` (the >50%-reduction acceptance
    metric) without running the exhaustive path.
    """
    cols = list(card_by_col)
    total = 0
    for k in range(1, min(max_vars, len(cols)) + 1):
        for combo in itertools.combinations(cols, k):
            prod = 1
            for c in combo:
                prod *= card_by_col[c]
            total += prod
    return total


def _stat(
    conditions: tuple[Condition, ...],
    mask: npt.NDArray[np.bool_],
    error_mask: npt.NDArray[np.bool_],
) -> CellStat:
    size = int(np.count_nonzero(mask))
    n_error = int(np.count_nonzero(mask & error_mask))
    return CellStat(conditions=conditions, size=size, n_error=n_error)


def enumerate_cells(
    frame: pd.DataFrame,
    columns: list[str],
    error_mask: npt.NDArray[np.bool_],
    *,
    max_vars: int,
    min_support: int,
    prune: bool = True,
    max_candidates: int | None = None,
) -> tuple[list[CellStat], int, int, bool]:
    """Enumerate cells up to ``max_vars`` conditions.

    Parameters
    ----------
    frame : DataFrame
        Prepared frame whose explanatory columns are already categorical
        (continuous columns pre-binned to interval labels). Not mutated.
    columns : list[str]
        Explanatory columns to combine.
    error_mask : ndarray of bool
        Row mask flagging the error category (e.g. ``error_label ==
        "incorrect"``). Length must equal ``len(frame)``.
    max_vars : int
        Maximum number of conditions per cell.
    min_support : int
        Minimum cell size to be retained (``prune=True``) or the
        threshold against which the exhaustive output is later filtered.
    prune : bool, default True
        ``True`` runs Apriori (returns only frequent cells);
        ``False`` returns every cell with its support (the oracle).
    max_candidates : int or None, default None
        Cap on the number of candidate cells evaluated (Apriori path only).
        When reached, the search stops early and ``truncated`` is ``True``.
        ``None`` means unbounded. Ignored for ``prune=False``.

    Returns
    -------
    cells : list[CellStat]
        ``prune=True`` -> only cells with ``size >= min_support``.
        ``prune=False`` -> every cell.
    n_evaluated : int
        Number of candidate cells whose support was computed.
    n_pruned : int
        ``prune=True`` -> ``total_candidates - n_evaluated``; counts both
        branches Apriori never generated *and* candidates that were
        evaluated but fell below ``min_support`` (i.e. every cell whose
        support was not computed because a parent was infrequent).
        ``prune=False`` -> ``0``.
    truncated : bool
        ``True`` if the Apriori search hit ``max_candidates`` and stopped
        early (a sound subset, not exhaustive). Always ``False`` for the
        exhaustive path.
    """
    by_col = _condition_masks(frame, columns)
    card_by_col = {col: len(by_col[col]) for col in columns}
    eff_max = min(max_vars, len(columns))

    if not prune:
        return _enumerate_exhaustive(by_col, error_mask, eff_max)

    return _enumerate_apriori(
        by_col, card_by_col, error_mask, eff_max, min_support, max_candidates
    )


def _enumerate_exhaustive(
    by_col: dict[str, list[tuple[Condition, npt.NDArray[np.bool_]]]],
    error_mask: npt.NDArray[np.bool_],
    eff_max: int,
) -> tuple[list[CellStat], int, int, bool]:
    """Every conjunction across distinct columns, each with its support."""
    cells: list[CellStat] = []
    cols = list(by_col)
    for k in range(1, eff_max + 1):
        for combo in itertools.combinations(cols, k):
            choices = [by_col[c] for c in combo]
            for picks in itertools.product(*choices):
                conditions = tuple(sorted((cond for cond, _ in picks)))
                mask = picks[0][1].copy()
                for _, m in picks[1:]:
                    mask &= m
                cells.append(_stat(conditions, mask, error_mask))
    return cells, len(cells), 0, False


def _enumerate_apriori(
    by_col: dict[str, list[tuple[Condition, npt.NDArray[np.bool_]]]],
    card_by_col: dict[str, int],
    error_mask: npt.NDArray[np.bool_],
    eff_max: int,
    min_support: int,
    max_candidates: int | None = None,
) -> tuple[list[CellStat], int, int, bool]:
    """Apriori: only extend cells that are themselves frequent.

    A candidate ``k``-cell is generated only when all of its
    ``(k-1)``-sub-cells are frequent — the classic anti-monotone prune.
    """
    mask_of: dict[Condition, npt.NDArray[np.bool_]] = {}
    for col_masks in by_col.values():
        for cond, m in col_masks:
            mask_of[cond] = m

    all_frequent: list[CellStat] = []
    n_evaluated = 0
    truncated = False

    # Level 1.
    prev_level: list[tuple[Condition, ...]] = []
    for col_masks in by_col.values():
        for cond, m in col_masks:
            if max_candidates is not None and n_evaluated >= max_candidates:
                truncated = True
                break
            n_evaluated += 1
            stat = _stat((cond,), m, error_mask)
            if stat.size >= min_support:
                all_frequent.append(stat)
                prev_level.append((cond,))
        if truncated:
            break

    frequent_set = set(prev_level)

    # Levels 2..eff_max via candidate generation from frequent (k-1)-cells.
    for _k in range(2, eff_max + 1):
        if truncated:
            break
        if max_candidates is not None and n_evaluated >= max_candidates:
            truncated = True
            break
        remaining = None if max_candidates is None else max_candidates - n_evaluated
        candidates = _generate_candidates(prev_level, frequent_set, limit=remaining)
        next_level: list[tuple[Condition, ...]] = []
        for conditions in candidates:
            if max_candidates is not None and n_evaluated >= max_candidates:
                truncated = True
                break
            n_evaluated += 1
            mask = mask_of[conditions[0]].copy()
            for cond in conditions[1:]:
                mask &= mask_of[cond]
            stat = _stat(conditions, mask, error_mask)
            if stat.size >= min_support:
                all_frequent.append(stat)
                next_level.append(conditions)
        if not next_level:
            break
        prev_level = next_level
        frequent_set = set(prev_level)

    total = _total_candidates(card_by_col, eff_max)
    n_pruned = total - n_evaluated
    return all_frequent, n_evaluated, n_pruned, truncated


def _generate_candidates(
    prev_level: list[tuple[Condition, ...]],
    frequent_set: set[tuple[Condition, ...]],
    *,
    limit: int | None = None,
) -> list[tuple[Condition, ...]]:
    """Join frequent ``(k-1)``-cells into ``k``-cell candidates.

    Two ``(k-1)``-cells join when they share their first ``k-2``
    conditions and differ in the last (canonical-order join). A
    candidate survives only if every one of its ``(k-1)``-subsets is
    frequent (Apriori pruning).

    ``limit`` caps the number of candidates produced, stopping the
    ``O(N^2)`` join early so a huge frequent set cannot explode memory /
    time (H-0016). ``None`` means unbounded.
    """
    candidates: list[tuple[Condition, ...]] = []
    seen: set[tuple[Condition, ...]] = set()
    n = len(prev_level)
    for i in range(n):
        if limit is not None and len(candidates) >= limit:
            break
        for j in range(i + 1, n):
            if limit is not None and len(candidates) >= limit:
                break
            a, b = prev_level[i], prev_level[j]
            if a[:-1] != b[:-1]:
                continue
            # Different columns only (same column → empty intersection).
            if a[-1][0] == b[-1][0]:
                continue
            merged = tuple(sorted({*a, *b}))
            if len(merged) != len(a) + 1 or merged in seen:
                continue
            # Apriori: all (k-1)-subsets must be frequent.
            if all(
                tuple(sub) in frequent_set
                for sub in itertools.combinations(merged, len(merged) - 1)
            ):
                seen.add(merged)
                candidates.append(merged)
    return candidates
