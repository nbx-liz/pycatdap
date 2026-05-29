"""Multivariable error-slice discovery (H-0014 Phase L, PR-L3).

:func:`discover_error_slices` is the public entry point. It composes
existing pycatdap machinery rather than reinventing it:

- :func:`pycatdap.error.error_label` — the synthetic ``correct`` /
  ``incorrect`` response (classification only).
- :func:`pycatdap._pooling.optimal_binning` — AIC-optimal binning of
  continuous explanatory columns, with an **explicit bounded
  ``accuracy``** (HISTORY H-0013 §B-bis: ``accuracy=None`` lets the
  smallest-gap heuristic explode the initial grid on continuous axes).
- :func:`pycatdap.error._enumerate.enumerate_cells` — support-pruned
  (Apriori) cell enumeration.
- :mod:`pycatdap.measures` registry — the pluggable interestingness
  measure (FR-9). ``measure="aic"`` is scored via the registry too, but
  its sign is normalised (see below).
- :func:`pycatdap._aic.compute_delta_aic` — the ΔAIC stored on every
  slice for reference.

Measure directionality
----------------------
``measures.aic`` returns ΔAIC where *negative* = informative, whereas
``cramers_v`` / ``mutual_info`` are *higher* = stronger. To keep
``SliceDiscoveryResult.slices`` uniformly "sorted descending by
``measure_value``", the built-in name ``"aic"`` is normalised to
``-ΔAIC`` (higher = more informative). Custom callables and the other
registry measures are taken as-is (higher = better, documented).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._aic import compute_base_aic, compute_delta_aic
from pycatdap._contingency import build_multidim_crosstab
from pycatdap._pooling import optimal_binning
from pycatdap.error._describe import interval_label
from pycatdap.error._enumerate import enumerate_cells
from pycatdap.error._labels import _detect_task, abs_residual_pool, error_label
from pycatdap.error._slice import ErrorSlice, SliceDiscoveryResult
from pycatdap.measures import _registry

#: Numeric columns with more than this many distinct values are treated
#: as continuous and AIC-binned; at or below, they are used as discrete
#: categories directly.
_MAX_DISCRETE_CARD = 20

#: Initial-grid resolution for continuous binning — caps the initial bin
#: count so ``optimal_binning`` does not explode on fine-grained columns
#: (the §B-bis lesson, generalised from probabilities to any range).
_BIN_INIT_GRID = 50

#: The error category surfaced by :func:`error_label` (classification).
_ERROR_CATEGORY = "incorrect"

#: Binary residual-magnitude categories for the regression path (D1).
_HIGH_RESIDUAL = "high_residual"
_LOW_RESIDUAL = "low_residual"

#: Internal response column injected into the prepared frame for subset
#: ΔAIC scoring. Reserved — collides loudly if a user column shares it.
_RESPONSE_COL = "_error_label_"

MeasureArg = str | Callable[[npt.NDArray[np.float64]], float]


def _resolve_min_support(min_support: int | float, n_rows: int) -> int:
    """Convert a fractional ``min_support`` to an absolute row count."""
    if isinstance(min_support, float):
        if 0.0 < min_support <= 1.0:
            return max(1, int(round(min_support * n_rows)))
        # A float outside (0, 1] (e.g. 1.5) would otherwise truncate
        # silently to int — reject it so the caller's intent is explicit.
        msg = f"float min_support must be in (0, 1]; got {min_support!r}"
        raise ValueError(msg)
    value = int(min_support)
    if value < 1:
        msg = f"min_support must be >= 1 (got {min_support!r})"
        raise ValueError(msg)
    return value


def _prepare_frame(
    df: pd.DataFrame,
    columns: list[str],
    response: npt.NDArray[np.object_],
) -> pd.DataFrame:
    """Return a copy of ``df[columns]`` with continuous columns AIC-binned
    to interval-label strings. Input ``df`` is never mutated.

    Continuous columns are binned **against the error-label response** so
    AIC places cuts where the error rate shifts — coarse, well-populated,
    diagnostically meaningful bins (the pycatdap value proposition). A
    constant placeholder response would instead leave a fine initial grid
    of tiny, sub-support bins.
    """
    prepared = pd.DataFrame(index=df.index)
    for col in columns:
        series = df[col]
        if _is_continuous(series):
            prepared[col] = _bin_continuous(series, response)
        else:
            prepared[col] = series.astype("object")
    return prepared


def _is_continuous(series: pd.Series) -> bool:
    if not pd.api.types.is_numeric_dtype(series):
        return False
    return int(series.nunique(dropna=True)) > _MAX_DISCRETE_CARD


def _bin_continuous(
    series: pd.Series,
    response: npt.NDArray[np.object_],
) -> pd.Series:
    """AIC-bin a continuous column into interval-label strings.

    Uses an explicit bounded ``accuracy`` so the initial grid stays
    small (§B-bis); the error-label ``response`` then drives AIC merging
    down to bins that track error-rate shifts. Rows with NaN keep NaN
    (excluded from tabulation).
    """
    values = series.to_numpy(dtype=np.float64)
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return series.astype("object")
    vmin, vmax = float(finite.min()), float(finite.max())
    accuracy = (vmax - vmin) / _BIN_INIT_GRID if vmax > vmin else 1.0
    accuracy = max(accuracy, 1e-12)

    pooling = optimal_binning(values, response, accuracy=accuracy)
    boundaries = pooling.boundaries

    labels = np.empty(values.shape[0], dtype=object)
    codes = pooling.codes
    finite_mask = np.isfinite(values)
    labels[~finite_mask] = np.nan
    for i in np.nonzero(finite_mask)[0]:
        labels[i] = interval_label(int(codes[i]), boundaries)
    return pd.Series(labels, index=series.index, dtype="object")


def _top_residual_bin(
    resid_bins: npt.NDArray[np.object_],
    abs_resid: npt.NDArray[np.float64],
) -> Any:
    """Return the residual-bin label with the largest mean ``|residual|``.

    Determined dynamically rather than by assuming the AIC pooler numbered
    its bins in magnitude order, so the "worst predictions" pivot is correct
    regardless of bin-code ordering (INV-R9). Ties are broken by first-seen
    label (strict ``>`` comparison). Returns ``None`` only when every label is
    ``NaN`` — unreachable on the production path because
    :func:`_high_residual_labels` rejects non-finite inputs first.
    """
    best_label: Any = None
    best_mean = -np.inf
    for label in pd.unique(resid_bins):
        if pd.isna(label):
            continue
        mean_resid = float(abs_resid[resid_bins == label].mean())
        if mean_resid > best_mean:
            best_mean = mean_resid
            best_label = label
    return best_label


def _high_residual_labels(
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
    *,
    n_bins: int,
) -> pd.Series:
    """Binary high/low ``|residual|`` response for regression discovery (D1).

    Bins ``|y_true - y_pred|`` via AIC pooling (:func:`abs_residual_pool`)
    and marks the bin with the largest mean ``|residual|`` as
    ``"high_residual"``; every other row is ``"low_residual"``. This is the
    regression analogue of :func:`error_label`'s ``"incorrect"`` category and
    keeps the downstream 2-category contingency machinery unchanged.

    Raises
    ------
    ValueError
        If ``y_true`` or ``y_pred`` contains a non-finite value (NaN / Inf):
        the AIC residual pooler cannot bin missing residuals, and dropping
        rows here would break the length contract with ``df`` / ``error_mask``.
    """
    yt = np.asarray(y_true, dtype=np.float64)
    yp = np.asarray(y_pred, dtype=np.float64)
    if not bool(np.isfinite(yt).all()) or not bool(np.isfinite(yp).all()):
        msg = (
            "discover_error_slices: regression y_true/y_pred must be finite "
            "(no NaN/Inf). Drop or impute missing values before discovery."
        )
        raise ValueError(msg)
    resid_bins = abs_residual_pool(y_true, y_pred, n_bins=n_bins).to_numpy()
    abs_resid = np.abs(yt - yp)
    top = _top_residual_bin(resid_bins, abs_resid)
    is_high = resid_bins == top
    labels = np.where(is_high, _HIGH_RESIDUAL, _LOW_RESIDUAL)
    return pd.Series(
        pd.Categorical(labels, categories=[_LOW_RESIDUAL, _HIGH_RESIDUAL]),
        name="high_residual_label",
    )


def _normalised_measure(
    measure: MeasureArg,
) -> tuple[str, Callable[[npt.NDArray[np.float64]], float], bool]:
    """Resolve ``measure`` to ``(name, fn, negate)``.

    ``negate`` flips the sign so the returned ``measure_value`` is always
    "higher = more interesting" (only the built-in ``"aic"`` needs it).
    """
    if callable(measure):
        return ("<callable>", measure, False)
    fn = _registry.get(measure)
    return (measure, fn, measure == "aic")


def discover_error_slices(
    df: pd.DataFrame,
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
    *,
    max_vars: int = 3,
    measure: MeasureArg = "aic",
    top_k: int = 10,
    min_support: int | float = 30,
    columns: list[str] | None = None,
    n_bins: int = 4,
) -> SliceDiscoveryResult:
    """Discover multivariable subgroups where prediction errors concentrate.

    Works for both tasks (auto-detected via :func:`_detect_task`):

    - **Classification**: errors are :func:`error_label` (``y_true != y_pred``);
      the error category is ``"incorrect"``.
    - **Regression**: ``|y_true - y_pred|`` is AIC-binned via
      :func:`abs_residual_pool` and the largest-residual bin becomes a binary
      ``"high_residual"`` error category (design D1, H-0015 §B). The downstream
      2-category contingency / measure / support-pruning machinery is shared.

    Continuous explanatory columns are AIC-binned. The search is support-pruned
    (Apriori) — see HISTORY H-0014 §C for why pruning is on support, not ΔAIC.

    Parameters
    ----------
    df : DataFrame
        Explanatory variables. Not mutated.
    y_true, y_pred : array-like
        Aligned ground-truth and predicted values (length ``len(df)``).
    max_vars : int, default 3
        Maximum number of conditions combined per slice.
    measure : {"aic", "cramers_v", "mutual_info"} or callable, default "aic"
        Interestingness measure scoring each variable subset's
        association with the error label. A callable takes a 2D
        contingency table and returns a float (higher = more
        interesting). Custom measures may be registered via
        :func:`pycatdap.measures.register`.
    top_k : int, default 10
        Number of top slices to return.
    min_support : int or float, default 30
        Minimum slice size. A float in ``(0, 1]`` is read as a fraction
        of ``len(df)``.
    columns : list[str] or None
        Explanatory columns to search. ``None`` uses every column of
        ``df``.
    n_bins : int, default 4
        Regression only: initial bin count for AIC-pooling ``|residual|``
        into the high/low-residual response. Ignored for classification.

    Returns
    -------
    SliceDiscoveryResult
        Top-``k`` :class:`ErrorSlice` objects (sorted descending by
        ``measure_value``) plus search metadata.

    Raises
    ------
    ValueError
        On length mismatch or invalid ``min_support``.
    """
    task = _detect_task(np.asarray(y_true), np.asarray(y_pred))

    cols = list(df.columns) if columns is None else list(columns)
    if _RESPONSE_COL in cols:
        msg = f"column name {_RESPONSE_COL!r} is reserved by discover_error_slices"
        raise ValueError(msg)
    n_rows = len(df)
    support_floor = _resolve_min_support(min_support, n_rows)
    name, measure_fn, negate = _normalised_measure(measure)

    if task == "regression":
        labels = _high_residual_labels(y_true, y_pred, n_bins=n_bins)
        error_category = _HIGH_RESIDUAL
        label_kind = "abs_residual_pool"
    else:
        labels = error_label(y_true, y_pred)
        error_category = _ERROR_CATEGORY
        label_kind = "error_label"

    if len(labels) != n_rows:
        msg = f"y_true/y_pred length ({len(labels)}) must equal len(df) ({n_rows})"
        raise ValueError(msg)
    error_mask = (labels.to_numpy() == error_category).astype(np.bool_)
    base_error_rate = float(error_mask.mean()) if n_rows else 0.0

    response = labels.to_numpy().astype(object)
    prepared = _prepare_frame(df, cols, response)
    # base AIC of the null model (error label with no explanatory variable).
    base_aic = _null_aic(error_mask, n_rows)

    cells, n_evaluated, n_pruned = enumerate_cells(
        prepared,
        cols,
        error_mask,
        max_vars=max_vars,
        min_support=support_floor,
        prune=True,
    )

    prepared_with_error = prepared.copy()
    prepared_with_error[_RESPONSE_COL] = labels.to_numpy()

    subset_cache: dict[tuple[str, ...], tuple[float, float]] = {}
    slices: list[ErrorSlice] = []
    for cell in cells:
        if cell.size == 0:
            continue
        error_metric = cell.n_error / cell.size
        # Only error-concentrated cells are "interesting".
        if error_metric <= base_error_rate:
            continue
        subset = tuple(col for col, _ in cell.conditions)
        if subset not in subset_cache:
            subset_cache[subset] = _score_subset(
                prepared_with_error, _RESPONSE_COL, list(subset), measure_fn, negate
            )
        delta_aic, measure_value = subset_cache[subset]
        slices.append(
            ErrorSlice.from_conditions(
                cell.conditions,
                size=cell.size,
                error_metric=error_metric,
                delta_aic=delta_aic,
                measure_value=measure_value,
                n_error_in_slice=cell.n_error,
            )
        )

    slices.sort(
        key=lambda s: (s.measure_value, s.error_metric, s.size),
        reverse=True,
    )
    top = tuple(slices[:top_k])

    return SliceDiscoveryResult(
        slices=top,
        measure=name,
        max_vars=max_vars,
        base_aic=base_aic,
        n_evaluated=n_evaluated,
        n_pruned=n_pruned,
        label_kind=label_kind,
    )


def _null_aic(error_mask: npt.NDArray[np.bool_], n_rows: int) -> float:
    """AIC of the error-label null model (no explanatory variable)."""
    if n_rows == 0:
        return 0.0
    n_err = int(error_mask.sum())
    marginal_e = np.array([n_rows - n_err, n_err], dtype=np.float64)
    marginal_e = marginal_e[marginal_e > 0]
    return compute_base_aic(marginal_e, n_rows)


def _score_subset(
    frame: pd.DataFrame,
    response: str,
    subset: list[str],
    measure_fn: Callable[[npt.NDArray[np.float64]], float],
    negate: bool,
) -> tuple[float, float]:
    """Return ``(delta_aic, measure_value)`` for a variable subset.

    ``delta_aic`` is always the raw subset ΔAIC; ``measure_value`` is the
    chosen measure (sign-normalised so higher = more interesting).
    """
    cross, marg_e, marg_f, n = build_multidim_crosstab(frame, response, subset)
    delta_aic = compute_delta_aic(cross, marg_e, marg_f, n)
    raw = measure_fn(cross)
    measure_value = -raw if negate else raw
    return delta_aic, measure_value
