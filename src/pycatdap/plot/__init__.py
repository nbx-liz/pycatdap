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
    "barplot_twoway",
    "mosaic_plot",
    "plot_missing",
    "plot_target",
    "plot_variable",
]
