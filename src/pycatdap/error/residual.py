"""Phase J residual visualization dispatchers (H-0012 PR-H2).

Public API entries:

- :func:`residual_plot` — residual vs predicted scatter / y_pred vs y_true /
  residual histogram
- :func:`residual_by_category` — box plot of residuals stratified by a
  categorical or continuous variable (AIC-binned)
- :func:`residual_pool_plot` — AIC-pooled ``|residual|`` histogram with
  boundary lines

Backend dispatch mirrors :mod:`pycatdap.plot` — pass ``backend="matplotlib"``
or ``backend="plotly"``.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy.typing as npt
import pandas as pd

from pycatdap.error._backend import Backend
from pycatdap.error._backend import get_backend_module as _get_backend_module

ResidualKind = Literal["scatter_pred_resid", "scatter_true_pred", "histogram"]


def residual_plot(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    kind: ResidualKind = "scatter_pred_resid",
    color_by: pd.Series | npt.NDArray[Any] | None = None,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Residual diagnostic plot (H-0012 Phase J).

    Three styles via ``kind=``:

    - ``"scatter_pred_resid"`` (default): residual vs predicted scatter,
      with a zero reference line. The canonical "is the model biased?"
      view.
    - ``"scatter_true_pred"``: predicted vs true scatter with a y = x
      identity line. The canonical "how well do predictions track
      truth?" view.
    - ``"histogram"``: residual distribution, centered on zero.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned regression targets and predictions.
    kind : {"scatter_pred_resid", "scatter_true_pred", "histogram"}
        Plot style.
    color_by : array-like or None
        Optional third variable used to colour scatter points (ignored
        when ``kind == "histogram"``). For numeric inputs a continuous
        colour scale is used.
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Backend-specific keyword arguments (e.g. ``ax=`` for matplotlib).

    Returns
    -------
    matplotlib.axes.Axes | plotly.graph_objects.Figure
    """
    return _get_backend_module(backend).residual_plot(
        y_true, y_pred, kind=kind, color_by=color_by, **kwargs
    )


def residual_by_category(
    df: pd.DataFrame,
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    var: str,
    *,
    bins: int | None = None,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Box plot of residuals stratified by ``var`` (H-0012 Phase J).

    When ``var`` is continuous numeric:

    - ``bins=None`` (default) → AIC-optimal binning via
      :func:`pycatdap._pooling.optimal_binning`, using the residual sign
      as the proxy response (one boundary per AIC-favoured split).
    - ``bins=int`` → equal-width binning over the variable's range.

    Categorical / Categorical-dtype ``var`` is used as-is with the
    declared category order honoured.

    Parameters
    ----------
    df : DataFrame
        Source frame. ``len(df)`` must equal ``len(y_true) == len(y_pred)``.
    y_true, y_pred : array-like
        Aligned regression targets and predictions.
    var : str
        Column in ``df`` to stratify by.
    bins : int or None
        Continuous-variable binning strategy (see above). Ignored for
        categorical ``var``.
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Backend-specific keyword arguments (e.g. ``ax=``).

    Returns
    -------
    matplotlib.axes.Axes | plotly.graph_objects.Figure
    """
    return _get_backend_module(backend).residual_by_category(
        df, y_true, y_pred, var, bins=bins, **kwargs
    )


def residual_pool_plot(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    n_bins: int = 4,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """AIC-pooled |residual| histogram with boundary overlay (H-0012 Phase J).

    Reuses :func:`pycatdap.error.residual_label`'s ``method="aic_pool"``
    pipeline to derive the bin boundaries, then renders an absolute-
    residual histogram with vertical dashed lines at each boundary. The
    final bin count after AIC merging may be smaller than ``n_bins``.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned regression targets and predictions.
    n_bins : int
        Initial quantile bin count fed into the AIC pooling stage.
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Backend-specific keyword arguments (e.g. ``ax=``).

    Returns
    -------
    matplotlib.axes.Axes | plotly.graph_objects.Figure
    """
    return _get_backend_module(backend).residual_pool_plot(
        y_true, y_pred, n_bins=n_bins, **kwargs
    )


__all__ = ["residual_by_category", "residual_plot", "residual_pool_plot"]
