"""CATDAP-01: Pairwise AIC evaluation of categorical variable associations.

Evaluates every pair of categorical variables in a DataFrame using AIC,
ranking explanatory variables by their informativeness for each response.
"""

from __future__ import annotations

import types
from collections.abc import Mapping
from dataclasses import dataclass, field

import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap._contingency import build_crosstab


@dataclass(frozen=True)
class Catdap1Result:
    """Result container for :func:`catdap1`.

    Attributes
    ----------
    tway_tables : Mapping[tuple[str, str], pd.DataFrame]
        Two-way frequency tables keyed by ``(response, explanatory)``.
        These tables reflect NaN-dropped data (consistent with AIC).
    aic : pd.DataFrame
        ΔAIC values.  Rows are response variables, columns are all
        variables in the original column order.  Self-entries are ``NaN``.
    aic_order : Mapping[str, list[str]]
        For each response variable, explanatory variables sorted by ΔAIC
        ascending (best first).  Read-only mapping.
    total : pd.Series
        Per-column non-null count from the input data.  Note: pairwise
        observation counts used in AIC may differ when NaN values exist.
    """

    tway_tables: Mapping[tuple[str, str], pd.DataFrame] = field(repr=False)
    aic: pd.DataFrame = field(repr=False)
    aic_order: Mapping[str, list[str]] = field(repr=False)
    total: pd.Series = field(repr=False)

    def __repr__(self) -> str:
        n_resp = len(self.aic.index)
        n_vars = len({*self.aic.index.tolist(), *self.aic.columns.tolist()})
        return f"Catdap1Result(responses={n_resp}, variables={n_vars})"


def _validate_input(
    data: pd.DataFrame,
    response_names: list[str] | None,
) -> list[str]:
    """Validate inputs and return resolved response names.

    Raises
    ------
    ValueError
        If the DataFrame is empty, has fewer than 2 columns,
        or a requested response name is not found.
    """
    if data.empty:
        msg = "data must not be empty"
        raise ValueError(msg)

    if len(data.columns) < 2:
        msg = "data must have at least 2 columns"
        raise ValueError(msg)

    if response_names is None:
        return list(data.columns)

    for name in response_names:
        if name not in data.columns:
            msg = f"response variable '{name}' not found in data columns"
            raise ValueError(msg)

    return list(response_names)


def catdap1(
    data: pd.DataFrame,
    response_names: list[str] | None = None,
) -> Catdap1Result:
    """Evaluate pairwise associations between categorical variables using AIC.

    For each response variable, computes ΔAIC for every other variable
    as explanatory, then ranks them by informativeness.

    Parameters
    ----------
    data : DataFrame
        DataFrame of categorical variables.  Not modified.
    response_names : list[str] or None
        Column names to use as response variables.  If ``None``, all
        columns are used as response variables in turn.

    Returns
    -------
    Catdap1Result
        Container with two-way tables, AIC values, rankings, and totals.

    Raises
    ------
    ValueError
        If *data* is empty, has fewer than 2 columns, or a response
        name is missing.
    """
    responses = _validate_input(data, response_names)
    all_cols = list(data.columns)

    tway_tables: dict[tuple[str, str], pd.DataFrame] = {}
    aic_records: dict[str, dict[str, float]] = {}
    aic_order: dict[str, list[str]] = {}

    for resp in responses:
        explanatory_cols = [c for c in all_cols if c != resp]
        row: dict[str, float] = {}

        for expl in explanatory_cols:
            cross, marg_e, marg_f, n = build_crosstab(data, resp, expl)
            delta = compute_delta_aic(cross, marg_e, marg_f, n)
            row[expl] = delta

            # Store NaN-dropped crosstab consistent with AIC computation
            subset = data[[resp, expl]].dropna()
            tway_tables[(resp, expl)] = pd.crosstab(subset[resp], subset[expl])

        aic_records[resp] = row
        aic_order[resp] = sorted(row, key=lambda col: row[col])

    aic_df = pd.DataFrame.from_dict(aic_records, orient="index")
    aic_df = aic_df.reindex(columns=all_cols)
    aic_df.index.name = "response"

    total = data.count()

    return Catdap1Result(
        tway_tables=types.MappingProxyType(tway_tables),
        aic=aic_df.copy(),
        aic_order=types.MappingProxyType(aic_order),
        total=total.copy(),
    )
