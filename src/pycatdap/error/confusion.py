"""Phase I confusion visualization + AIC dispatchers (H-0012 PR-H1).

Public API entries:

- :func:`plot_confusion` — single confusion-matrix heatmap, multi-class capable
- :func:`plot_confusion_by_slice` — small-multiples grid of confusion matrices,
  one per category of a slicing variable
- :func:`confusion_aic` — pycatdap ΔAIC of the predictions against the true
  labels (negative when informative; see H-0012 §F)

Backend dispatch mirrors :mod:`pycatdap.plot` — pass ``backend="matplotlib"``
or ``backend="plotly"``.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap.error._backend import Backend
from pycatdap.error._backend import get_backend_module as _get_backend_module

NormalizeMode = Literal["true", "pred", "all"] | None


def plot_confusion(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    *,
    labels: list[Any] | None = None,
    normalize: NormalizeMode = None,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Confusion matrix heatmap (H-0012 Phase I).

    Multi-class capable: any N×N matrix renders. For binary tasks this is
    the standard 2×2 confusion display; for multi-class it mirrors
    sklearn's ``ConfusionMatrixDisplay`` layout.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted labels.
    labels : list or None
        Class order. ``None`` uses sorted unique values from both inputs.
    normalize : {"true", "pred", "all", None}
        Per-row / per-column / total normalization, or raw counts.
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Backend-specific keyword arguments (e.g. ``ax``, ``cmap``,
        ``colorscale``, ``show_values``).

    Returns
    -------
    matplotlib.axes.Axes | plotly.graph_objects.Figure
        Backend-specific figure object.
    """
    return _get_backend_module(backend).plot_confusion(
        y_true, y_pred, labels=labels, normalize=normalize, **kwargs
    )


def plot_confusion_by_slice(
    df: pd.DataFrame,
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
    var: str,
    *,
    labels: list[Any] | None = None,
    n_cols: int = 3,
    normalize: NormalizeMode = "true",
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Per-category small-multiples of confusion matrices (H-0012 Phase I).

    Returns ``matplotlib.figure.Figure`` (matplotlib) or
    ``plotly.graph_objects.Figure`` (plotly). The matplotlib path is an
    **intentional exception** to the project-wide ``Axes`` rule (multi-
    panel grid; see H-0012 §F-bis).

    Parameters
    ----------
    df : DataFrame
        Source frame. ``len(df)`` must equal ``len(y_true) == len(y_pred)``.
    y_true, y_pred : array-like
        Aligned labels.
    var : str
        Column in ``df`` to slice by. Continuous numeric columns must be
        pre-binned by the caller.
    labels : list or None
        Class order shared across panels.
    n_cols : int
        Grid column count.
    normalize : {"true", "pred", "all", None}
        Per-panel normalization (default ``"true"``).
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Backend-specific keyword arguments.

    Returns
    -------
    matplotlib.figure.Figure | plotly.graph_objects.Figure
    """
    return _get_backend_module(backend).plot_confusion_by_slice(
        df,
        y_true,
        y_pred,
        var,
        labels=labels,
        n_cols=n_cols,
        normalize=normalize,
        **kwargs,
    )


def confusion_aic(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
) -> float:
    """ΔAIC of the predictions against the true labels (H-0012 Phase I).

    Implements the sign convention of pycatdap's existing
    :func:`pycatdap._aic.compute_delta_aic`:

    .. math::

        \\Delta AIC = AIC(y_{true} \\sim y_{pred}) - AIC(y_{true} \\sim \\phi)

    A **negative** return value indicates that the predictions are
    informative about the true labels (matching the convention used by
    ``catdap1`` / ``target_analysis.ranking``). Issue #18 phrased this
    as "positive when informative" — see H-0012 §A5 for the rationale
    behind keeping the existing project-wide negative-is-good convention.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned labels (any dtype supported by :func:`pandas.crosstab`).

    Returns
    -------
    float
        ΔAIC value. Negative → predictions are informative; positive →
        predictions are uninformative (worse than chance under AIC).
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    if y_true_arr.shape[0] != y_pred_arr.shape[0]:
        msg = (
            f"y_true and y_pred must have the same length "
            f"(got {y_true_arr.shape[0]} and {y_pred_arr.shape[0]})"
        )
        raise ValueError(msg)
    if y_true_arr.size == 0:
        msg = "confusion_aic requires at least one observation"
        raise ValueError(msg)

    classes = sorted({*np.unique(y_true_arr).tolist(), *np.unique(y_pred_arr).tolist()})
    cross = pd.crosstab(
        pd.Series(y_true_arr, name="y_true"),
        pd.Series(y_pred_arr, name="y_pred"),
        dropna=False,
    ).reindex(index=classes, columns=classes, fill_value=0)
    cross_freq = cross.to_numpy(dtype=np.int64)
    marginal_e = cross_freq.sum(axis=1)
    marginal_f = cross_freq.sum(axis=0)
    n = int(cross_freq.sum())
    return float(compute_delta_aic(cross_freq, marginal_e, marginal_f, n))


__all__ = ["confusion_aic", "plot_confusion", "plot_confusion_by_slice"]
