"""Visualization: mosaic plots, stacked bar charts, AIC comparison plots.

All functions require ``matplotlib``.  An ``ImportError`` with install
instructions is raised if the library is missing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from pycatdap.catdap1 import Catdap1Result
    from pycatdap.catdap2 import Catdap2Result


def _import_matplotlib() -> Any:
    """Import matplotlib or raise with install instructions."""
    try:
        import matplotlib  # noqa: F811
        import matplotlib.pyplot  # noqa: F811

        return matplotlib.pyplot
    except ImportError:
        msg = (
            "matplotlib is required for plotting. "
            "Install it with: pip install pycatdap[plot]"
        )
        raise ImportError(msg) from None


def aic_comparison_plot(
    result: Catdap1Result | Catdap2Result,
    response: str | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Horizontal bar chart of ΔAIC values per explanatory variable.

    Parameters
    ----------
    result : Catdap1Result or Catdap2Result
        Analysis result.
    response : str or None
        Response variable name.  Required for ``Catdap1Result`` when
        multiple responses are present.  Ignored for ``Catdap2Result``.
    ax : Axes or None
        Matplotlib axes.  Created if ``None``.
    **kwargs
        Passed to :meth:`Axes.barh`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    from pycatdap.catdap1 import Catdap1Result

    if isinstance(result, Catdap1Result):
        if response is None:
            response = str(result.aic.index[0])
        aic_row = result.aic.loc[response].dropna()
        variables = list(aic_row.index)
        values = list(aic_row.values)
    else:
        variables = list(result.aic["variable"])
        values = list(result.aic["aic"])

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    colors = ["tab:green" if v < 0 else "tab:red" for v in values]
    ax.barh(variables, values, color=colors, **kwargs)
    ax.set_xlabel("ΔAIC")
    ax.set_title(f"AIC Comparison (response: {response})")
    ax.axvline(0, color="black", linewidth=0.8)
    return ax


def barplot_twoway(
    table: pd.DataFrame,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Stacked proportional bar chart for a two-way frequency table.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table (e.g. from ``result.tway_tables``).
    ax : Axes or None
        Matplotlib axes.  Created if ``None``.
    **kwargs
        Passed to :meth:`DataFrame.plot.bar`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    proportions = table.div(table.sum(axis=0), axis=1).T

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    proportions.plot.bar(stacked=True, ax=ax, **kwargs)
    ax.set_ylabel("Proportion")
    ax.legend(title=str(table.index.name))
    return ax


def mosaic_plot(
    table: pd.DataFrame,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Mosaic plot for a two-way frequency table.

    Uses ``statsmodels.graphics.mosaicplot`` if available, otherwise
    falls back to a proportional rectangle plot with matplotlib.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table.
    ax : Axes or None
        Matplotlib axes.  Created if ``None``.
    **kwargs
        Passed to the underlying plot function.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    # Flatten table to dict for statsmodels mosaic
    try:
        import statsmodels.graphics.mosaicplot as _sm

        sm_mosaic = _sm.mosaic

        data_dict: dict[tuple[str, str], float] = {}
        for row_label in table.index:
            for col_label in table.columns:
                data_dict[(str(row_label), str(col_label))] = float(
                    table.loc[row_label, col_label]
                )
        sm_mosaic(data_dict, ax=ax, **kwargs)
    except ImportError:
        # Fallback: simple proportional rectangles
        _draw_simple_mosaic(table, ax)

    ax.set_title("Mosaic Plot")
    return ax


def _draw_simple_mosaic(table: pd.DataFrame, ax: Axes) -> None:
    """Draw a basic mosaic plot with matplotlib rectangles."""
    from matplotlib.patches import Rectangle

    total = float(table.to_numpy().sum())
    col_widths = table.sum(axis=0).to_numpy() / total
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

    x_offset = 0.0
    for j, _col_label in enumerate(table.columns):
        col_total = float(table.iloc[:, j].sum())
        y_offset = 0.0
        width = float(col_widths[j])
        for i, _row_label in enumerate(table.index):
            cell: float = float(table.iloc[i, j])  # type: ignore[arg-type]
            height = cell / col_total if col_total > 0 else 0
            color = colors[i % len(colors)]
            rect = Rectangle(
                (x_offset, y_offset),
                width,
                height,
                facecolor=color,
                edgecolor="white",
                linewidth=0.5,
            )
            ax.add_patch(rect)
            y_offset += height
        x_offset += width

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(str(table.columns.name or "Explanatory"))
    ax.set_ylabel(str(table.index.name or "Response"))
