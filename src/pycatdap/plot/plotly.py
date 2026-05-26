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

if TYPE_CHECKING:
    import pandas as pd
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
