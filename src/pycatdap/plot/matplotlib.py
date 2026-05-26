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
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot a single variable: histogram for continuous, bar chart for categorical.

    Parameters
    ----------
    df : DataFrame
        Source data.
    col : str
        Column name.
    kind : {'auto', 'hist', 'bar'}
        ``'auto'`` infers from dtype; otherwise explicit.
    ax : Axes or None
        Matplotlib axes. Created if ``None``.
    **kwargs
        Forwarded to the underlying matplotlib call.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    if col not in df.columns:
        msg = f"plot_variable: column {col!r} not found in DataFrame"
        raise KeyError(msg)

    if kind not in {"auto", "hist", "bar"}:
        msg = f"plot_variable: kind must be 'auto', 'hist', or 'bar' (got {kind!r})"
        raise ValueError(msg)

    series = df[col].dropna()
    resolved_kind = _infer_plot_kind(series) if kind == "auto" else kind

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    if resolved_kind == "hist":
        ax.hist(series.to_numpy(), **kwargs)
        ax.set_xlabel(str(col))
        ax.set_ylabel("Frequency")
    else:
        counts = series.value_counts().sort_index()
        ax.bar(
            [str(idx) for idx in counts.index],
            counts.to_numpy(),
            **kwargs,
        )
        ax.set_xlabel(str(col))
        ax.set_ylabel("Count")

    ax.set_title(str(col))
    return ax


def plot_target(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    kind: str = "auto",
    bins: int | list[float] | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Plot a target × explanatory relationship.

    Auto-dispatch by dtype combination (when ``kind='auto'``):

    - categorical target × categorical explanatory (≤ 8 levels) -> stacked bar
    - categorical target × categorical explanatory (> 8 levels) -> mosaic
    - categorical target × continuous explanatory -> grouped violin
    - boolean target × continuous explanatory -> overlaid histograms

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
        Binning for continuous explanatory (passed to
        :func:`pycatdap.target_summary` when relevant).
    ax : Axes or None
        Matplotlib axes; created if ``None``.
    **kwargs
        Forwarded to the underlying matplotlib call.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    from pycatdap._target_pair import target_summary
    from pycatdap.eda import _detect_kind

    if target not in df.columns:
        msg = f"plot_target: target column not found: {target!r}"
        raise KeyError(msg)
    if explanatory not in df.columns:
        msg = f"plot_target: explanatory column not found: {explanatory!r}"
        raise KeyError(msg)

    target_kind = _detect_kind(df[target])
    if target_kind == "continuous":
        msg = (
            f"plot_target: target {target!r} is continuous; "
            f"a categorical or boolean target is required."
        )
        raise ValueError(msg)

    expl_kind = _detect_kind(df[explanatory])
    resolved = _resolve_target_kind(kind, target_kind, expl_kind)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    if resolved in {"stacked", "mosaic"}:
        summary = target_summary(df, target=target, explanatory=explanatory, bins=bins)
        if resolved == "stacked":
            barplot_twoway(summary.counts, ax=ax, **kwargs)
            ax.set_title(f"{target} × {explanatory}")
        else:
            mosaic_plot(summary.counts, ax=ax, **kwargs)
            ax.set_title(f"Mosaic: {target} × {explanatory}")
        return ax

    # Categorical/boolean target × continuous explanatory
    work = df[[target, explanatory]].dropna()
    groups: list[Any] = sorted(work[target].astype(str).unique().tolist())
    data = [
        work.loc[work[target].astype(str) == g, explanatory].to_numpy(dtype=float)
        for g in groups
    ]

    if resolved == "violin":
        ax.violinplot(data, showmeans=True, showmedians=False)
        ax.set_xticks(range(1, len(groups) + 1))
        ax.set_xticklabels(groups)
        ax.set_xlabel(str(target))
        ax.set_ylabel(str(explanatory))
        ax.set_title(f"{explanatory} by {target}")
    elif resolved == "box":
        ax.boxplot(data, tick_labels=groups)
        ax.set_xlabel(str(target))
        ax.set_ylabel(str(explanatory))
        ax.set_title(f"{explanatory} by {target}")
    elif resolved == "hist":
        for label, arr in zip(groups, data, strict=True):
            ax.hist(arr, bins=20, alpha=0.5, label=str(label))
        ax.set_xlabel(str(explanatory))
        ax.set_ylabel("Frequency")
        ax.legend(title=str(target))
        ax.set_title(f"{explanatory} by {target}")
    else:
        msg = f"plot_target: unsupported kind {resolved!r}"
        raise ValueError(msg)

    return ax


def _resolve_target_kind(kind: str, target_kind: str, expl_kind: str) -> str:
    """Map kind='auto' to a concrete kind based on the dtype combination."""
    valid = {"auto", "stacked", "mosaic", "violin", "box", "hist", "grouped_bar"}
    if kind not in valid:
        msg = f"plot_target: kind must be one of {sorted(valid)}; got {kind!r}"
        raise ValueError(msg)
    if kind != "auto":
        return kind
    if expl_kind in {"categorical", "boolean"}:
        return "stacked"
    if expl_kind == "continuous":
        return "violin"
    msg = (
        f"plot_target: cannot auto-dispatch for target_kind={target_kind!r}, "
        f"explanatory_kind={expl_kind!r}; pass an explicit kind."
    )
    raise ValueError(msg)


def plot_missing(
    df: pd.DataFrame,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Bar chart of missing-value counts per column.

    Parameters
    ----------
    df : DataFrame
        Source data.
    ax : Axes or None
        Matplotlib axes. Created if ``None``.
    **kwargs
        Forwarded to :meth:`Axes.bar`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    counts = df.isna().sum().astype(int)
    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    columns = [str(c) for c in counts.index]
    ax.bar(columns, counts.to_numpy(), **kwargs)
    ax.set_xlabel("Variable")
    ax.set_ylabel("Missing count")
    ax.set_title("Missing values per column")
    if len(columns) > 6:
        ax.tick_params(axis="x", rotation=45)
    return ax
