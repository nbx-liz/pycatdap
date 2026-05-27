"""pycatdap.plot — visualization with selectable backend.

This package provides the canonical pycatdap visualization API (v0.3+).
Two backends are supported:

- ``matplotlib`` (default) — static figures, compatible with notebooks and scripts
- ``plotly`` — interactive figures, ideal for LizyStudio and standalone HTML

Usage
-----

Top-level dispatchers select the backend via the ``backend`` keyword:

>>> from pycatdap.plot import mosaic_plot
>>> ax = mosaic_plot(table, backend="matplotlib")
>>> fig = mosaic_plot(table, backend="plotly")

Or import directly from a backend submodule:

>>> from pycatdap.plot.matplotlib import mosaic_plot
>>> ax = mosaic_plot(table)

Backward compatibility
----------------------

The legacy v0.2 import path ``pycatdap.plotting`` continues to work and
delegates to ``pycatdap.plot.matplotlib``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import pandas as pd

    from pycatdap.catdap1 import Catdap1Result
    from pycatdap.catdap2 import Catdap2Result

Backend = Literal["matplotlib", "plotly"]


def _get_backend_module(backend: Backend) -> Any:
    """Resolve the backend submodule, raising a clear error for unknown names."""
    if backend == "matplotlib":
        from pycatdap.plot import matplotlib as _mpl

        return _mpl
    if backend == "plotly":
        from pycatdap.plot import plotly as _plotly

        return _plotly
    msg = f"Unknown plot backend: {backend!r}. Use 'matplotlib' (default) or 'plotly'."
    raise ValueError(msg)


def aic_comparison_plot(
    result: Catdap1Result | Catdap2Result,
    response: str | None = None,
    *,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Horizontal bar chart of ΔAIC values per explanatory variable.

    Parameters
    ----------
    result : Catdap1Result or Catdap2Result
        Analysis result.
    response : str or None
        Response variable name (required for Catdap1Result with multiple
        responses; ignored for Catdap2Result).
    backend : {'matplotlib', 'plotly'}
        Plotting backend. Default 'matplotlib'.
    **kwargs
        Additional keyword arguments forwarded to the chosen backend's
        implementation.

    Returns
    -------
    object
        - matplotlib backend: ``matplotlib.axes.Axes``
        - plotly backend: ``plotly.graph_objs.Figure``
    """
    return _get_backend_module(backend).aic_comparison_plot(
        result, response=response, **kwargs
    )


def barplot_twoway(
    table: pd.DataFrame,
    *,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Stacked proportional bar chart for a two-way frequency table.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Additional keyword arguments forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.
    """
    return _get_backend_module(backend).barplot_twoway(table, **kwargs)


def mosaic_plot(
    table: pd.DataFrame,
    *,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Mosaic plot for a two-way frequency table.

    Parameters
    ----------
    table : DataFrame
        Cross-frequency table.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Additional keyword arguments forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.
    """
    return _get_backend_module(backend).mosaic_plot(table, **kwargs)


def plot_variable(
    df: pd.DataFrame,
    col: str,
    kind: str = "auto",
    *,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Plot a single variable: histogram for continuous, bar for categorical.

    Parameters
    ----------
    df : DataFrame
        Source data.
    col : str
        Column name.
    kind : {'auto', 'hist', 'bar'}
        ``'auto'`` (default) infers from dtype.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.
    """
    return _get_backend_module(backend).plot_variable(df, col, kind=kind, **kwargs)


_VALID_TARGET_KINDS: frozenset[str] = frozenset(
    {"auto", "stacked", "mosaic", "violin", "box", "hist", "scatter", "bin_means"}
)


def _resolve_target_kind(
    kind: str,
    target_kind: str,
    expl_kind: str,
    *,
    continuous_default: str,
) -> str:
    """Resolve ``kind='auto'`` to a concrete kind based on dtype combination.

    Shared between matplotlib and plotly backends. The two backends differ
    only on ``continuous_default`` for the categorical-target case
    (matplotlib prefers ``violin``, plotly prefers ``box``).

    For continuous targets (H-0005 regression mode), the dispatch is:

    - continuous target × categorical / boolean explanatory -> ``box``
    - continuous target × continuous explanatory          -> ``scatter``
    """
    if kind not in _VALID_TARGET_KINDS:
        msg = (
            f"plot_target: kind must be one of {sorted(_VALID_TARGET_KINDS)}; "
            f"got {kind!r}"
        )
        raise ValueError(msg)
    if kind != "auto":
        return kind
    if target_kind == "continuous":
        if expl_kind in {"categorical", "boolean"}:
            return "box"
        if expl_kind == "continuous":
            return "scatter"
        msg = (
            f"plot_target: cannot auto-dispatch for target_kind='continuous', "
            f"explanatory_kind={expl_kind!r}; pass an explicit kind."
        )
        raise ValueError(msg)
    if expl_kind in {"categorical", "boolean"}:
        return "stacked"
    if expl_kind == "continuous":
        return continuous_default
    msg = (
        f"plot_target: cannot auto-dispatch for target_kind={target_kind!r}, "
        f"explanatory_kind={expl_kind!r}; pass an explicit kind."
    )
    raise ValueError(msg)


def plot_target(
    df: pd.DataFrame,
    target: str,
    explanatory: str,
    *,
    kind: str = "auto",
    bins: int | list[float] | None = None,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Plot a target × explanatory relationship (H-0004).

    Auto-dispatch (``kind='auto'``):

    - categorical target × categorical explanatory -> stacked bar / mosaic
    - categorical/boolean target × continuous explanatory -> violin (mpl) / box (plotly)

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
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.

    See Also
    --------
    pycatdap.target_summary : underlying cross-tabulation with proportions
        and Pearson residuals.
    """
    return _get_backend_module(backend).plot_target(
        df, target=target, explanatory=explanatory, kind=kind, bins=bins, **kwargs
    )


def _resolve_pair_response(
    df: pd.DataFrame,
    x: str,
    y: str,
) -> tuple[str, str]:
    """Decide which of (x, y) is the response (target) side (H-0006).

    Returns ``(target, explanatory)``. Rule:

    - Both discrete (categorical / boolean / datetime / other) → ``y`` wins
      (seaborn / vcd ``y ~ x`` convention).
    - Mixed discrete/continuous → discrete side wins (Pearson residual
      interpretation is more natural with the discrete side as response).
    - Both continuous → ``y`` wins (H-0005 regression: ``y`` is target).
    """
    from pycatdap.eda import _detect_kind

    if x not in df.columns:
        msg = f"plot_pair: x column not found: {x!r}"
        raise KeyError(msg)
    if y not in df.columns:
        msg = f"plot_pair: y column not found: {y!r}"
        raise KeyError(msg)

    kind_x = _detect_kind(df[x])
    kind_y = _detect_kind(df[y])

    x_is_continuous = kind_x == "continuous"
    y_is_continuous = kind_y == "continuous"

    if x_is_continuous and not y_is_continuous:
        return y, x
    if y_is_continuous and not x_is_continuous:
        return x, y
    return y, x


def plot_pair(
    df: pd.DataFrame,
    x: str,
    y: str,
    *,
    kind: str = "auto",
    bins: int | list[float] | None = None,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Plot a symmetric x × y pair (H-0006 Phase B).

    Decides which side is the response based on dtypes, then delegates
    to :func:`plot_target`. The decision rule (H-0006):

    - discrete × discrete → ``y`` is the response
    - discrete × continuous → discrete side is the response
    - continuous × continuous → ``y`` is the response (H-0005 regression
      mode; scatter plot)

    Parameters
    ----------
    df : DataFrame
        Source data.
    x, y : str
        The two variables to compare.
    kind : str
        Plot kind, forwarded to :func:`plot_target`. Default ``'auto'``.
    bins : int, sequence of float, or None
        Binning for continuous variables, forwarded to :func:`plot_target`.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Additional keyword arguments forwarded to :func:`plot_target`.

    Returns
    -------
    object
        Backend-specific figure/axes object (whatever :func:`plot_target`
        returns).

    See Also
    --------
    pycatdap.plot_target : the underlying target-aware dispatcher.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> ax = pycatdap.plot_pair(df, "Sex", "Survived")
    """
    target, explanatory = _resolve_pair_response(df, x, y)
    return plot_target(
        df,
        target=target,
        explanatory=explanatory,
        kind=kind,
        bins=bins,
        backend=backend,
        **kwargs,
    )


def aic_heatmap(
    result: Catdap1Result | pd.DataFrame,
    *,
    threshold: float | None = 0.0,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Diverging ΔAIC heatmap (H-0006).

    Parameters
    ----------
    result : Catdap1Result or DataFrame
        ΔAIC values. ``Catdap1Result.aic`` is extracted automatically.
        For a raw DataFrame, rows are responses and columns are
        explanatories. Diagonal cells are typically ``NaN``.
    threshold : float or None
        Annotate cells with ΔAIC strictly less than ``threshold`` (default
        ``0.0``: highlight informative cells). Pass ``None`` to disable.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.

    See Also
    --------
    pycatdap.association_matrix : build the m × m ΔAIC matrix to feed in.
    pycatdap.catdap1 : produces a ``Catdap1Result`` whose ``.aic`` is the
        natural input for this function.
    """
    return _get_backend_module(backend).aic_heatmap(
        result, threshold=threshold, **kwargs
    )


def association_plot(
    table: Any,
    *,
    threshold: float | None = 2.0,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """vcd-style heatmap of Pearson standardized residuals (H-0006).

    Parameters
    ----------
    table : TargetSummary or DataFrame
        :class:`pycatdap.TargetSummary` (residuals from
        ``pearson_residuals``) or a raw two-way contingency table
        (residuals computed internally as ``(obs - exp) / sqrt(exp)``).
    threshold : float or None
        Annotate cells where ``|residual| > threshold`` with a ``*``
        overlay (default ``2.0``: conventional "strong" association
        cutoff). Pass ``None`` to disable.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.

    Raises
    ------
    TypeError
        If *table* is a :class:`pycatdap.RegressionTargetSummary` (Pearson
        residuals are undefined for a continuous target; use
        :func:`pycatdap.plot_target` with ``kind="scatter"``) or an
        unsupported input type.

    See Also
    --------
    pycatdap.target_summary : computes ``pearson_residuals`` to feed in.
    """
    return _get_backend_module(backend).association_plot(
        table, threshold=threshold, **kwargs
    )


def plot_missing(
    df: pd.DataFrame,
    *,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Bar chart of missing-value counts per column.

    Parameters
    ----------
    df : DataFrame
        Source data.
    backend : {'matplotlib', 'plotly'}
        Plotting backend.
    **kwargs
        Forwarded to the chosen backend.

    Returns
    -------
    object
        Backend-specific figure/axes object.
    """
    return _get_backend_module(backend).plot_missing(df, **kwargs)


__all__ = [
    "Backend",
    "aic_comparison_plot",
    "aic_heatmap",
    "association_plot",
    "barplot_twoway",
    "mosaic_plot",
    "plot_missing",
    "plot_pair",
    "plot_target",
    "plot_variable",
    "_resolve_pair_response",
    "_resolve_target_kind",
]
