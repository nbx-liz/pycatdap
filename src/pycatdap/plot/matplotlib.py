"""Visualization: mosaic plots, stacked bar charts, AIC comparison plots.

All functions require ``matplotlib``.  An ``ImportError`` with install
instructions is raised if the library is missing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt
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

    from pycatdap._target_pair import _summary_categorical
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
        kind, target_kind, expl_kind, continuous_default="violin"
    )

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    # H-0005: continuous target → regression-mode plotting (Y on y-axis raw).
    if target_kind == "continuous":
        return _plot_target_regression(
            df,
            target=target,
            explanatory=explanatory,
            kind=resolved,
            bins=bins,
            ax=ax,
            **kwargs,
        )

    if resolved in {"stacked", "mosaic"}:
        summary = _summary_categorical(
            df, target=target, explanatory=explanatory, bins=bins
        )
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


def _plot_target_regression(
    df: pd.DataFrame,
    *,
    target: str,
    explanatory: str,
    kind: str,
    bins: int | list[float] | None,
    ax: Axes,
    **kwargs: Any,
) -> Axes:
    """Render a continuous-target plot (H-0005 regression mode).

    ``kind`` values:

    - ``"box"`` / ``"violin"`` — target distribution per categorical X bin
    - ``"scatter"`` — raw scatter of (X, target) with bin-mean overlay for
      a continuous X (boundaries from :func:`target_summary`)
    - ``"bin_means"`` — bar chart of ``target_mean`` per X bin (no scatter)
    - ``"hist"`` — overlaid histograms per binary X
    """
    _import_matplotlib()  # raise if matplotlib missing
    from pycatdap._target_pair import _summary_regression
    from pycatdap.eda import _detect_kind

    expl_kind = _detect_kind(df[explanatory])

    # Drop rows with missing Y for plotting (M2: keep missing X visible as a
    # group; pyplot box treats it as its own category).
    work = df[df[target].notna()][[target, explanatory]]

    if kind in {"box", "violin"}:
        labels: list[str]
        data: list[npt.NDArray[np.float64]]
        if expl_kind == "continuous":
            # For continuous X with box/violin, derive X bins from regression summary.
            summary = _summary_regression(
                work,
                target=target,
                explanatory=explanatory,
                bins=None,
                criterion="bic",
            )
            labels = [str(idx) for idx in summary.bin_stats.index]
            x_arr = work[explanatory].to_numpy(dtype=float)
            y_arr = work[target].to_numpy(dtype=float)
            # Replicate the binning by reconstructing edges from summary
            # intervals (good-enough heuristic for the plot)
            data = []
            if summary.intervals:
                edges = [
                    float(np.nanmin(x_arr)) - 1e-9,
                    *summary.intervals,
                    float(np.nanmax(x_arr)) + 1e-9,
                ]
                cuts = pd.cut(x_arr, bins=edges, include_lowest=True)
                for label in labels:
                    if label == "_missing_":
                        mask = np.isnan(x_arr)
                    else:
                        mask = cuts.astype(str) == label
                    data.append(y_arr[mask])
            else:
                data = [y_arr]
                labels = labels or [str(explanatory)]
        else:
            # Categorical X: group target by X value (including _missing_)
            x_str = (
                work[explanatory]
                .astype(object)
                .where(work[explanatory].notna(), "_missing_")
            )
            x_str = x_str.astype(str)
            labels = sorted(x_str.unique().tolist())
            data = [
                work.loc[x_str == lbl, target].to_numpy(dtype=float) for lbl in labels
            ]

        if kind == "box":
            ax.boxplot(data, tick_labels=labels)
        else:
            ax.violinplot(data, showmeans=True, showmedians=False)
            ax.set_xticks(range(1, len(labels) + 1))
            ax.set_xticklabels(labels)
        ax.set_xlabel(str(explanatory))
        ax.set_ylabel(str(target))
        ax.set_title(f"{target} by {explanatory}")
        if expl_kind == "continuous" and len(labels) > 6:
            ax.tick_params(axis="x", rotation=45)
        return ax

    if kind == "bin_means":
        summary = _summary_regression(
            work,
            target=target,
            explanatory=explanatory,
            bins=bins,
            criterion="bic",
        )
        labels = [str(idx) for idx in summary.bin_stats.index]
        means = summary.bin_stats["target_mean"].to_numpy(dtype=float)
        ax.bar(range(len(labels)), means, **kwargs)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        ax.set_xlabel(str(explanatory))
        ax.set_ylabel(f"mean({target})")
        ax.set_title(f"mean({target}) by {explanatory} (ΔAIC={summary.delta_aic:.2f})")
        if len(labels) > 6:
            ax.tick_params(axis="x", rotation=45)
        return ax

    if kind == "scatter":
        if expl_kind != "continuous":
            msg = "plot_target: kind='scatter' requires a continuous explanatory"
            raise ValueError(msg)
        x = work[explanatory].to_numpy(dtype=float)
        y = work[target].to_numpy(dtype=float)
        # Drop missing X for scatter
        mask = ~np.isnan(x)
        ax.scatter(x[mask], y[mask], alpha=0.4, s=12, **kwargs)
        # Overlay bin means as a step line
        summary = _summary_regression(
            work,
            target=target,
            explanatory=explanatory,
            bins=bins,
            criterion="bic",
        )
        if summary.intervals:
            edges = [
                float(np.nanmin(x)),
                *summary.intervals,
                float(np.nanmax(x)),
            ]
            centers = [(edges[i] + edges[i + 1]) / 2 for i in range(len(edges) - 1)]
            # Exclude _missing_ from the overlay
            bin_means_no_missing = [
                float(v)
                for label, v in summary.bin_stats["target_mean"].items()
                if str(label) != "_missing_"
            ]
            if len(centers) == len(bin_means_no_missing):
                ax.plot(
                    centers,
                    bin_means_no_missing,
                    "o-",
                    color="red",
                    linewidth=2,
                    label="bin mean",
                )
                ax.legend()
        ax.set_xlabel(str(explanatory))
        ax.set_ylabel(str(target))
        ax.set_title(f"{target} vs {explanatory} (ΔAIC={summary.delta_aic:.2f})")
        return ax

    if kind == "hist":
        # Treat X as the (categorical) hue dimension
        x_str = (
            work[explanatory]
            .astype(object)
            .where(work[explanatory].notna(), "_missing_")
        )
        x_str = x_str.astype(str)
        groups_h: list[str] = sorted(x_str.unique().tolist())
        for g in groups_h:
            ax.hist(
                work.loc[x_str == g, target].to_numpy(dtype=float),
                bins=20,
                alpha=0.5,
                label=str(g),
            )
        ax.set_xlabel(str(target))
        ax.set_ylabel("Frequency")
        ax.legend(title=str(explanatory))
        ax.set_title(f"{target} by {explanatory}")
        return ax

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
    ax: Axes | None = None,
    threshold: float | None = 0.0,
    cmap: str = "RdYlGn_r",
    **kwargs: Any,
) -> Axes:
    """Diverging ΔAIC heatmap (H-0006).

    Parameters
    ----------
    result : Catdap1Result or DataFrame
        ΔAIC values. ``Catdap1Result.aic`` is extracted automatically.
        For a raw DataFrame: rows are responses, columns are
        explanatories. Diagonal cells should be ``NaN`` (rendered white).
    ax : Axes or None
        Matplotlib axes. Created if ``None``.
    threshold : float or None
        Mark cells whose ΔAIC is strictly less than ``threshold`` with a
        ``*`` overlay (default ``0.0`` highlights informative cells).
        Pass ``None`` to disable.
    cmap : str
        Diverging colormap name. Default ``'RdYlGn_r'`` paints negative
        (informative) ΔAIC green and positive red, matching Issue #13.
    **kwargs
        Forwarded to :meth:`matplotlib.axes.Axes.imshow`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()
    from matplotlib.colors import TwoSlopeNorm

    aic_df = _coerce_aic_dataframe(result)
    data = aic_df.to_numpy(dtype=float)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    finite = data[np.isfinite(data)]
    if finite.size == 0:
        vmin, vmax = -1.0, 1.0
    else:
        abs_max = float(np.nanmax(np.abs(finite)))
        if abs_max == 0.0:
            abs_max = 1.0
        vmin = -abs_max
        vmax = abs_max
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0.0, vmax=vmax)

    # Pass NaN-containing data directly; rely on the colormap's bad-color
    # handling to render diagonal / undefined cells as transparent.
    # (Avoids np.ma which is untyped in some numpy stub versions.)
    cmap_obj = plt.get_cmap(cmap).copy()
    cmap_obj.set_bad(color="white", alpha=0.0)
    image = ax.imshow(data, cmap=cmap_obj, norm=norm, aspect="auto", **kwargs)

    n_rows, n_cols = data.shape
    ax.set_xticks(range(n_cols))
    ax.set_yticks(range(n_rows))
    ax.set_xticklabels([str(c) for c in aic_df.columns])
    ax.set_yticklabels([str(r) for r in aic_df.index])
    ax.set_xlabel("Explanatory")
    ax.set_ylabel("Response")
    ax.set_title("ΔAIC heatmap")
    if n_cols > 6:
        ax.tick_params(axis="x", rotation=45)

    if threshold is not None:
        for i in range(n_rows):
            for j in range(n_cols):
                value = data[i, j]
                if np.isfinite(value) and value < threshold:
                    ax.text(
                        j,
                        i,
                        "*",
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=10,
                        fontweight="bold",
                    )

    ax.figure.colorbar(image, ax=ax, label="ΔAIC")
    return ax


def _coerce_residuals(table: Any) -> pd.DataFrame:
    """Extract Pearson residuals from a TargetSummary or compute from a crosstab.

    Rejects RegressionTargetSummary (continuous targets have no Pearson
    residual concept) with a pointer to plot_target(kind="scatter").
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
    ax: Axes | None = None,
    threshold: float | None = 2.0,
    cmap: str = "RdBu_r",
    **kwargs: Any,
) -> Axes:
    """vcd-style heatmap of Pearson standardized residuals (H-0006).

    Parameters
    ----------
    table : TargetSummary or DataFrame
        :class:`TargetSummary` (residuals taken from
        ``pearson_residuals``) or a raw two-way contingency table
        (residuals computed internally).
    ax : Axes or None
        Matplotlib axes. Created if ``None``.
    threshold : float or None
        Overlay ``*`` on cells whose ``|residual| > threshold`` (default
        ``2.0``: convention for "strong" association). ``None`` disables.
    cmap : str
        Diverging colormap. Default ``'RdBu_r'`` (blue=negative,
        red=positive), matching vcd ``assoc(shade=TRUE)``.
    **kwargs
        Forwarded to :meth:`matplotlib.axes.Axes.imshow`.

    Returns
    -------
    Axes

    Raises
    ------
    TypeError
        If *table* is a :class:`RegressionTargetSummary` (use
        ``plot_target(kind='scatter')`` instead) or an unsupported type.
    """
    plt = _import_matplotlib()
    from matplotlib.colors import TwoSlopeNorm

    residuals = _coerce_residuals(table)
    data = residuals.to_numpy(dtype=float)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    finite = data[np.isfinite(data)]
    abs_max = float(np.nanmax(np.abs(finite))) if finite.size else 1.0
    if abs_max == 0.0:
        abs_max = 1.0
    norm = TwoSlopeNorm(vmin=-abs_max, vcenter=0.0, vmax=abs_max)

    cmap_obj = plt.get_cmap(cmap).copy()
    cmap_obj.set_bad(color="white", alpha=0.0)
    image = ax.imshow(data, cmap=cmap_obj, norm=norm, aspect="auto", **kwargs)

    n_rows, n_cols = data.shape
    ax.set_xticks(range(n_cols))
    ax.set_yticks(range(n_rows))
    ax.set_xticklabels([str(c) for c in residuals.columns])
    ax.set_yticklabels([str(r) for r in residuals.index])
    ax.set_xlabel(str(residuals.columns.name) if residuals.columns.name else "")
    ax.set_ylabel(str(residuals.index.name) if residuals.index.name else "")
    ax.set_title("Pearson standardized residuals")
    if n_cols > 6:
        ax.tick_params(axis="x", rotation=45)

    if threshold is not None:
        for i in range(n_rows):
            for j in range(n_cols):
                value = data[i, j]
                if np.isfinite(value) and abs(value) > threshold:
                    ax.text(
                        j,
                        i,
                        "*",
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=10,
                        fontweight="bold",
                    )

    ax.figure.colorbar(image, ax=ax, label="Pearson residual")
    return ax


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


# ---------------------------------------------------------------------------
# Phase I (H-0012): confusion matrix visualization
# ---------------------------------------------------------------------------


def _build_confusion_matrix(
    y_true: npt.NDArray[Any],
    y_pred: npt.NDArray[Any],
    labels: list[Any] | None,
    normalize: str | None,
) -> tuple[npt.NDArray[np.float64], list[str]]:
    """Build a normalized confusion matrix shared by both backends.

    Parameters
    ----------
    y_true, y_pred : ndarray
        Aligned ground-truth and predicted labels.
    labels : list or None
        Class order; ``None`` uses sorted unique values from both inputs.
    normalize : {"true", "pred", "all", None}
        Row / column / total normalization, or raw counts.

    Returns
    -------
    matrix : ndarray, shape (N, N)
    label_strs : list[str]
    """
    if labels is None:
        labels = sorted({*np.unique(y_true).tolist(), *np.unique(y_pred).tolist()})
    label_strs = [str(label) for label in labels]
    cross = pd.crosstab(
        pd.Series(y_true, name="y_true"),
        pd.Series(y_pred, name="y_pred"),
        dropna=False,
    ).reindex(index=labels, columns=labels, fill_value=0)
    matrix = cross.to_numpy(dtype=np.float64)

    if normalize == "true":
        row_sums = matrix.sum(axis=1, keepdims=True)
        out = np.zeros_like(matrix)
        with np.errstate(invalid="ignore", divide="ignore"):
            np.divide(matrix, row_sums, out=out, where=row_sums != 0)
        matrix = out
    elif normalize == "pred":
        col_sums = matrix.sum(axis=0, keepdims=True)
        out = np.zeros_like(matrix)
        with np.errstate(invalid="ignore", divide="ignore"):
            np.divide(matrix, col_sums, out=out, where=col_sums != 0)
        matrix = out
    elif normalize == "all":
        total = matrix.sum()
        if total > 0:
            matrix = matrix / total
    elif normalize is not None:
        msg = (
            f"unknown normalize={normalize!r}; expected one of "
            f"'true', 'pred', 'all', None"
        )
        raise ValueError(msg)

    return matrix, label_strs


def plot_confusion(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    labels: list[Any] | None = None,
    normalize: str | None = None,
    ax: Axes | None = None,
    cmap: str = "Blues",
    show_values: bool = True,
    **kwargs: Any,
) -> Axes:
    """Confusion matrix heatmap (H-0012 Phase I, matplotlib backend).

    Multi-class capable (N×N grid for any N).

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted labels.
    labels : list or None
        Class order. ``None`` uses sorted unique values.
    normalize : {"true", "pred", "all", None}
        Row / column / total normalization, or raw counts.
    ax : Axes or None
        Matplotlib axes. Created if ``None``.
    cmap : str
        Matplotlib colormap. Default ``"Blues"`` mirrors sklearn convention.
    show_values : bool
        Annotate each cell with its numeric value.
    **kwargs
        Forwarded to :meth:`Axes.imshow`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    matrix, label_strs = _build_confusion_matrix(
        y_true_arr, y_pred_arr, labels, normalize
    )

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    image = ax.imshow(matrix, cmap=cmap, aspect="auto", **kwargs)

    n = len(label_strs)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(label_strs)
    ax.set_yticklabels(label_strs)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    title_suffix = " (normalized)" if normalize else ""
    ax.set_title(f"Confusion matrix{title_suffix}")
    if n > 6:
        ax.tick_params(axis="x", rotation=45)

    if show_values:
        if normalize:
            threshold = matrix[np.isfinite(matrix)].max() / 2.0 if matrix.size else 0.5
            fmt = ".2f"
        else:
            threshold = matrix.max() / 2.0 if matrix.size else 0.0
            fmt = ".0f"
        for i in range(n):
            for j in range(n):
                value = matrix[i, j]
                if not np.isfinite(value):
                    continue
                color = "white" if value > threshold else "black"
                ax.text(
                    j,
                    i,
                    format(value, fmt),
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=9,
                )

    ax.figure.colorbar(image, ax=ax, label="proportion" if normalize else "count")
    return ax


def plot_confusion_by_slice(
    df: pd.DataFrame,
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    var: str,
    *,
    labels: list[Any] | None = None,
    n_cols: int = 3,
    normalize: str | None = "true",
    cmap: str = "Blues",
    **kwargs: Any,  # noqa: ARG001
) -> Figure:
    """Per-category small-multiples of confusion matrices (H-0012 Phase I).

    Multi-panel grid: one confusion matrix per category of ``var``.

    Returns ``matplotlib.figure.Figure`` (intentional exception to the
    Axes convention — see H-0012 §F-bis). Does NOT accept ``ax=``.

    Parameters
    ----------
    df : DataFrame
        Source frame. Must have ``len(df) == len(y_true) == len(y_pred)``.
    y_true, y_pred : array-like
        Labels aligned to ``df``.
    var : str
        Column in ``df`` to slice on. Continuous numeric columns must be
        pre-binned (the function does not auto-bin; see Phase J's
        ``residual_by_category`` for a continuous-aware analogue).
    labels : list or None
        Class order shared across panels.
    n_cols : int
        Grid column count.
    normalize : {"true", "pred", "all", None}
        Per-panel normalization; default ``"true"`` (row-normalized).
    cmap : str
        Matplotlib colormap.

    Returns
    -------
    matplotlib.figure.Figure
    """
    plt = _import_matplotlib()

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

    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), squeeze=False
    )

    for idx, category in enumerate(categories):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row][col]
        mask = (df[var] == category).to_numpy()
        plot_confusion(
            y_true_arr[mask],
            y_pred_arr[mask],
            labels=labels,
            normalize=normalize,
            ax=ax,
            cmap=cmap,
        )
        ax.set_title(f"{var} = {category}")

    # Hide unused axes
    for idx in range(n_panels, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row][col].axis("off")

    fig.tight_layout()
    return fig  # type: ignore[no-any-return]
