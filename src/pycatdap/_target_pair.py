"""Target × explanatory pair analysis (H-0004).

Provides :func:`target_summary` for cross-tabulation with proportions,
Pearson standardized residuals, and ΔAIC of a single (target, explanatory)
pair. Implements the :class:`TargetSummary` dataclass with rich display
methods (``show``, ``to_html``, ``to_dict``, ``to_plotly_json``).

The companion visualization function :func:`pycatdap.plot_target` lives in
:mod:`pycatdap.plot` so it can dispatch on backend.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap._pooling import optimal_binning
from pycatdap.eda import _detect_kind


@dataclass(frozen=True)
class TargetSummary:
    """Result of :func:`target_summary`.

    Attributes
    ----------
    target : str
        Target (response) variable column name.
    explanatory : str
        Explanatory variable column name.
    counts : pd.DataFrame
        Cross-frequency table. Rows are target categories, columns are
        explanatory categories (or bins for a binned continuous variable).
    row_prop : pd.DataFrame
        Row-normalized proportions; each row sums to 1.
    col_prop : pd.DataFrame
        Column-normalized proportions; each column sums to 1.
    expected : pd.DataFrame
        Expected counts under the independence assumption.
    pearson_residuals : pd.DataFrame
        ``(observed - expected) / sqrt(expected)``; values with
        ``|residual| > 2`` indicate a strong association in that cell.
    delta_aic : float
        ΔAIC of the (target, explanatory) pair, identical to the value
        returned by :func:`pycatdap.catdap1`.
    intervals : list[float] or None
        For a binned continuous explanatory, the sorted interior bin
        boundaries. ``None`` when the explanatory is categorical.
    """

    target: str
    explanatory: str
    counts: pd.DataFrame = field(repr=False)
    row_prop: pd.DataFrame = field(repr=False)
    col_prop: pd.DataFrame = field(repr=False)
    expected: pd.DataFrame = field(repr=False)
    pearson_residuals: pd.DataFrame = field(repr=False)
    delta_aic: float
    intervals: list[float] | None = field(repr=False)

    def __repr__(self) -> str:
        return (
            f"TargetSummary(target={self.target!r}, "
            f"explanatory={self.explanatory!r}, "
            f"delta_aic={self.delta_aic:.4f})"
        )

    def show(self) -> None:
        """Display the four tables inline in a Jupyter notebook.

        Falls back to ``print`` outside Jupyter.
        """
        tables: list[tuple[str, pd.DataFrame]] = [
            ("counts", self.counts),
            ("row_prop", self.row_prop.round(3)),
            ("col_prop", self.col_prop.round(3)),
            ("pearson_residuals", self.pearson_residuals.round(2)),
        ]
        try:
            from IPython.display import display
        except ImportError:
            print(
                f"TargetSummary: target={self.target}, explanatory={self.explanatory}"
            )
            print(f"delta_aic = {self.delta_aic:.4f}")
            for name, df in tables:
                print(f"\n--- {name} ---")
                print(df)
            return
        display(f"TargetSummary: {self.target} × {self.explanatory}")
        display(f"ΔAIC = {self.delta_aic:.4f}")
        for name, df in tables:
            display(name)
            display(df)

    def to_html(self, path: str | Path | None = None) -> str:
        """Render the summary as a standalone HTML string.

        Parameters
        ----------
        path : str, Path, or None
            If provided, the HTML is also written to this file.

        Returns
        -------
        str
            HTML document containing the four tables stacked vertically.
        """
        title = f"target_summary: {self.target} × {self.explanatory}"
        head = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>"
            "body{font-family:system-ui,sans-serif;margin:24px;}"
            "h1{font-size:1.2em;margin-bottom:0.3em;}"
            "h2{font-size:1em;margin-top:1.5em;color:#444;}"
            ".meta{color:#666;margin-bottom:1em;}"
            "table{border-collapse:collapse;font-size:0.9em;margin-bottom:0.5em;}"
            "th,td{border:1px solid #ddd;padding:4px 8px;text-align:right;}"
            "th{background:#f5f5f5;text-align:left;}"
            "td:first-child,th:first-child{text-align:left;}"
            "</style></head><body>"
        )
        sections = [
            ("Counts", self.counts),
            ("Row proportions", self.row_prop.round(3)),
            ("Column proportions", self.col_prop.round(3)),
            ("Pearson residuals", self.pearson_residuals.round(2)),
        ]
        body_parts = [
            f"<h1>{title}</h1>",
            f"<div class='meta'>ΔAIC = {self.delta_aic:.4f}</div>",
        ]
        if self.intervals is not None:
            cuts = ", ".join(f"{c:.3f}" for c in self.intervals)
            body_parts.append(f"<div class='meta'>bin boundaries: [{cuts}]</div>")
        for label, df in sections:
            body_parts.append(f"<h2>{label}</h2>{df.to_html(border=0)}")
        html = head + "".join(body_parts) + "</body></html>"
        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")
        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict representation."""
        return {
            "target": self.target,
            "explanatory": self.explanatory,
            "delta_aic": float(self.delta_aic),
            "intervals": (
                None if self.intervals is None else [float(c) for c in self.intervals]
            ),
            "counts": _df_to_jsonable(self.counts),
            "row_prop": _df_to_jsonable(self.row_prop),
            "col_prop": _df_to_jsonable(self.col_prop),
            "expected": _df_to_jsonable(self.expected),
            "pearson_residuals": _df_to_jsonable(self.pearson_residuals),
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return a Plotly Figure spec rendering the counts table.

        Suitable for ``react-plotly.js`` and any Plotly renderer (DP-4).
        """
        df = self.counts.reset_index().rename(columns={"index": str(self.target)})
        return {
            "data": [
                {
                    "type": "table",
                    "header": {
                        "values": [[c] for c in df.columns.astype(str)],
                        "fill": {"color": "#f5f5f5"},
                        "align": "left",
                    },
                    "cells": {
                        "values": [df[c].tolist() for c in df.columns],
                        "align": "left",
                    },
                }
            ],
            "layout": {
                "title": (
                    f"target_summary: {self.target} × {self.explanatory} "
                    f"(ΔAIC = {self.delta_aic:.2f})"
                ),
            },
        }


def _df_to_jsonable(df: pd.DataFrame) -> dict[str, Any]:
    """Convert a small DataFrame to a JSON-safe nested dict."""
    return {
        "index": [_jsonable(v) for v in df.index],
        "columns": [_jsonable(c) for c in df.columns],
        "values": [[_jsonable(v) for v in row] for row in df.to_numpy().tolist()],
    }


def _jsonable(value: Any) -> Any:
    """Coerce a single scalar to a JSON-safe Python primitive."""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _bin_continuous(
    values: pd.Series,
    target: pd.Series,
    bins: int | Iterable[float] | None,
) -> tuple[pd.Series, list[float]]:
    """Categorize a continuous explanatory variable.

    Returns the binned series (string labels for crosstab) and the sorted
    interior boundary list.
    """
    arr = values.to_numpy(dtype=float)

    if bins is None:
        # AIC-optimal binning: bottom-up merge (catdap2 pool=1 default)
        result = optimal_binning(arr, target.to_numpy(), accuracy=None)
        boundaries = list(result.boundaries)
    elif isinstance(bins, int):
        if bins < 2:
            msg = f"bins must be >= 2 when given as int; got {bins}"
            raise ValueError(msg)
        # Equal-width cuts; boundaries are the interior edges
        edges = np.linspace(arr.min(), arr.max(), bins + 1)
        boundaries = [float(e) for e in edges[1:-1]]
    else:
        boundaries = sorted(float(b) for b in bins)

    if not boundaries:
        # Single-bin case — return everything in one labeled bucket
        label = f"[{arr.min():.3g}, {arr.max():.3g}]"
        labels = pd.Series([label] * len(arr), index=values.index)
        return labels, []

    # Build labels of the form "(a, b]" matching the bin assignment
    edge_list: list[float] = [
        float(arr.min()) - 1e-9,
        *boundaries,
        float(arr.max()) + 1e-9,
    ]
    cut = pd.cut(arr, bins=edge_list, include_lowest=True)
    labels = pd.Series(cut.astype(str), index=values.index)
    return labels, boundaries


def target_summary(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | Iterable[float] | None = None,
) -> TargetSummary:
    """Cross-tabulate a target × explanatory pair with proportions and ΔAIC.

    Rows containing ``NaN`` in either the target or the explanatory column
    are dropped before tabulation. Continuous explanatory variables are
    binned (default: AIC-optimal via :func:`pycatdap._pooling.optimal_binning`).

    Parameters
    ----------
    df : DataFrame
        Source data (not modified).
    target : str
        Target (response) variable column name. Must be categorical.
    explanatory : str
        Explanatory variable column name. May be categorical or continuous.
    bins : int, sequence of float, or None
        Binning specification for a continuous explanatory variable:

        - ``None`` (default): AIC-optimal binning
        - ``int``: that many equal-width bins
        - sequence: explicit interior boundaries

        Ignored for categorical explanatory variables.

    Returns
    -------
    TargetSummary

    Raises
    ------
    KeyError
        If *target* or *explanatory* is not in *df*.
    ValueError
        If *target* is a continuous variable.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_health_data()
    >>> r = pycatdap.target_summary(df, target="symptoms", explanatory="cholesterol")
    >>> r.delta_aic < 0  # cholesterol is informative for symptoms
    True
    """
    # Validate column membership (raises KeyError with a clear message)
    if target not in df.columns:
        msg = f"target column not found: {target!r}"
        raise KeyError(msg)
    if explanatory not in df.columns:
        msg = f"explanatory column not found: {explanatory!r}"
        raise KeyError(msg)

    # Validate target is not continuous
    target_kind = _detect_kind(df[target])
    if target_kind == "continuous":
        msg = (
            f"target {target!r} is continuous; target_summary requires a "
            f"categorical or boolean target. Bin it first or pick a different column."
        )
        raise ValueError(msg)

    work = df[[target, explanatory]].dropna()
    if work.empty:
        msg = "no non-null rows in (target, explanatory)"
        raise ValueError(msg)

    expl_kind = _detect_kind(work[explanatory])
    intervals: list[float] | None
    if expl_kind == "continuous":
        binned, intervals = _bin_continuous(work[explanatory], work[target], bins)
    else:
        binned = work[explanatory].astype(str)
        intervals = None

    counts = pd.crosstab(work[target], binned)
    counts.index.name = target
    counts.columns.name = explanatory

    observed = counts.to_numpy(dtype=float)
    row_totals = observed.sum(axis=1, keepdims=True)
    col_totals = observed.sum(axis=0, keepdims=True)
    n = float(observed.sum())

    # Proportions
    row_prop_arr = np.divide(
        observed, row_totals, out=np.zeros_like(observed), where=row_totals > 0
    )
    col_prop_arr = np.divide(
        observed, col_totals, out=np.zeros_like(observed), where=col_totals > 0
    )

    # Expected counts under independence
    expected_arr = row_totals @ col_totals / n
    # Pearson standardized residuals; guard divide-by-zero
    pearson_arr = np.divide(
        observed - expected_arr,
        np.sqrt(expected_arr),
        out=np.zeros_like(observed),
        where=expected_arr > 0,
    )

    def _wrap(arr: npt.NDArray[np.float64]) -> pd.DataFrame:
        return pd.DataFrame(arr, index=counts.index, columns=counts.columns)

    # ΔAIC via the same helper used by catdap1 / catdap2
    marginal_e = observed.sum(axis=1).astype(np.float64)
    marginal_f = observed.sum(axis=0).astype(np.float64)
    delta = compute_delta_aic(
        observed.astype(np.float64), marginal_e, marginal_f, int(n)
    )

    return TargetSummary(
        target=target,
        explanatory=explanatory,
        counts=counts,
        row_prop=_wrap(row_prop_arr),
        col_prop=_wrap(col_prop_arr),
        expected=_wrap(expected_arr),
        pearson_residuals=_wrap(pearson_arr),
        delta_aic=float(delta),
        intervals=intervals,
    )


__all__ = ["TargetSummary", "target_summary"]
