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
    from pycatdap.error.calibration import Strategy


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


# ---------------------------------------------------------------------------
# Phase J (H-0012): regression residual visualization
# ---------------------------------------------------------------------------


def _residual_values(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Compute aligned (y_true_f, y_pred_f, residual) float arrays."""
    yt = np.asarray(y_true, dtype=np.float64)
    yp = np.asarray(y_pred, dtype=np.float64)
    if yt.shape[0] != yp.shape[0]:
        msg = (
            f"y_true and y_pred must have the same length "
            f"(got {yt.shape[0]} and {yp.shape[0]})"
        )
        raise ValueError(msg)
    return yt, yp, yt - yp


def residual_plot(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    kind: str = "scatter_pred_resid",
    color_by: pd.Series | npt.NDArray[Any] | None = None,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Residual diagnostic plot (H-0012 Phase J, matplotlib backend).

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned regression targets and predictions.
    kind : {"scatter_pred_resid", "scatter_true_pred", "histogram"}
        - ``"scatter_pred_resid"`` (default): residual vs y_pred scatter
          with a zero reference line.
        - ``"scatter_true_pred"``: y_pred vs y_true scatter with a
          y = x identity line.
        - ``"histogram"``: residual histogram.
    color_by : array-like or None
        Optional third variable used to colour the scatter points.
        Ignored when ``kind == "histogram"``.
    ax : Axes or None
        Matplotlib axes; created if ``None``.
    **kwargs
        Forwarded to the underlying matplotlib call.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()

    yt, yp, residual = _residual_values(y_true, y_pred)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    color_arr: npt.NDArray[Any] | None = None
    if color_by is not None:
        color_arr = np.asarray(color_by)
        if color_arr.shape[0] != yt.shape[0]:
            msg = (
                f"color_by length ({color_arr.shape[0]}) does not match "
                f"y_true / y_pred length ({yt.shape[0]})"
            )
            raise ValueError(msg)

    if kind == "scatter_pred_resid":
        if color_arr is not None and color_arr.dtype.kind in "fiub":
            scatter = ax.scatter(yp, residual, c=color_arr, **kwargs)
            ax.figure.colorbar(scatter, ax=ax)
        else:
            ax.scatter(yp, residual, **kwargs)
        ax.axhline(0, color="black", linewidth=1)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Residual (y_true − y_pred)")
        ax.set_title("Residuals vs predictions")
    elif kind == "scatter_true_pred":
        ax.scatter(yt, yp, **kwargs)
        lo = float(min(yt.min(), yp.min()))
        hi = float(max(yt.max(), yp.max()))
        ax.plot([lo, hi], [lo, hi], color="black", linewidth=1)
        ax.set_xlabel("True")
        ax.set_ylabel("Predicted")
        ax.set_title("Predictions vs truth")
    elif kind == "histogram":
        ax.hist(residual, bins=kwargs.pop("bins", 30), **kwargs)
        ax.axvline(0, color="black", linewidth=1)
        ax.set_xlabel("Residual (y_true − y_pred)")
        ax.set_ylabel("Count")
        ax.set_title("Residual histogram")
    else:
        msg = (
            f"unknown kind={kind!r}; expected one of "
            f"'scatter_pred_resid', 'scatter_true_pred', 'histogram'"
        )
        raise ValueError(msg)

    return ax


def _ordered_categories(values: pd.Series) -> list[Any]:
    """Sort unique non-NA categories, preserving Categorical ordering."""
    if isinstance(values.dtype, pd.CategoricalDtype):
        return [c for c in values.cat.categories if c in values.unique()]
    return sorted(values.dropna().unique().tolist(), key=str)


def residual_by_category(
    df: pd.DataFrame,
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    var: str,
    *,
    bins: int | None = None,
    ax: Axes | None = None,
    **kwargs: Any,  # noqa: ARG001
) -> Axes:
    """Box plot of residuals stratified by a categorical variable.

    Continuous ``var`` is auto-binned via :func:`pycatdap._pooling.optimal_binning`
    (AIC-driven) when ``bins=None``. Pass ``bins=int`` for equal-width binning.

    Returns ``Axes`` (single panel). Categorical or pre-binned ``var``
    yields one box per category, ordered alphabetically (Categorical
    dtype preserves declared order).
    """
    plt = _import_matplotlib()

    if var not in df.columns:
        msg = f"residual_by_category: var={var!r} not in df.columns"
        raise KeyError(msg)
    yt, yp, residual = _residual_values(y_true, y_pred)
    if len(yt) != len(df):
        msg = f"y_true / y_pred length ({len(yt)}) does not match len(df) ({len(df)})"
        raise ValueError(msg)

    series = df[var]
    is_continuous = pd.api.types.is_numeric_dtype(series) and not isinstance(
        series.dtype, pd.CategoricalDtype
    )
    if is_continuous:
        from pycatdap._pooling import optimal_binning

        values = series.to_numpy(dtype=np.float64)
        mask = np.isfinite(values)
        if not mask.any():
            msg = f"residual_by_category: var={var!r} has no finite values"
            raise ValueError(msg)
        if bins is None:
            # AIC-optimal binning using residual sign as a proxy response.
            response = np.where(residual >= 0, "pos", "neg").astype(object)
            pooling = optimal_binning(values[mask], response[mask])
            codes_masked = pooling.codes
            edges = list(pooling.boundaries)
            codes = np.full_like(values, fill_value=-1, dtype=np.intp)
            codes[mask] = codes_masked
            categories_str = _bin_labels_from_edges(values[mask], edges)
        else:
            categories_str, codes = _equal_width_bin_labels(values, mask, int(bins))
        categories = list(range(len(categories_str)))
        valid = codes >= 0
        group_data = [residual[valid & (codes == k)] for k in categories]
        group_labels = categories_str
    else:
        cats = _ordered_categories(series)
        if not cats:
            msg = f"residual_by_category: var={var!r} has no non-NA categories"
            raise ValueError(msg)
        group_data = [residual[(series == c).to_numpy()] for c in cats]
        group_labels = [str(c) for c in cats]

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    # Matplotlib 3.9+ uses `tick_labels=` and `orientation=`; pass via a
    # version-tolerant kwarg dict so we don't trip new deprecations.
    ax.boxplot(group_data, tick_labels=group_labels)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xlabel(var)
    ax.set_ylabel("Residual (y_true − y_pred)")
    ax.set_title(f"Residuals by {var}")
    if len(group_labels) > 6:
        ax.tick_params(axis="x", rotation=45)
    return ax


def _equal_width_bin_labels(
    values: npt.NDArray[np.float64],
    mask: npt.NDArray[np.bool_],
    n_bins: int,
) -> tuple[list[str], npt.NDArray[np.intp]]:
    """Equal-width binning with closed-on-left intervals."""
    finite = values[mask]
    if finite.size == 0:
        return [], np.full_like(values, -1, dtype=np.intp)
    lo, hi = float(finite.min()), float(finite.max())
    if lo == hi:
        labels = [f"[{lo:.3g}]"]
        codes = np.full_like(values, -1, dtype=np.intp)
        codes[mask] = 0
        return labels, codes
    edges = np.linspace(lo, hi, n_bins + 1)
    codes = np.full_like(values, -1, dtype=np.intp)
    codes[mask] = np.clip(np.digitize(values[mask], edges[1:-1]), 0, n_bins - 1).astype(
        np.intp
    )
    labels = [f"[{edges[i]:.2f}, {edges[i + 1]:.2f})" for i in range(n_bins)]
    return labels, codes


def _bin_labels_from_edges(
    values: npt.NDArray[np.float64],
    boundaries: list[float],
) -> list[str]:
    """Format AIC-pool boundaries as half-open interval labels."""
    if not boundaries:
        lo, hi = float(values.min()), float(values.max())
        return [f"[{lo:.2f}, {hi:.2f}]"]
    edges = [float(values.min()), *boundaries, float(values.max())]
    return [f"[{edges[i]:.2f}, {edges[i + 1]:.2f})" for i in range(len(edges) - 1)]


def residual_pool_plot(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    n_bins: int = 4,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Visualise the AIC pooling boundaries of |residual| (H-0012 Phase J).

    Plots an absolute-residual histogram with vertical lines at the
    AIC-pooled bin boundaries derived from
    :func:`pycatdap.error.residual_label` (``method="aic_pool"``).
    """
    plt = _import_matplotlib()
    from pycatdap.error._labels import _residual_label_aic_pool

    _, _, residual = _residual_values(y_true, y_pred)
    abs_resid = np.abs(residual)

    pooled = _residual_label_aic_pool(abs_resid, n_bins=n_bins)
    bin_counts = pooled.value_counts().reindex(pooled.cat.categories, fill_value=0)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    ax.hist(abs_resid, bins=kwargs.pop("bins", 30), color="#bcd2e8", **kwargs)

    # Draw vertical lines at the boundaries between consecutive AIC bins
    # by walking each unique bin label in order.
    sorted_resid = np.sort(abs_resid)
    bin_codes = pooled.cat.codes.to_numpy()[np.argsort(abs_resid)]
    for k in range(1, len(bin_counts)):
        switch = np.where(bin_codes == k)[0]
        if switch.size == 0:
            continue
        boundary = float(sorted_resid[switch[0]])
        ax.axvline(boundary, color="#cf222e", linewidth=1.2, linestyle="--")

    ax.set_xlabel("|residual|")
    ax.set_ylabel("Count")
    ax.set_title(f"AIC-pooled |residual| bins ({len(bin_counts)} bins)")
    return ax


# ---------------------------------------------------------------------------
# Phase K (H-0013): calibration reliability diagram
# ---------------------------------------------------------------------------


def calibration_curve(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: str = "aic",
    n_bins: int = 10,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Reliability diagram (H-0013 Phase K, matplotlib backend).

    Plots observed positive-rate vs mean predicted probability per bin, with a
    ``y = x`` perfect-calibration reference and Wilson 95% CI error bars. See
    :func:`pycatdap.error.calibration_curve` for the parameter contract and
    binning strategies.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()
    from pycatdap.error.calibration import _calibration_table

    table = _calibration_table(y_true, y_proba, strategy=strategy, n_bins=n_bins)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    ax.plot(
        [0.0, 1.0],
        [0.0, 1.0],
        linestyle="--",
        color="black",
        linewidth=1,
        label="perfect",
    )

    if not table.empty:
        pred = table["prob_pred"].to_numpy(dtype=np.float64)
        obs = table["prob_true"].to_numpy(dtype=np.float64)
        lower = np.clip(obs - table["ci_low"].to_numpy(dtype=np.float64), 0.0, None)
        upper = np.clip(table["ci_high"].to_numpy(dtype=np.float64) - obs, 0.0, None)
        # Defaults are overridable by caller kwargs (merge, not collide) so
        # passing e.g. color= / label= / markersize= does not raise TypeError.
        errorbar_kwargs: dict[str, Any] = {
            "fmt": "o-",
            "capsize": 3,
            "color": "#1f77b4",
            "label": "model",
        }
        errorbar_kwargs.update(kwargs)
        ax.errorbar(pred, obs, yerr=np.vstack([lower, upper]), **errorbar_kwargs)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed frequency")
    ax.set_title(f"Reliability diagram ({strategy})")
    ax.legend(loc="best")
    return ax


def regression_calibration_curve(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    n_quantiles: int = 10,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Regression calibration diagram (H-0015 PR-M3, matplotlib backend).

    Plots per-band ``pred_mean`` vs ``actual_mean`` with a ``y = x`` reference
    spanning the data range (not clamped to ``[0, 1]``) and a normal CI on the
    outcome mean. See :func:`pycatdap.error.regression_calibration_curve`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()
    from pycatdap.error.calibration import regression_calibration_table

    table = regression_calibration_table(y_true, y_pred, n_quantiles=n_quantiles)

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    if not table.empty:
        pred = table["pred_mean"].to_numpy(dtype=np.float64)
        obs = table["actual_mean"].to_numpy(dtype=np.float64)
        lower = np.clip(obs - table["ci_low"].to_numpy(dtype=np.float64), 0.0, None)
        upper = np.clip(table["ci_high"].to_numpy(dtype=np.float64) - obs, 0.0, None)
        lo = float(min(pred.min(), obs.min()))
        hi = float(max(pred.max(), obs.max()))
        if hi - lo < 1e-12:
            # Degenerate (constant predictor): expand so the y=x reference and
            # the single data point remain visible instead of collapsing to a dot.
            margin = max(abs(lo) * 0.05, 1e-6)
            lo, hi = lo - margin, hi + margin
        ax.plot(
            [lo, hi],
            [lo, hi],
            linestyle="--",
            color="black",
            linewidth=1,
            label="perfect",
        )
        errorbar_kwargs: dict[str, Any] = {
            "fmt": "o-",
            "capsize": 3,
            "color": "#1f77b4",
            "label": "model",
        }
        errorbar_kwargs.update(kwargs)
        ax.errorbar(pred, obs, yerr=np.vstack([lower, upper]), **errorbar_kwargs)

    ax.set_xlabel("Mean predicted value")
    ax.set_ylabel("Mean actual value")
    ax.set_title("Regression calibration")
    ax.legend(loc="best")
    return ax


def multiclass_calibration_curve(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    classes: list[Any] | None = None,
    strategy: Strategy = "aic",
    n_bins: int = 10,
    ax: Axes | None = None,
    **kwargs: Any,
) -> Axes:
    """Multi-class one-vs-rest reliability diagram (H-0015 PR-M3, matplotlib).

    Overlays one reliability curve per class on a shared ``[0, 1]`` square
    with a single ``y = x`` reference. See
    :func:`pycatdap.error.multiclass_calibration_curve`.

    Returns
    -------
    Axes
    """
    plt = _import_matplotlib()
    from pycatdap.error.calibration import multiclass_calibration_table

    tables = multiclass_calibration_table(
        y_true, y_proba, classes=classes, strategy=strategy, n_bins=n_bins
    )

    if ax is None:
        _fig: Figure
        _fig, ax = plt.subplots()

    ax.plot(
        [0.0, 1.0],
        [0.0, 1.0],
        linestyle="--",
        color="black",
        linewidth=1,
        label="perfect",
    )

    line_kwargs: dict[str, Any] = {"marker": "o", "linestyle": "-"}
    line_kwargs.update(kwargs)
    line_kwargs.pop("label", None)
    for cls, table in tables.items():
        if table.empty:
            continue
        pred = table["prob_pred"].to_numpy(dtype=np.float64)
        obs = table["prob_true"].to_numpy(dtype=np.float64)
        ax.plot(pred, obs, label=f"class {cls}", **line_kwargs)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed frequency")
    ax.set_title("Multi-class calibration (one-vs-rest)")
    ax.legend(loc="best")
    return ax
