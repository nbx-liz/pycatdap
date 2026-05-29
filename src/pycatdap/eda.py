"""Univariate EDA primitives.

Provides :func:`describe` for per-variable summary statistics and the
:class:`DescribeResult` dataclass for rich result display. The
visualization helpers ``plot_variable`` and ``plot_missing`` live in
:mod:`pycatdap.plot`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from pycatdap._jsonsafe import scalar_to_json

# Column ordering for the summary DataFrame produced by describe(). The
# kept column set deliberately emphasises CATDAP-relevant signals
# (n_missing, n_unique) rather than sklearn-style describe() output.
_SUMMARY_COLUMNS: tuple[str, ...] = (
    "kind",
    "n_obs",
    "n_missing",
    "missing_rate",
    "n_unique",
    "top",
    "top_freq",
    "mean",
    "std",
    "min",
    "q25",
    "median",
    "q75",
    "max",
)


def _detect_kind(series: pd.Series) -> str:
    """Heuristic classification of a column into a CATDAP-relevant kind.

    Returns one of: 'boolean', 'continuous', 'categorical', 'datetime', 'other'.
    """
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        # Numeric with very small cardinality is treated as categorical
        # so the summary surfaces top/top_freq instead of mean/std/...
        nunique = series.dropna().nunique()
        if nunique <= 2:
            return (
                "boolean" if {0, 1} >= set(series.dropna().unique()) else "categorical"
            )
        return "continuous"
    if (
        isinstance(series.dtype, pd.CategoricalDtype)
        or pd.api.types.is_string_dtype(series)
        or pd.api.types.is_object_dtype(series)
    ):
        return "categorical"
    return "other"


def _summarize_column(series: pd.Series) -> dict[str, Any]:
    """Compute the per-variable summary row."""
    kind = _detect_kind(series)
    n_obs = int(len(series))
    n_missing = int(series.isna().sum())
    missing_rate = float(n_missing / n_obs) if n_obs else float("nan")
    non_null = series.dropna()
    n_unique = int(non_null.nunique())

    row: dict[str, Any] = {
        "kind": kind,
        "n_obs": n_obs,
        "n_missing": n_missing,
        "missing_rate": missing_rate,
        "n_unique": n_unique,
        "top": None,
        "top_freq": None,
        "mean": None,
        "std": None,
        "min": None,
        "q25": None,
        "median": None,
        "q75": None,
        "max": None,
    }

    if len(non_null) == 0:
        return row

    # Top value (most-frequent) — always meaningful when nonempty
    counts = non_null.value_counts()
    row["top"] = counts.index[0]
    row["top_freq"] = int(counts.iloc[0])

    if kind == "continuous":
        arr = non_null.to_numpy(dtype=float, na_value=np.nan)
        row["mean"] = float(np.mean(arr))
        row["std"] = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
        row["min"] = float(np.min(arr))
        row["q25"] = float(np.quantile(arr, 0.25))
        row["median"] = float(np.median(arr))
        row["q75"] = float(np.quantile(arr, 0.75))
        row["max"] = float(np.max(arr))

    return row


@dataclass(frozen=True)
class DescribeResult:
    """Result of :func:`describe`.

    Attributes
    ----------
    summary : pd.DataFrame
        Per-variable summary table indexed by column name. Columns are
        listed in :data:`_SUMMARY_COLUMNS`. Continuous-only fields are
        ``None`` for non-continuous variables.
    n_rows : int
        Number of rows in the source DataFrame.
    n_cols : int
        Number of columns in the source DataFrame.
    """

    summary: pd.DataFrame = field(repr=False)
    n_rows: int
    n_cols: int

    def __repr__(self) -> str:
        return f"DescribeResult(n_rows={self.n_rows}, n_cols={self.n_cols})"

    def show(self) -> None:
        """Display the summary table inline in a Jupyter notebook.

        Falls back to ``print`` outside Jupyter.
        """
        try:
            from IPython.display import display
        except ImportError:
            print(self.summary)
            return
        display(self.summary)

    def to_html(self, path: str | Path | None = None) -> str:
        """Render the summary as a standalone HTML string.

        Parameters
        ----------
        path : str, Path, or None
            If provided, the HTML is also written to this file.

        Returns
        -------
        str
            HTML document.
        """
        title = "pycatdap.describe summary"
        head = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>"
            "body{font-family:system-ui,sans-serif;margin:24px;}"
            "h1{font-size:1.2em;margin-bottom:0.5em;}"
            ".meta{color:#666;margin-bottom:1em;}"
            "table{border-collapse:collapse;font-size:0.9em;}"
            "th,td{border:1px solid #ddd;padding:4px 8px;text-align:right;}"
            "th{background:#f5f5f5;text-align:left;}"
            "td:first-child,th:first-child{text-align:left;}"
            "</style></head><body>"
        )
        body = (
            f"<h1>{title}</h1>"
            f"<div class='meta'>n_rows={self.n_rows}, n_cols={self.n_cols}</div>"
            f"{self.summary.to_html(border=0)}"
            "</body></html>"
        )
        html = head + body
        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")
        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict representation."""
        return {
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "variables": self.summary.to_dict(orient="index"),
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return a Plotly Figure spec rendering the summary as a table.

        Suitable for ``react-plotly.js`` and any Plotly renderer (DP-4).
        """
        df = self.summary.reset_index().rename(columns={"index": "variable"})
        return {
            "data": [
                {
                    "type": "table",
                    "header": {
                        "values": [[c] for c in df.columns],
                        "fill": {"color": "#f5f5f5"},
                        "align": "left",
                    },
                    "cells": {
                        "values": [
                            [scalar_to_json(v) for v in df[c]] for c in df.columns
                        ],
                        "align": "left",
                    },
                }
            ],
            "layout": {
                "title": (
                    f"describe summary (n_rows={self.n_rows}, n_cols={self.n_cols})"
                ),
            },
        }


def describe(df: pd.DataFrame) -> DescribeResult:
    """Compute per-variable summary statistics for a DataFrame.

    The summary emphasizes CATDAP-relevant signals: variable kind
    (boolean / continuous / categorical / datetime / other), missing
    counts and rate, cardinality, the most-frequent value and its
    frequency, and (for continuous variables only) basic distribution
    statistics.

    Parameters
    ----------
    df : DataFrame
        Input data.

    Returns
    -------
    DescribeResult
        Result object with rich display methods (``show``, ``to_html``,
        ``to_dict``, ``to_plotly_json``).

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> result = pycatdap.describe(df)
    >>> result.summary.loc["Sex", "n_unique"]
    2
    """
    if df.empty and len(df.columns) == 0:
        msg = "describe: DataFrame has no columns"
        raise ValueError(msg)

    rows: dict[str, dict[str, Any]] = {}
    for col in df.columns:
        rows[str(col)] = _summarize_column(df[col])

    summary = pd.DataFrame.from_dict(
        rows, orient="index", columns=list(_SUMMARY_COLUMNS)
    )
    summary.index.name = "variable"

    return DescribeResult(
        summary=summary,
        n_rows=int(len(df)),
        n_cols=int(len(df.columns)),
    )


__all__ = ["DescribeResult", "describe"]
