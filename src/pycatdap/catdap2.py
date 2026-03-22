"""CATDAP-02: Optimal explanatory variable subset search.

Finds the best subset of explanatory variables for a response variable,
with support for continuous variable binning (pooling).
"""

from __future__ import annotations

import types
from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from pycatdap._aic import compute_base_aic
from pycatdap._contingency import build_crosstab
from pycatdap._pooling import PoolingResult, optimal_binning
from pycatdap._subset_search import SubsetResult, search_best_subset


@dataclass(frozen=True)
class Catdap2Result:
    """Result container for :func:`catdap2`.

    Attributes
    ----------
    base_aic : float
        AIC of the null model (no explanatory variables).
    aic : pd.DataFrame
        Single-variable ΔAIC values with columns ``['variable', 'aic']``.
    aic_order : list[str]
        Variables sorted by ΔAIC ascending (best first).
    subsets : list[SubsetResult]
        Best variable subsets grouped by size.
    intervals : Mapping[str, list[float]]
        Pooling boundaries for continuous variables.  Empty for
        categorical-only analyses.
    tway_tables : Mapping[str, pd.DataFrame]
        Two-way tables for each single explanatory variable.
    """

    base_aic: float
    aic: pd.DataFrame = field(repr=False)
    aic_order: list[str] = field(repr=False)
    subsets: list[SubsetResult] = field(repr=False)
    intervals: Mapping[str, list[float]] = field(repr=False)
    tway_tables: Mapping[str, pd.DataFrame] = field(repr=False)

    def __repr__(self) -> str:
        n_vars = len(self.aic)
        n_subsets = len(self.subsets)
        return (
            f"Catdap2Result(base_aic={self.base_aic:.2f}, "
            f"variables={n_vars}, subsets={n_subsets})"
        )


def _validate_catdap2_input(
    data: pd.DataFrame,
    pool: list[int],
    response_name: str,
) -> None:
    """Validate catdap2 inputs.

    Raises
    ------
    ValueError
        If inputs are invalid.
    """
    if data.empty:
        msg = "data must not be empty"
        raise ValueError(msg)

    if response_name not in data.columns:
        msg = f"response_name '{response_name}' not found in data columns"
        raise ValueError(msg)

    if len(pool) != len(data.columns):
        msg = (
            f"pool length ({len(pool)}) must match number of columns "
            f"({len(data.columns)})"
        )
        raise ValueError(msg)


def _prepare_data(
    data: pd.DataFrame,
    pool: list[int],
    response_name: str,
    accuracy: list[float] | None,
) -> tuple[pd.DataFrame, dict[str, list[float]]]:
    """Apply pooling to continuous variables.

    Returns
    -------
    prepared : DataFrame
        Fully categorical DataFrame.
    intervals : dict
        Pooling boundaries keyed by variable name.
    """
    columns = list(data.columns)
    intervals: dict[str, list[float]] = {}
    prepared = data.copy()

    for i, col in enumerate(columns):
        if col == response_name:
            continue

        pool_val = pool[i]

        if pool_val == 2:
            # Already categorical — no pooling
            continue

        # Continuous variable — apply pooling
        values = data[col].to_numpy(dtype=np.float64)
        response_vals = data[response_name].to_numpy()

        acc = accuracy[i] if accuracy is not None else None
        method = "top_down" if pool_val == 0 else "bottom_up"

        result: PoolingResult = optimal_binning(
            values, response_vals, method=method, accuracy=acc
        )
        intervals[col] = result.boundaries
        prepared[col] = result.codes

    return prepared, intervals


def catdap2(
    data: pd.DataFrame,
    pool: list[int] | None = None,
    response_name: str | None = None,
    accuracy: list[float] | None = None,
    nvar: int | None = None,
) -> Catdap2Result:
    """Search for optimal explanatory variable subsets using AIC.

    Parameters
    ----------
    data : DataFrame
        Input data with categorical and/or continuous variables.
        Not modified.
    pool : list[int] or None
        Pooling method per column:
        ``0`` = equal pooling, ``1`` = unequal pooling (default),
        ``2`` = categorical (no pooling).
        If ``None``, all columns treated as categorical.
    response_name : str or None
        Response variable column name.  If ``None``, uses the first column.
    accuracy : list[float] or None
        Minimum bin width per column for pooling.
        If ``None``, auto-detected.
    nvar : int or None
        Number of top variables to retain for multi-variable search.

    Returns
    -------
    Catdap2Result

    Raises
    ------
    ValueError
        If inputs are invalid.
    """
    if response_name is None:
        if data.empty:
            msg = "data must not be empty"
            raise ValueError(msg)
        response_name = str(data.columns[0])

    if pool is None:
        pool = [2] * len(data.columns)

    _validate_catdap2_input(data, pool, response_name)

    # Prepare data (apply pooling)
    prepared, intervals = _prepare_data(data, pool, response_name, accuracy)

    # Compute base AIC
    resp_col = prepared[response_name]
    marg_e = resp_col.value_counts().to_numpy(dtype=np.float64)
    n_total = len(resp_col)
    base_aic = compute_base_aic(marg_e, n_total)

    # Identify explanatory variables
    expl_cols = [c for c in prepared.columns if c != response_name]

    # Single-variable AIC
    aic_records: list[dict[str, object]] = []
    tway_tables: dict[str, pd.DataFrame] = {}

    for col in expl_cols:
        cross, me, mf, n = build_crosstab(prepared, response_name, col)
        from pycatdap._aic import compute_delta_aic

        delta = compute_delta_aic(cross, me, mf, n)
        aic_records.append({"variable": col, "aic": delta})

        subset = prepared[[response_name, col]].dropna()
        tway_tables[col] = pd.crosstab(subset[response_name], subset[col])

    aic_df = pd.DataFrame(aic_records)
    if not aic_df.empty:
        aic_df = aic_df.sort_values("aic").reset_index(drop=True)

    aic_order = list(aic_df["variable"]) if not aic_df.empty else []

    # Subset search
    subsets = search_best_subset(prepared, response_name, expl_cols, nvar=nvar)

    return Catdap2Result(
        base_aic=base_aic,
        aic=aic_df.copy(),
        aic_order=aic_order,
        subsets=subsets,
        intervals=types.MappingProxyType(intervals),
        tway_tables=types.MappingProxyType(tway_tables),
    )
