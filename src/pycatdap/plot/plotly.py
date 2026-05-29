"""Plotly backend for pycatdap visualization.

Implements the same three primitives as the matplotlib backend:
``mosaic_plot``, ``barplot_twoway``, ``aic_comparison_plot``. All
functions return ``plotly.graph_objects.Figure`` objects suitable for
inline display in Jupyter, embedding in HTML reports, or JSON
serialization for web frontends (e.g. LizyStudio).

See :mod:`pycatdap.plot` for the canonical dispatcher.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt
import pandas as pd

if TYPE_CHECKING:
    import plotly.graph_objects as _go

    from pycatdap.catdap1 import Catdap1Result
    from pycatdap.catdap2 import Catdap2Result


def _import_plotly() -> Any:
    """Import plotly.graph_objects or raise with install instructions."""
    try:
        import plotly.graph_objects as go

        return go
    except ImportError:
        msg = (
            "plotly is required for the Plotly backend. "
            "Install it with: pip install 'pycatdap[plotly]'"
        )
        raise ImportError(msg) from None


_INFORMATIVE_COLOR = "#2ca02c"
_NONINFORMATIVE_COLOR = "#d62728"
_MOSAIC_PALETTE = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
]


def aic_comparison_plot(
    result: Catdap1Result | Catdap2Result,
    response: str | None = None,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Horizontal bar chart of ΔAIC values per explanatory variable (Plotly).

    Parameters
    ----------
    result : Catdap1Result or Catdap2Result
        Analysis result.
    response : str or None
        Response variable name. Required for ``Catdap1Result`` when
        multiple responses are present. Ignored for ``Catdap2Result``.

    Returns
    -------
    plotly.graph_objects.Figure
        Horizontal bar chart; green bars indicate informative variables
        (ΔAIC < 0), red bars indicate non-informative (ΔAIC ≥ 0).
    """
    go = _import_plotly()

    from pycatdap.catdap1 import Catdap1Result

    if isinstance(result, Catdap1Result):
        if response is None:
            response = str(result.aic.index[0])
        row = result.aic.loc[response].dropna()
        variables = [str(v) for v in row.index]
        values = [float(v) for v in row.to_numpy()]
        title = f"AIC Comparison (response: {response})"
    else:
        variables = [str(v) for v in result.aic["variable"].tolist()]
        values = [float(v) for v in result.aic["aic"].to_numpy()]
        title = "AIC Comparison"

    colors = [_INFORMATIVE_COLOR if v < 0 else _NONINFORMATIVE_COLOR for v in values]
    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=variables,
                orientation="h",
                marker={"color": colors},
                name="ΔAIC",
            )
        ]
    )
    fig.update_layout(
        title=title,
        xaxis={"title": "ΔAIC", "zeroline": True, "zerolinecolor": "black"},
        yaxis={"title": "Variable", "automargin": True},
    )
    return fig


def barplot_twoway(
    table: pd.DataFrame,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Stacked proportional bar chart for a two-way frequency table (Plotly).

    Each column of ``table`` becomes a stacked bar of unit height, with
    each segment proportional to ``table.iloc[i, j] / table.iloc[:, j].sum()``.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    proportions = table.div(table.sum(axis=0), axis=1)

    fig = go.Figure()
    for i, row_label in enumerate(proportions.index):
        fig.add_trace(
            go.Bar(
                x=[str(c) for c in proportions.columns],
                y=[float(v) for v in proportions.loc[row_label].to_numpy()],
                name=str(row_label),
                marker={"color": _MOSAIC_PALETTE[i % len(_MOSAIC_PALETTE)]},
            )
        )
    fig.update_layout(
        barmode="stack",
        yaxis={"title": "Proportion", "range": [0, 1]},
        xaxis={"title": str(table.columns.name or "")},
        legend={"title": {"text": str(table.index.name or "")}},
    )
    return fig


def mosaic_plot(
    table: pd.DataFrame,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Mosaic plot for a two-way frequency table (Plotly).

    Each column's width is proportional to its marginal total; each
    cell's height within a column is proportional to its conditional
    frequency.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    total = float(table.to_numpy().sum())
    if total <= 0:
        msg = "mosaic_plot: table sum must be positive"
        raise ValueError(msg)

    col_totals = table.sum(axis=0).to_numpy(dtype=float)
    col_widths = col_totals / total

    fig = go.Figure()
    x_offset = 0.0
    seen_rows: set[str] = set()

    for j, col_label in enumerate(table.columns):
        col_total = float(col_totals[j])
        width = float(col_widths[j])
        y_offset = 0.0
        for i, row_label in enumerate(table.index):
            cell = float(table.iloc[i, j])  # type: ignore[arg-type]
            height = cell / col_total if col_total > 0 else 0.0
            color = _MOSAIC_PALETTE[i % len(_MOSAIC_PALETTE)]
            row_key = str(row_label)
            show_legend = row_key not in seen_rows
            seen_rows.add(row_key)
            fig.add_trace(
                go.Scatter(
                    x=[
                        x_offset,
                        x_offset + width,
                        x_offset + width,
                        x_offset,
                        x_offset,
                    ],
                    y=[
                        y_offset,
                        y_offset,
                        y_offset + height,
                        y_offset + height,
                        y_offset,
                    ],
                    fill="toself",
                    fillcolor=color,
                    line={"color": "white", "width": 1},
                    mode="lines",
                    name=row_key,
                    showlegend=show_legend,
                    hovertemplate=(
                        f"{table.columns.name or 'col'}={col_label}<br>"
                        f"{table.index.name or 'row'}={row_label}<br>"
                        f"freq=%{{customdata}}<extra></extra>"
                    ),
                    customdata=[cell] * 5,
                )
            )
            y_offset += height
        x_offset += width

    fig.update_layout(
        title="Mosaic Plot",
        xaxis={
            "title": str(table.columns.name or "Explanatory"),
            "range": [0, 1],
            "showgrid": False,
            "zeroline": False,
        },
        yaxis={
            "title": str(table.index.name or "Response"),
            "range": [0, 1],
            "showgrid": False,
            "zeroline": False,
        },
        legend={"title": {"text": str(table.index.name or "")}},
    )
    return fig


def _infer_plot_kind(series: pd.Series) -> str:
    """Infer 'hist' (continuous) or 'bar' (categorical) for plot_variable."""
    if (
        pd.api.types.is_numeric_dtype(series)
        and not pd.api.types.is_bool_dtype(series)
        and series.dropna().nunique() > 2
    ):
        return "hist"
    return "bar"


def plot_variable(
    df: pd.DataFrame,
    col: str,
    kind: str = "auto",
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Plot a single variable (Plotly): histogram or bar chart.

    Parameters
    ----------
    df : DataFrame
        Source data.
    col : str
        Column name.
    kind : {'auto', 'hist', 'bar'}
        ``'auto'`` infers from dtype; otherwise explicit.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    if col not in df.columns:
        msg = f"plot_variable: column {col!r} not found in DataFrame"
        raise KeyError(msg)
    if kind not in {"auto", "hist", "bar"}:
        msg = f"plot_variable: kind must be 'auto', 'hist', or 'bar' (got {kind!r})"
        raise ValueError(msg)

    series = df[col].dropna()
    resolved_kind = _infer_plot_kind(series) if kind == "auto" else kind

    if resolved_kind == "hist":
        fig = go.Figure(
            data=[
                go.Histogram(
                    x=series.to_numpy(),
                    marker={"color": "#1f77b4"},
                    name=str(col),
                )
            ]
        )
        fig.update_layout(
            title=str(col),
            xaxis={"title": str(col)},
            yaxis={"title": "Frequency"},
        )
        return fig

    counts = series.value_counts().sort_index()
    fig = go.Figure(
        data=[
            go.Bar(
                x=[str(idx) for idx in counts.index],
                y=counts.to_numpy(),
                marker={"color": "#1f77b4"},
                name=str(col),
            )
        ]
    )
    fig.update_layout(
        title=str(col),
        xaxis={"title": str(col)},
        yaxis={"title": "Count"},
    )
    return fig


def plot_target(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    kind: str = "auto",
    bins: int | list[float] | None = None,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Plot a target × explanatory relationship (Plotly backend).

    Auto-dispatch mirrors the matplotlib backend; see
    :func:`pycatdap.plot.plot_target` for the dispatch table.

    Parameters
    ----------
    df : DataFrame
        Source data.
    target : str
        Target (response) column. Must be categorical.
    explanatory : str
        Explanatory column. May be categorical or continuous.
    kind : {'auto', 'stacked', 'mosaic', 'violin', 'box', 'hist'}
        Plot kind. ``'auto'`` dispatches by dtype.
    bins : int, sequence of float, or None
        Binning for continuous explanatory.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    from pycatdap.eda import _detect_kind

    if target not in df.columns:
        msg = f"plot_target: target column not found: {target!r}"
        raise KeyError(msg)
    if explanatory not in df.columns:
        msg = f"plot_target: explanatory column not found: {explanatory!r}"
        raise KeyError(msg)

    target_kind = _detect_kind(df[target])
    expl_kind = _detect_kind(df[explanatory])
    from pycatdap.plot import _resolve_target_kind

    resolved = _resolve_target_kind(
        kind, target_kind, expl_kind, continuous_default="box"
    )

    # H-0005: continuous target → regression-mode plotting.
    if target_kind == "continuous":
        return _plot_target_regression_plotly(
            df,
            target=target,
            explanatory=explanatory,
            kind=resolved,
            bins=bins,
        )

    if resolved in {"stacked", "mosaic"}:
        from pycatdap._target_pair import _summary_categorical

        summary = _summary_categorical(
            df, target=target, explanatory=explanatory, bins=bins
        )
        if resolved == "stacked":
            fig = barplot_twoway(summary.counts)
        else:
            fig = mosaic_plot(summary.counts)
        fig.update_layout(title=f"{target} × {explanatory}")
        return fig

    work = df[[target, explanatory]].dropna()
    groups = sorted(work[target].astype(str).unique().tolist())

    fig = go.Figure()
    for g in groups:
        arr = work.loc[work[target].astype(str) == g, explanatory].to_numpy(dtype=float)
        if resolved == "violin":
            fig.add_trace(go.Violin(y=arr, name=str(g), box_visible=True))
        elif resolved == "box":
            fig.add_trace(go.Box(y=arr, name=str(g)))
        elif resolved == "hist":
            fig.add_trace(go.Histogram(x=arr, name=str(g), opacity=0.5))
        else:
            msg = f"plot_target: unsupported kind {resolved!r}"
            raise ValueError(msg)

    if resolved == "hist":
        fig.update_layout(barmode="overlay", xaxis={"title": str(explanatory)})
    else:
        fig.update_layout(
            xaxis={"title": str(target)}, yaxis={"title": str(explanatory)}
        )
    fig.update_layout(title=f"{explanatory} by {target}")
    return fig


def _plot_target_regression_plotly(
    df: pd.DataFrame,
    *,
    target: str,
    explanatory: str,
    kind: str,
    bins: int | list[float] | None,
) -> _go.Figure:
    """Continuous-target Plotly plotting (H-0005 regression mode)."""
    go = _import_plotly()
    from pycatdap._target_pair import _summary_regression
    from pycatdap.eda import _detect_kind

    expl_kind = _detect_kind(df[explanatory])
    work = df[df[target].notna()][[target, explanatory]]

    if kind in {"box", "violin"}:
        labels: list[str]
        y_groups: list[Any]
        if expl_kind == "continuous":
            summary = _summary_regression(
                work,
                target=target,
                explanatory=explanatory,
                bins=bins,
                criterion="bic",
            )
            labels = [str(idx) for idx in summary.bin_stats.index]
            x_arr = work[explanatory].to_numpy(dtype=float)
            y_arr = work[target].to_numpy(dtype=float)
            y_groups = []
            if summary.intervals:
                import numpy as _np

                edges = [
                    float(_np.nanmin(x_arr)) - 1e-9,
                    *summary.intervals,
                    float(_np.nanmax(x_arr)) + 1e-9,
                ]
                cuts = pd.cut(x_arr, bins=edges, include_lowest=True).astype(str)
                for label in labels:
                    mask: npt.NDArray[np.bool_]
                    if label == "_missing_":
                        mask = pd.isna(work[explanatory]).to_numpy()
                    else:
                        mask = np.asarray(cuts == label, dtype=bool)
                    y_groups.append(y_arr[mask])
            else:
                y_groups = [y_arr]
                labels = labels or [str(explanatory)]
        else:
            x_filled = (
                work[explanatory]
                .astype(object)
                .where(work[explanatory].notna(), "_missing_")
                .astype(str)
            )
            labels = sorted(x_filled.unique().tolist())
            y_groups = [
                work.loc[x_filled == lbl, target].to_numpy(dtype=float)
                for lbl in labels
            ]

        fig = go.Figure()
        for label, arr in zip(labels, y_groups, strict=True):
            if kind == "violin":
                fig.add_trace(go.Violin(y=arr, name=label, box_visible=True))
            else:
                fig.add_trace(go.Box(y=arr, name=label))
        fig.update_layout(
            title=f"{target} by {explanatory}",
            xaxis={"title": str(explanatory)},
            yaxis={"title": str(target)},
        )
        return fig

    if kind == "bin_means":
        summary = _summary_regression(
            work,
            target=target,
            explanatory=explanatory,
            bins=bins,
            criterion="bic",
        )
        labels = [str(idx) for idx in summary.bin_stats.index]
        means = summary.bin_stats["target_mean"].to_list()
        fig = go.Figure(data=[go.Bar(x=labels, y=means)])
        fig.update_layout(
            title=f"mean({target}) by {explanatory} (ΔAIC={summary.delta_aic:.2f})",
            xaxis={"title": str(explanatory)},
            yaxis={"title": f"mean({target})"},
        )
        return fig

    if kind == "scatter":
        if expl_kind != "continuous":
            msg = "plot_target: kind='scatter' requires a continuous explanatory"
            raise ValueError(msg)
        import numpy as _np

        x = work[explanatory].to_numpy(dtype=float)
        y = work[target].to_numpy(dtype=float)
        mask = ~_np.isnan(x)
        fig = go.Figure()
        fig.add_trace(
            go.Scattergl(
                x=x[mask],
                y=y[mask],
                mode="markers",
                marker={"opacity": 0.4, "size": 6},
                name="points",
            )
        )
        summary = _summary_regression(
            work,
            target=target,
            explanatory=explanatory,
            bins=bins,
            criterion="bic",
        )
        if summary.intervals:
            edges = [
                float(_np.nanmin(x)),
                *summary.intervals,
                float(_np.nanmax(x)),
            ]
            centers = [(edges[i] + edges[i + 1]) / 2 for i in range(len(edges) - 1)]
            bin_means_no_missing = [
                float(v)
                for label, v in summary.bin_stats["target_mean"].items()
                if str(label) != "_missing_"
            ]
            if len(centers) == len(bin_means_no_missing):
                fig.add_trace(
                    go.Scatter(
                        x=centers,
                        y=bin_means_no_missing,
                        mode="lines+markers",
                        line={"color": "red", "width": 2},
                        name="bin mean",
                    )
                )
        fig.update_layout(
            title=f"{target} vs {explanatory} (ΔAIC={summary.delta_aic:.2f})",
            xaxis={"title": str(explanatory)},
            yaxis={"title": str(target)},
        )
        return fig

    if kind == "hist":
        x_filled = (
            work[explanatory]
            .astype(object)
            .where(work[explanatory].notna(), "_missing_")
            .astype(str)
        )
        labels = sorted(x_filled.unique().tolist())
        fig = go.Figure()
        for label in labels:
            fig.add_trace(
                go.Histogram(
                    x=work.loc[x_filled == label, target].to_numpy(dtype=float),
                    name=str(label),
                    opacity=0.5,
                )
            )
        fig.update_layout(
            barmode="overlay",
            title=f"{target} by {explanatory}",
            xaxis={"title": str(target)},
        )
        return fig

    msg = (
        f"plot_target: kind {kind!r} is not supported for a continuous target. "
        f"Use 'auto', 'box', 'violin', 'scatter', 'bin_means', or 'hist'."
    )
    raise ValueError(msg)


def _coerce_aic_dataframe(
    result: Catdap1Result | pd.DataFrame,
) -> pd.DataFrame:
    """Extract a ΔAIC DataFrame from a Catdap1Result or accept one directly."""
    if isinstance(result, pd.DataFrame):
        return result
    aic = getattr(result, "aic", None)
    if isinstance(aic, pd.DataFrame):
        return aic
    msg = (
        f"aic_heatmap: expected Catdap1Result or pd.DataFrame; "
        f"got {type(result).__name__}"
    )
    raise TypeError(msg)


def aic_heatmap(
    result: Catdap1Result | pd.DataFrame,
    *,
    threshold: float | None = 0.0,
    colorscale: str = "RdYlGn_r",
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Diverging ΔAIC heatmap (H-0006, Plotly backend).

    Parameters
    ----------
    result : Catdap1Result or DataFrame
        ΔAIC values; ``Catdap1Result.aic`` is extracted automatically.
    threshold : float or None
        Cells with ΔAIC strictly less than ``threshold`` get a ``*``
        annotation. Pass ``None`` to disable.
    colorscale : str
        Plotly diverging colorscale name. Default ``'RdYlGn_r'`` paints
        informative cells green.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    aic_df = _coerce_aic_dataframe(result)
    data = aic_df.to_numpy(dtype=float)

    finite = data[np.isfinite(data)]
    if finite.size == 0:
        abs_max = 1.0
    else:
        abs_max = float(np.nanmax(np.abs(finite)))
        if abs_max == 0.0:
            abs_max = 1.0

    annotations: list[dict[str, Any]] = []
    if threshold is not None:
        n_rows, n_cols = data.shape
        for i in range(n_rows):
            for j in range(n_cols):
                value = data[i, j]
                if np.isfinite(value) and value < threshold:
                    annotations.append(
                        {
                            "x": str(aic_df.columns[j]),
                            "y": str(aic_df.index[i]),
                            "text": "*",
                            "showarrow": False,
                            "font": {"size": 14, "color": "black"},
                        }
                    )

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=data,
                x=[str(c) for c in aic_df.columns],
                y=[str(r) for r in aic_df.index],
                colorscale=colorscale,
                zmid=0,
                zmin=-abs_max,
                zmax=abs_max,
                colorbar={"title": "ΔAIC"},
                hovertemplate=(
                    "Response: %{y}<br>Explanatory: %{x}<br>"
                    "ΔAIC: %{z:.3f}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title="ΔAIC heatmap",
        xaxis={"title": "Explanatory"},
        yaxis={"title": "Response", "autorange": "reversed"},
        annotations=annotations,
    )
    return fig


def _coerce_residuals(table: Any) -> pd.DataFrame:
    """Extract Pearson residuals from a TargetSummary or compute from a crosstab.

    Mirrors the matplotlib backend's implementation. Rejects
    RegressionTargetSummary with a pointer to plot_target(kind="scatter").
    """
    from pycatdap._target_pair import RegressionTargetSummary, TargetSummary

    if isinstance(table, TargetSummary):
        return table.pearson_residuals
    if isinstance(table, RegressionTargetSummary):
        msg = (
            "association_plot does not support RegressionTargetSummary: "
            "Pearson standardized residuals are undefined for a continuous "
            "target. Use pycatdap.plot_target(df, target, explanatory, "
            'kind="scatter") instead.'
        )
        raise TypeError(msg)
    if isinstance(table, pd.DataFrame):
        observed = table.to_numpy(dtype=float)
        total = observed.sum()
        if total <= 0:
            msg = "association_plot: crosstab total must be positive"
            raise ValueError(msg)
        row_sum = observed.sum(axis=1, keepdims=True)
        col_sum = observed.sum(axis=0, keepdims=True)
        expected = row_sum @ col_sum / total
        residuals = np.divide(
            observed - expected,
            np.sqrt(expected),
            out=np.zeros_like(observed),
            where=expected > 0,
        )
        return pd.DataFrame(residuals, index=table.index, columns=table.columns)
    msg = (
        f"association_plot: expected TargetSummary or pd.DataFrame; "
        f"got {type(table).__name__}"
    )
    raise TypeError(msg)


def association_plot(
    table: Any,
    *,
    threshold: float | None = 2.0,
    colorscale: str = "RdBu_r",
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """vcd-style heatmap of Pearson standardized residuals (H-0006, Plotly).

    Parameters
    ----------
    table : TargetSummary or DataFrame
        :class:`TargetSummary` or a raw two-way contingency table.
    threshold : float or None
        Overlay ``*`` on cells whose ``|residual| > threshold``. ``None``
        disables the annotation.
    colorscale : str
        Plotly diverging colorscale. Default ``'RdBu_r'``.

    Returns
    -------
    plotly.graph_objects.Figure

    Raises
    ------
    TypeError
        If *table* is a :class:`RegressionTargetSummary` or unsupported.
    """
    go = _import_plotly()

    residuals = _coerce_residuals(table)
    data = residuals.to_numpy(dtype=float)

    finite = data[np.isfinite(data)]
    abs_max = float(np.nanmax(np.abs(finite))) if finite.size else 1.0
    if abs_max == 0.0:
        abs_max = 1.0

    annotations: list[dict[str, Any]] = []
    if threshold is not None:
        n_rows, n_cols = data.shape
        for i in range(n_rows):
            for j in range(n_cols):
                value = data[i, j]
                if np.isfinite(value) and abs(value) > threshold:
                    annotations.append(
                        {
                            "x": str(residuals.columns[j]),
                            "y": str(residuals.index[i]),
                            "text": "*",
                            "showarrow": False,
                            "font": {"size": 14, "color": "black"},
                        }
                    )

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=data,
                x=[str(c) for c in residuals.columns],
                y=[str(r) for r in residuals.index],
                colorscale=colorscale,
                zmid=0,
                zmin=-abs_max,
                zmax=abs_max,
                colorbar={"title": "Pearson residual"},
                hovertemplate=("%{y} × %{x}<br>residual: %{z:.3f}<extra></extra>"),
            )
        ]
    )
    fig.update_layout(
        title="Pearson standardized residuals",
        xaxis={"title": str(residuals.columns.name or "")},
        yaxis={"title": str(residuals.index.name or ""), "autorange": "reversed"},
        annotations=annotations,
    )
    return fig


def plot_missing(
    df: pd.DataFrame,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Bar chart of missing-value counts per column (Plotly).

    Parameters
    ----------
    df : DataFrame
        Source data.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _import_plotly()

    counts = df.isna().sum().astype(int)
    fig = go.Figure(
        data=[
            go.Bar(
                x=[str(c) for c in counts.index],
                y=counts.to_numpy(),
                marker={"color": "#d62728"},
                name="Missing",
            )
        ]
    )
    fig.update_layout(
        title="Missing values per column",
        xaxis={"title": "Variable"},
        yaxis={"title": "Missing count"},
    )
    return fig


# ---------------------------------------------------------------------------
# Phase I (H-0012): confusion matrix visualization
# ---------------------------------------------------------------------------


def plot_confusion(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    labels: list[Any] | None = None,
    normalize: str | None = None,
    colorscale: str = "Blues",
    show_values: bool = True,
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Confusion matrix heatmap (H-0012 Phase I, Plotly backend).

    See :func:`pycatdap.plot.matplotlib.plot_confusion` for the parameter
    contract. ``cmap`` is renamed ``colorscale`` to match Plotly conventions.
    """
    go = _import_plotly()
    from pycatdap.plot.matplotlib import _build_confusion_matrix

    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    matrix, label_strs = _build_confusion_matrix(
        y_true_arr, y_pred_arr, labels, normalize
    )

    annotations: list[dict[str, Any]] = []
    if show_values:
        if normalize:
            threshold = matrix[np.isfinite(matrix)].max() / 2.0 if matrix.size else 0.5
            fmt = "{:.2f}"
        else:
            threshold = matrix.max() / 2.0 if matrix.size else 0.0
            fmt = "{:.0f}"
        for i, true_lbl in enumerate(label_strs):
            for j, pred_lbl in enumerate(label_strs):
                value = matrix[i, j]
                if not np.isfinite(value):
                    continue
                color = "white" if value > threshold else "black"
                annotations.append(
                    {
                        "x": pred_lbl,
                        "y": true_lbl,
                        "text": fmt.format(value),
                        "showarrow": False,
                        "font": {"size": 12, "color": color},
                    }
                )

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=matrix,
                x=label_strs,
                y=label_strs,
                colorscale=colorscale,
                colorbar={"title": "proportion" if normalize else "count"},
                hovertemplate=(
                    "True: %{y}<br>Predicted: %{x}<br>value: %{z}<extra></extra>"
                ),
            )
        ]
    )
    title_suffix = " (normalized)" if normalize else ""
    fig.update_layout(
        title=f"Confusion matrix{title_suffix}",
        xaxis={"title": "Predicted"},
        yaxis={"title": "True", "autorange": "reversed"},
        annotations=annotations,
    )
    return fig


def plot_confusion_by_slice(
    df: pd.DataFrame,
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    var: str,
    *,
    labels: list[Any] | None = None,
    n_cols: int = 3,
    normalize: str | None = "true",
    colorscale: str = "Blues",
    **kwargs: Any,  # noqa: ARG001
) -> _go.Figure:
    """Per-category small-multiples of confusion matrices (H-0012 Phase I, Plotly)."""
    go = _import_plotly()
    from plotly.subplots import make_subplots

    from pycatdap.plot.matplotlib import _build_confusion_matrix

    if var not in df.columns:
        msg = f"plot_confusion_by_slice: var={var!r} not in df.columns"
        raise KeyError(msg)
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    if len(y_true_arr) != len(df) or len(y_pred_arr) != len(df):
        msg = (
            f"y_true / y_pred length must equal len(df) "
            f"(got {len(y_true_arr)} / {len(y_pred_arr)} vs {len(df)})"
        )
        raise ValueError(msg)

    if labels is None:
        labels = sorted(
            {*np.unique(y_true_arr).tolist(), *np.unique(y_pred_arr).tolist()}
        )

    categories = sorted(df[var].dropna().unique().tolist(), key=str)
    n_panels = len(categories)
    if n_panels == 0:
        msg = f"plot_confusion_by_slice: var={var!r} has no non-NA categories"
        raise ValueError(msg)

    n_cols = max(1, min(n_cols, n_panels))
    n_rows = (n_panels + n_cols - 1) // n_cols

    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=[f"{var} = {c}" for c in categories],
    )

    for idx, category in enumerate(categories):
        row = idx // n_cols + 1
        col = idx % n_cols + 1
        mask = (df[var] == category).to_numpy()
        matrix, label_strs = _build_confusion_matrix(
            y_true_arr[mask], y_pred_arr[mask], labels, normalize
        )
        fig.add_trace(
            go.Heatmap(
                z=matrix,
                x=label_strs,
                y=label_strs,
                colorscale=colorscale,
                showscale=(idx == 0),
                hovertemplate=(
                    f"{var} = {category}<br>True: %{{y}}<br>"
                    "Predicted: %{x}<br>value: %{z}<extra></extra>"
                ),
            ),
            row=row,
            col=col,
        )

    fig.update_layout(
        title=f"Confusion matrix by {var}",
        height=350 * n_rows,
        width=350 * n_cols,
    )
    fig.update_yaxes(autorange="reversed")
    return fig
