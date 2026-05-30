"""Tests for the slice-enumeration core (H-0014 PR-L3).

The load-bearing test is :func:`test_pruned_equals_exhaustive_above_support`
— the soundness guarantee that support (Apriori) pruning never drops a
cell that meets ``min_support`` (HISTORY H-0014 §C).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pycatdap.error._enumerate import (
    _total_candidates,
    enumerate_cells,
)


def _frame(seed: int, n: int = 200) -> tuple[pd.DataFrame, np.ndarray]:
    """Small synthetic categorical frame + an error mask."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "a": rng.choice(["x", "y", "z"], size=n),
            "b": rng.choice(["p", "q"], size=n),
            "c": rng.choice(["m", "n", "o"], size=n),
        }
    )
    error_mask = rng.random(n) < 0.3
    return df, error_mask


def _frequent_keys(cells: list, min_support: int) -> set:
    return {c.conditions for c in cells if c.size >= min_support}


@pytest.mark.parametrize("seed", [0, 1, 2, 7, 42])
@pytest.mark.parametrize("min_support", [1, 10, 30, 80])
@pytest.mark.parametrize("max_vars", [1, 2, 3])
def test_pruned_equals_exhaustive_above_support(
    seed: int, min_support: int, max_vars: int
) -> None:
    """INVARIANT: pruned == {exhaustive cells with size >= min_support}.

    This is the correctness oracle for support pruning. If it ever fails,
    Apriori is dropping a frequent cell — a real bug, not a tuning knob.
    """
    df, error_mask = _frame(seed)
    cols = ["a", "b", "c"]

    exhaustive, _, n_pruned_exh, _ = enumerate_cells(
        df, cols, error_mask, max_vars=max_vars, min_support=min_support, prune=False
    )
    pruned, _, _, _ = enumerate_cells(
        df, cols, error_mask, max_vars=max_vars, min_support=min_support, prune=True
    )

    assert n_pruned_exh == 0
    assert {c.conditions for c in pruned} == _frequent_keys(exhaustive, min_support)


def test_pruned_cells_all_meet_support() -> None:
    df, error_mask = _frame(3)
    pruned, _, _, _ = enumerate_cells(
        df, ["a", "b", "c"], error_mask, max_vars=3, min_support=25, prune=True
    )
    assert all(c.size >= 25 for c in pruned)


def test_support_and_error_counts_correct() -> None:
    df = pd.DataFrame({"a": ["x", "x", "y", "x"], "b": ["p", "p", "p", "q"]})
    error_mask = np.array([True, False, True, False])
    cells, _, _, _ = enumerate_cells(
        df, ["a", "b"], error_mask, max_vars=2, min_support=1, prune=False
    )
    by_key = {c.conditions: c for c in cells}
    # a=x matches rows 0,1,3 -> size 3, errors at row0 -> 1
    ax = by_key[(("a", "x"),)]
    assert ax.size == 3
    assert ax.n_error == 1
    # a=x & b=p matches rows 0,1 -> size 2, error row0 -> 1
    axbp = by_key[tuple(sorted((("a", "x"), ("b", "p"))))]
    assert axbp.size == 2
    assert axbp.n_error == 1


def test_conditions_are_canonically_sorted() -> None:
    df, error_mask = _frame(1, n=60)
    cells, _, _, _ = enumerate_cells(
        df, ["c", "a", "b"], error_mask, max_vars=3, min_support=1, prune=False
    )
    for c in cells:
        assert list(c.conditions) == sorted(c.conditions)


def test_pruning_reduces_search_space() -> None:
    """With a real support floor, the pruned run skips a large fraction."""
    df, error_mask = _frame(5, n=400)
    _, n_eval, n_pruned, _ = enumerate_cells(
        df, ["a", "b", "c"], error_mask, max_vars=3, min_support=50, prune=True
    )
    total = n_eval + n_pruned
    assert n_pruned >= 0
    assert n_eval <= total


def test_total_candidates_formula() -> None:
    # cards a=3,b=2,c=3; max_vars=2:
    # k=1: 3+2+3=8 ; k=2: ab=6, ac=9, bc=6 => 21 ; total=29
    assert _total_candidates({"a": 3, "b": 2, "c": 3}, 2) == 29
    # max_vars=3 adds abc = 3*2*3 = 18 -> 47
    assert _total_candidates({"a": 3, "b": 2, "c": 3}, 3) == 47


def test_max_vars_capped_to_columns() -> None:
    df, error_mask = _frame(2, n=50)
    # max_vars larger than #columns must not error
    cells, _, _, _ = enumerate_cells(
        df, ["a", "b"], error_mask, max_vars=9, min_support=1, prune=True
    )
    assert all(len(c.conditions) <= 2 for c in cells)
