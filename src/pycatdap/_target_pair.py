"""Target × explanatory pair analysis (H-0004, H-0005).

Provides :func:`target_summary` for inspecting a (target, explanatory) pair
and its ΔAIC.

* Categorical / boolean target (H-0004) — returns :class:`TargetSummary`
  with cross-tabulation, proportions, Pearson standardized residuals, and
  multinomial-AIC ΔAIC.
* Continuous target (H-0005) — returns :class:`RegressionTargetSummary`
  with per-bin (count, target_mean, target_std), Gaussian-regression ΔAIC,
  and R² under the BIC / AIC / AICc criteria.

For continuous targets, an explicit ``target_bins=`` discretizes Y first
and routes through the categorical path (fallback for users who want the
contingency-table view; see H-0005 §7.2).

Both result types expose ``.show()``, ``.to_html()``, ``.to_dict()``, and
``.to_plotly_json()``.  The companion visualization function
:func:`pycatdap.plot_target` lives in :mod:`pycatdap.plot` so it can
dispatch on backend.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap._aic_regression import Criterion, compute_delta_aic_regression
from pycatdap._pooling import optimal_binning
from pycatdap.eda import _detect_kind

TargetBinsSpec = int | Sequence[float] | Literal["quantile", "equal_width", "fd"] | None

MISSING_LABEL = "_missing_"


# ---------------------------------------------------------------------------
# TargetSummary (categorical target — H-0004)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TargetSummary:
    """Result of :func:`target_summary` for a categorical / boolean target.

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


# ---------------------------------------------------------------------------
# RegressionTargetSummary (continuous target — H-0005)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RegressionTargetSummary:
    """Result of :func:`target_summary` for a continuous target (H-0005).

    Returned when ``target`` is detected as continuous and ``target_bins``
    is left at its default ``None``. The (target, explanatory) pair is
    scored with the **Gaussian regression AIC** of a piecewise-constant
    model: ``AIC = n * log(RSS / n) + penalty(k_means + 1)``. The target
    itself is never discretized; only the explanatory is binned.

    Attributes
    ----------
    target : str
        Target column name.
    explanatory : str
        Explanatory column name.
    bin_stats : pd.DataFrame
        Indexed by bin label. Columns: ``count``, ``target_mean``,
        ``target_std``. For ``M2`` missing-value handling, missing-X rows
        appear as a ``"_missing_"`` row when present.
    delta_aic : float
        ``AIC(model) - AIC(null)``. More negative = more informative.
    r_squared : float
        ``1 - RSS / TSS``, clipped to ``[0, 1]``.
    n_effective : int
        Number of rows used (Y non-missing; X missing handled as its own
        bin per H-0005 strategy M2).
    intervals : list[float] or None
        Continuous-X bin boundaries (excluding outer edges). ``None`` for
        categorical explanatory.
    criterion : {"aic", "aicc", "bic"}
        Penalty family used to compute ``delta_aic``.
    """

    target: str
    explanatory: str
    bin_stats: pd.DataFrame = field(repr=False)
    delta_aic: float
    r_squared: float
    n_effective: int
    intervals: list[float] | None = field(repr=False)
    criterion: Criterion

    def __repr__(self) -> str:
        return (
            f"RegressionTargetSummary(target={self.target!r}, "
            f"explanatory={self.explanatory!r}, "
            f"delta_aic={self.delta_aic:.4f}, "
            f"r_squared={self.r_squared:.4f}, "
            f"criterion={self.criterion!r})"
        )

    def show(self) -> None:
        """Display the bin-stats table inline in a Jupyter notebook."""
        try:
            from IPython.display import display
        except ImportError:
            print(
                f"RegressionTargetSummary: target={self.target}, "
                f"explanatory={self.explanatory}"
            )
            print(
                f"delta_aic = {self.delta_aic:.4f}  r_squared = {self.r_squared:.4f}  "
                f"criterion = {self.criterion}  n_effective = {self.n_effective}"
            )
            print(self.bin_stats)
            return
        display(f"RegressionTargetSummary: {self.target} × {self.explanatory}")
        display(
            f"ΔAIC = {self.delta_aic:.4f}  R² = {self.r_squared:.4f}  "
            f"criterion = {self.criterion}  n_effective = {self.n_effective}"
        )
        display(self.bin_stats)

    def to_html(self, path: str | Path | None = None) -> str:
        """Render the regression summary as a standalone HTML string."""
        title = f"target_summary (regression): {self.target} × {self.explanatory}"
        head = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>"
            "body{font-family:system-ui,sans-serif;margin:24px;}"
            "h1{font-size:1.2em;margin-bottom:0.3em;}"
            "h2{font-size:1em;margin-top:1.5em;color:#444;}"
            ".meta{color:#666;margin-bottom:0.6em;}"
            "table{border-collapse:collapse;font-size:0.9em;margin-bottom:0.5em;}"
            "th,td{border:1px solid #ddd;padding:4px 8px;text-align:right;}"
            "th{background:#f5f5f5;text-align:left;}"
            "td:first-child,th:first-child{text-align:left;}"
            "</style></head><body>"
        )
        body_parts = [
            f"<h1>{title}</h1>",
            (
                f"<div class='meta'>ΔAIC = {self.delta_aic:.4f}  |  "
                f"R² = {self.r_squared:.4f}  |  "
                f"criterion = {self.criterion}  |  "
                f"n_effective = {self.n_effective}</div>"
            ),
        ]
        if self.intervals is not None:
            cuts = ", ".join(f"{c:.3f}" for c in self.intervals)
            body_parts.append(f"<div class='meta'>X bin boundaries: [{cuts}]</div>")
        body_parts.append(
            f"<h2>Bin statistics</h2>{self.bin_stats.round(4).to_html(border=0)}"
        )
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
            "r_squared": float(self.r_squared),
            "n_effective": int(self.n_effective),
            "criterion": str(self.criterion),
            "intervals": (
                None if self.intervals is None else [float(c) for c in self.intervals]
            ),
            "bin_stats": _df_to_jsonable(self.bin_stats),
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return a Plotly Figure spec showing per-bin target means.

        Bar chart of ``target_mean`` per bin label, with hover values
        showing ``count`` and ``target_std``.
        """
        labels = [str(idx) for idx in self.bin_stats.index]
        means = [float(v) for v in self.bin_stats["target_mean"].to_list()]
        counts = [int(v) for v in self.bin_stats["count"].to_list()]
        stds = [float(v) for v in self.bin_stats["target_std"].to_list()]
        return {
            "data": [
                {
                    "type": "bar",
                    "x": labels,
                    "y": means,
                    "name": "target_mean",
                    "hovertemplate": (
                        "bin=%{x}<br>"
                        "target_mean=%{y:.4f}<br>"
                        "count=%{customdata[0]}<br>"
                        "target_std=%{customdata[1]:.4f}"
                        "<extra></extra>"
                    ),
                    "customdata": list(zip(counts, stds, strict=True)),
                }
            ],
            "layout": {
                "title": (
                    f"target_summary: {self.target} × {self.explanatory} "
                    f"(ΔAIC = {self.delta_aic:.2f}, R² = {self.r_squared:.3f})"
                ),
                "xaxis": {"title": self.explanatory},
                "yaxis": {"title": f"mean({self.target})"},
            },
        }


# ---------------------------------------------------------------------------
# JSON helpers (shared)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Explanatory binning helpers
# ---------------------------------------------------------------------------


def _bin_continuous(
    values: pd.Series,
    target: pd.Series,
    bins: int | Iterable[float] | None,
) -> tuple[pd.Series, list[float]]:
    """Categorize a continuous explanatory variable for the categorical path.

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
        edges = np.linspace(arr.min(), arr.max(), bins + 1)
        boundaries = [float(e) for e in edges[1:-1]]
    else:
        boundaries = sorted(float(b) for b in bins)

    if not boundaries:
        label = f"[{arr.min():.3g}, {arr.max():.3g}]"
        labels = pd.Series([label] * len(arr), index=values.index)
        return labels, []

    edge_list: list[float] = [
        float(arr.min()) - 1e-9,
        *boundaries,
        float(arr.max()) + 1e-9,
    ]
    cut = pd.cut(arr, bins=edge_list, include_lowest=True)
    labels = pd.Series(cut.astype(str), index=values.index)
    return labels, boundaries


def _build_regression_x_codes(
    x: pd.Series,
    bins: int | Iterable[float] | None,
) -> tuple[npt.NDArray[np.intp], list[str], list[float] | None]:
    """Map an explanatory variable to integer bin codes for regression mode.

    Implements H-0005 strategy M2: rows where X is missing receive a final
    code corresponding to the ``"_missing_"`` pseudo-bin.

    Returns
    -------
    codes : ndarray of intp, length len(x)
        Bin code per observation.
    labels : list of str
        Bin label per code (in code order).
    intervals : list of float or None
        Interior boundaries for continuous X; ``None`` for categorical.
    """
    expl_kind = _detect_kind(x)
    n = len(x)
    is_missing = x.isna().to_numpy()
    codes_full = np.zeros(n, dtype=np.intp)

    if expl_kind == "continuous":
        x_arr = x.to_numpy(dtype=float)
        x_clean = x_arr[~is_missing]
        if len(x_clean) == 0:
            return np.zeros(n, dtype=np.intp), [MISSING_LABEL], None
        boundaries: list[float]
        if bins is None:
            # Default for regression mode: quantile decile bins on X.
            # AIC-optimal X binning against a continuous Y is a future
            # enhancement (would require Gaussian-AIC pooling).
            try:
                _, edges = pd.qcut(x_clean, q=10, duplicates="drop", retbins=True)
                boundaries = [float(e) for e in list(edges)[1:-1]]
            except (ValueError, IndexError):
                boundaries = []
        elif isinstance(bins, int):
            if bins < 2:
                msg = f"bins must be >= 2 when given as int; got {bins}"
                raise ValueError(msg)
            edges = np.linspace(x_clean.min(), x_clean.max(), bins + 1)
            boundaries = [float(e) for e in edges[1:-1]]
        else:
            boundaries = sorted(float(b) for b in bins)

        if not boundaries:
            labels = [f"[{x_clean.min():.3g}, {x_clean.max():.3g}]"]
            codes_clean = np.zeros(len(x_clean), dtype=np.intp)
        else:
            edge_list = [
                float(x_clean.min()) - 1e-9,
                *boundaries,
                float(x_clean.max()) + 1e-9,
            ]
            cut = pd.cut(x_clean, bins=edge_list, include_lowest=True)
            codes_clean_raw, uniques = pd.factorize(cut, sort=True)
            codes_clean = codes_clean_raw.astype(np.intp)
            labels = [str(u) for u in uniques]
        intervals: list[float] | None = boundaries
    else:
        x_clean_series = x[~is_missing].astype(str)
        codes_clean_raw, uniques = pd.factorize(x_clean_series, sort=False)
        codes_clean = codes_clean_raw.astype(np.intp)
        labels = [str(u) for u in uniques]
        intervals = None

    if is_missing.any():
        missing_code = len(labels)
        labels.append(MISSING_LABEL)
        codes_full[~is_missing] = codes_clean
        codes_full[is_missing] = missing_code
    else:
        codes_full[:] = codes_clean

    return codes_full, labels, intervals


def _build_bin_stats(
    y: npt.NDArray[np.float64],
    codes: npt.NDArray[np.intp],
    labels: list[str],
) -> pd.DataFrame:
    """Per-bin count / target_mean / target_std table (regression mode)."""
    n_bins = len(labels)
    counts = np.bincount(codes, minlength=n_bins)
    sums = np.bincount(codes, weights=y, minlength=n_bins)
    sum_sq = np.bincount(codes, weights=y * y, minlength=n_bins)
    valid = counts > 0
    means = np.full(n_bins, np.nan)
    means[valid] = sums[valid] / counts[valid]
    var = np.zeros(n_bins, dtype=float)
    var[valid] = sum_sq[valid] / counts[valid] - means[valid] ** 2
    var = np.maximum(var, 0.0)
    stds = np.sqrt(var)
    return pd.DataFrame(
        {
            "count": counts.astype(int),
            "target_mean": means,
            "target_std": stds,
        },
        index=pd.Index(labels, name="bin"),
    )


# ---------------------------------------------------------------------------
# Target discretization (fallback path for continuous target + target_bins)
# ---------------------------------------------------------------------------


def _apply_target_discretization(
    df: pd.DataFrame,
    target: str,
    target_bins: TargetBinsSpec,
) -> pd.DataFrame:
    """Return a copy of *df* with ``target`` discretized per ``target_bins``.

    Used when a continuous target is combined with ``target_bins != None`` —
    the (c) fallback path that routes through the categorical-mode logic.
    """
    if target_bins is None:
        return df

    y = df[target]
    if isinstance(target_bins, str):
        if target_bins == "quantile":
            cut = pd.qcut(y, q=4, duplicates="drop")
        elif target_bins == "equal_width":
            cut = pd.cut(y, bins=4)
        elif target_bins == "fd":
            cut = pd.cut(y, bins=_freedman_diaconis_bins(y.dropna().to_numpy()))
        else:
            msg = (
                f"target_bins string must be 'quantile' | 'equal_width' | 'fd'; "
                f"got {target_bins!r}"
            )
            raise ValueError(msg)
    elif isinstance(target_bins, int):
        if target_bins < 2:
            msg = f"target_bins int must be >= 2; got {target_bins}"
            raise ValueError(msg)
        cut = pd.cut(y, bins=target_bins)
    else:
        cut = pd.cut(y, bins=list(target_bins))

    df_new: pd.DataFrame = df.copy()
    df_new[target] = cut.astype(str)
    return df_new


def _freedman_diaconis_bins(y: npt.NDArray[np.float64]) -> int:
    """Bin count via the Freedman-Diaconis rule, clipped to [2, 100]."""
    n = len(y)
    if n < 2:
        return 2
    q75, q25 = np.percentile(y, [75, 25])
    iqr = float(q75 - q25)
    if iqr <= 0:
        return max(2, int(np.sqrt(n)))
    h = 2 * iqr / np.cbrt(n)
    if h <= 0:
        return max(2, int(np.sqrt(n)))
    n_bins = int(np.ceil((y.max() - y.min()) / h))
    return max(2, min(n_bins, 100))


# ---------------------------------------------------------------------------
# Public API: target_summary
# ---------------------------------------------------------------------------


def target_summary(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | Iterable[float] | None = None,
    target_bins: TargetBinsSpec = None,
    criterion: Criterion = "bic",
) -> TargetSummary | RegressionTargetSummary:
    """Cross-tabulate or regress a (target, explanatory) pair, with ΔAIC.

    Behavior by target dtype:

    * **Categorical / boolean target**: returns :class:`TargetSummary`
      (H-0004). ``target_bins`` must be ``None`` (default).
    * **Continuous target + ``target_bins=None``**: returns
      :class:`RegressionTargetSummary` (H-0005); the target is never
      discretized. ``criterion`` selects the AIC penalty.
    * **Continuous target + ``target_bins`` given**: the target is
      discretized first, then routed through the categorical path; returns
      :class:`TargetSummary`.

    Parameters
    ----------
    df : DataFrame
        Source data (not modified).
    target : str
        Target (response) variable column name.
    explanatory : str
        Explanatory variable column name. May be categorical or continuous.
    bins : int, sequence of float, or None
        Binning specification for a continuous explanatory variable.
        Default ``None`` selects AIC-optimal binning in categorical mode
        and quantile (decile) binning in regression mode.
    target_bins : int, sequence, "quantile", "equal_width", "fd", or None
        Optional discretization of a continuous target (H-0005 fallback
        path). Ignored when target is already categorical.
    criterion : {"aic", "aicc", "bic"}
        Penalty family used in regression mode. Ignored in categorical
        mode. Default ``"bic"`` (Yao 1988 recommendation for changepoint
        structures).

    Returns
    -------
    TargetSummary or RegressionTargetSummary

    Raises
    ------
    KeyError
        If *target* or *explanatory* is not in *df*.
    ValueError
        If ``target_bins`` is given but target is not continuous, or if
        all rows of Y are missing.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_health_data()
    >>> r = pycatdap.target_summary(df, target="symptoms", explanatory="cholesterol")
    >>> r.delta_aic < 0  # cholesterol is informative for symptoms
    True
    """
    if target not in df.columns:
        msg = f"target column not found: {target!r}"
        raise KeyError(msg)
    if explanatory not in df.columns:
        msg = f"explanatory column not found: {explanatory!r}"
        raise KeyError(msg)

    target_kind = _detect_kind(df[target])

    if target_kind != "continuous":
        if target_bins is not None:
            msg = (
                f"target_bins must be None for a {target_kind} target; "
                f"got {target_bins!r}"
            )
            raise ValueError(msg)
        return _summary_categorical(df, target, explanatory, bins=bins)

    if target_bins is not None:
        df_binned = _apply_target_discretization(df, target, target_bins)
        return _summary_categorical(df_binned, target, explanatory, bins=bins)

    return _summary_regression(df, target, explanatory, bins=bins, criterion=criterion)


def _summary_categorical(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | Iterable[float] | None,
) -> TargetSummary:
    """Categorical / boolean target path (H-0004)."""
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

    row_prop_arr = np.divide(
        observed, row_totals, out=np.zeros_like(observed), where=row_totals > 0
    )
    col_prop_arr = np.divide(
        observed, col_totals, out=np.zeros_like(observed), where=col_totals > 0
    )

    expected_arr = row_totals @ col_totals / n
    pearson_arr = np.divide(
        observed - expected_arr,
        np.sqrt(expected_arr),
        out=np.zeros_like(observed),
        where=expected_arr > 0,
    )

    def _wrap(arr: npt.NDArray[np.float64]) -> pd.DataFrame:
        return pd.DataFrame(arr, index=counts.index, columns=counts.columns)

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


def _summary_regression(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    bins: int | Iterable[float] | None,
    criterion: Criterion,
) -> RegressionTargetSummary:
    """Continuous-target path with Gaussian regression AIC (H-0005).

    Implements strategy M2 for missing values: rows where Y is missing are
    dropped; rows where X is missing are kept and routed to a final
    "_missing_" pseudo-bin. This ensures ``n_effective`` and the null AIC
    are identical across X candidates that share the same Y.
    """
    y_series = df[target]
    y_mask = y_series.notna().to_numpy()
    if not y_mask.any():
        msg = f"all rows of target {target!r} are missing"
        raise ValueError(msg)

    work = df.loc[y_mask, [target, explanatory]]
    y = work[target].to_numpy(dtype=np.float64)
    n_eff = len(y)
    codes, labels, intervals = _build_regression_x_codes(work[explanatory], bins)
    delta_aic, r_squared = compute_delta_aic_regression(y, codes, criterion=criterion)
    bin_stats = _build_bin_stats(y, codes, labels)

    return RegressionTargetSummary(
        target=target,
        explanatory=explanatory,
        bin_stats=bin_stats,
        delta_aic=float(delta_aic),
        r_squared=float(r_squared),
        n_effective=int(n_eff),
        intervals=intervals,
        criterion=criterion,
    )


__all__ = [
    "RegressionTargetSummary",
    "TargetSummary",
    "target_summary",
]
