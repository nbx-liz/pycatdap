"""Phase K calibration metrics + reliability-diagram dispatch (H-0013 PR-K1).

Public API entries:

- :func:`calibration_curve` — reliability diagram (figure) with Wilson CIs
- :func:`calibration_table` — per-bin numeric data behind the diagram
- :func:`brier_score` — mean squared error of probability predictions
- :func:`expected_calibration_error` — bin-weighted ``|observed − predicted|``
- :func:`maximum_calibration_error` — worst-bin ``|observed − predicted|``

Binary classification only (v0.10.0); regression + multi-class calibration
are deferred to v0.11.0 (H-0013 §G). The probability axis is partitioned by
``strategy=``:

- ``"aic"`` (default): AIC-optimal pooling via
  :func:`pycatdap._pooling.optimal_binning`, using a **bounded** initial grid
  (``_AIC_INIT_BINS``) so continuous probabilities do not explode the initial
  bin count (H-0013 §B-bis). Bottom-up AIC merging then discovers the optimal
  coarser partition — bins land where the observed positive-rate shifts.
- ``"equal_width"`` / ``"quantile"``: ``n_bins`` fixed bins over ``[0, 1]``.

Backend dispatch mirrors :mod:`pycatdap.plot` — pass ``backend="matplotlib"``
or ``backend="plotly"``.

Note: unlike :func:`sklearn.calibration.calibration_curve` (which returns
``(prob_true, prob_pred)`` arrays), this :func:`calibration_curve` returns a
*figure*, consistent with the Phase I/J ``plot_confusion`` / ``residual_plot``
convention. Use :func:`calibration_table` for the numeric curve data.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._pooling import optimal_binning
from pycatdap.error._backend import Backend
from pycatdap.error._backend import get_backend_module as _get_backend_module

Strategy = Literal["aic", "equal_width", "quantile"]

#: Bounded initial-grid resolution for ``strategy="aic"`` (H-0013 §B-bis).
#: Probabilities are conceptually in ``[0, 1]``; a fixed ``1/50 = 0.02`` grid
#: caps the initial bin count at ~50 regardless of the float resolution of
#: ``y_proba``, avoiding the ``_auto_accuracy`` smallest-gap explosion (a
#: continuous predictor can have a minimum gap of ~1e-4 → thousands of bins).
_AIC_INIT_BINS = 50

#: Standard-normal two-sided quantile for a 95% interval.
_WILSON_Z = 1.959963984540054


def _validate_binary_proba(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
) -> tuple[npt.NDArray[np.int64], npt.NDArray[np.float64]]:
    """Validate and align binary labels with probabilities.

    Non-finite ``y_proba`` rows are dropped (with their ``y_true`` partners).

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned ground-truth labels and predicted probabilities of the
        positive class.

    Returns
    -------
    (y_true_int, y_proba_float) : tuple of ndarray
        Masked arrays with ``y_true_int`` coerced to ``{0, 1}``.

    Raises
    ------
    ValueError
        If lengths differ, there are no finite observations, probabilities
        fall outside ``[0, 1]``, or ``y_true`` is not binary ``{0, 1}``.
    """
    yt = np.asarray(y_true)
    yp = np.asarray(y_proba, dtype=np.float64)
    if yt.shape[0] != yp.shape[0]:
        msg = (
            f"y_true and y_proba must have the same length "
            f"(got {yt.shape[0]} and {yp.shape[0]})"
        )
        raise ValueError(msg)
    if yt.size == 0:
        msg = "calibration requires at least one observation"
        raise ValueError(msg)

    # Drop rows where either y_proba or (float) y_true is non-finite. Masking
    # y_true too avoids a NaN label leaking into the binary check below and
    # producing a confusing "got classes [0.0, 1.0, nan]" error. Non-float
    # y_true (int / bool / object) cannot hold NaN, so guard the isfinite call.
    finite = np.isfinite(yp)
    if np.issubdtype(yt.dtype, np.floating):
        finite = finite & np.isfinite(yt)
    yt = yt[finite]
    yp = yp[finite]
    if yp.size == 0:
        msg = "calibration requires at least one finite (y_true, y_proba) pair"
        raise ValueError(msg)

    if float(yp.min()) < 0.0 or float(yp.max()) > 1.0:
        msg = (
            f"y_proba must lie in [0, 1] "
            f"(got range [{float(yp.min()):.4g}, {float(yp.max()):.4g}])"
        )
        raise ValueError(msg)

    # Coerce y_true to {0, 1}; accept bool and the integer/float values 0/1.
    if yt.dtype == bool:
        return yt.astype(np.int64), yp
    uniq = np.unique(yt)
    if not bool(np.all(np.isin(uniq, np.array([0, 1])))):
        msg = (
            f"calibration is binary-only: y_true must be 0/1 (or bool); "
            f"got classes {uniq.tolist()!r}. Encode the positive class as 1 "
            f"(multi-class calibration is deferred to v0.11.0)."
        )
        raise ValueError(msg)
    return yt.astype(np.int64), yp


def _wilson_interval(
    k: npt.NDArray[np.float64],
    n: npt.NDArray[np.float64],
    z: float = _WILSON_Z,
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Vectorised Wilson score interval for a binomial proportion.

    Robust near ``p → 0`` / ``p → 1`` (the skewed-prediction case), unlike the
    normal (Wald) approximation which can leave ``[0, 1]``. Pure-numpy.

    Parameters
    ----------
    k : ndarray
        Per-bin positive counts.
    n : ndarray
        Per-bin totals (each ``> 0``).
    z : float
        Standard-normal quantile (default 1.96 → 95%).

    Returns
    -------
    (low, high) : tuple of ndarray
        Lower and upper bounds, clipped to ``[0, 1]``.
    """
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    half = (z / denom) * np.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n))
    low = np.clip(center - half, 0.0, 1.0)
    high = np.clip(center + half, 0.0, 1.0)
    return low, high


def _bin_codes(
    y_proba: npt.NDArray[np.float64],
    y_true_int: npt.NDArray[np.int64],
    strategy: str,
    n_bins: int,
) -> npt.NDArray[np.intp]:
    """Assign each probability to a contiguous bin code per ``strategy``."""
    if strategy == "aic":
        # Explicit bounded accuracy — see _AIC_INIT_BINS / H-0013 §B-bis.
        pooling = optimal_binning(
            y_proba,
            y_true_int.astype(object),
            accuracy=1.0 / _AIC_INIT_BINS,
        )
        return np.asarray(pooling.codes, dtype=np.intp)

    if strategy == "equal_width":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
    else:
        # Strategy is validated in _calibration_table, so this is "quantile".
        assert strategy == "quantile", f"unexpected strategy {strategy!r}"
        edges = np.unique(np.quantile(y_proba, np.linspace(0.0, 1.0, n_bins + 1)))
        if edges.size < 2:
            # Degenerate (near-constant) probabilities collapse to one bin.
            edges = np.array([float(y_proba.min()), float(y_proba.max()) + 1e-12])

    codes = np.clip(np.digitize(y_proba, edges[1:-1]), 0, len(edges) - 2)
    return codes.astype(np.intp)


def _calibration_table(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: str = "aic",
    n_bins: int = 10,
) -> pd.DataFrame:
    """Build the per-bin reliability table (private core).

    Empty bins are omitted by construction (iteration is over occupied codes
    only; H-0013 §B-bis) so downstream metrics never divide by zero. Rows are
    ordered by ``bin_low`` ascending.

    Columns: ``bin_low, bin_high, n, prob_pred, prob_true, ci_low, ci_high``.
    """
    if strategy not in ("aic", "equal_width", "quantile"):
        msg = (
            f"unknown strategy={strategy!r}; expected 'aic', "
            f"'equal_width', or 'quantile'"
        )
        raise ValueError(msg)
    if n_bins < 1:
        msg = f"n_bins must be >= 1 (got {n_bins})"
        raise ValueError(msg)

    yt_int, yp = _validate_binary_proba(y_true, y_proba)
    codes = _bin_codes(yp, yt_int, strategy, n_bins)

    rows: list[dict[str, float]] = []
    for code in np.unique(codes):
        mask = codes == code
        proba_bin = yp[mask]
        true_bin = yt_int[mask]
        rows.append(
            {
                "bin_low": float(proba_bin.min()),
                "bin_high": float(proba_bin.max()),
                "n": float(proba_bin.size),
                "prob_pred": float(proba_bin.mean()),
                "prob_true": float(true_bin.mean()),
            }
        )

    table = pd.DataFrame(
        rows, columns=["bin_low", "bin_high", "n", "prob_pred", "prob_true"]
    )
    if table.empty:  # pragma: no cover - unreachable: _validate_binary_proba
        # guarantees >= 1 finite row, so np.unique(codes) yields >= 1 bin.
        table["ci_low"] = pd.Series(dtype=np.float64)
        table["ci_high"] = pd.Series(dtype=np.float64)
        return table

    ordered: pd.DataFrame = table.sort_values("bin_low").reset_index(drop=True)
    ordered["n"] = ordered["n"].astype(np.int64)
    k_arr = (ordered["prob_true"] * ordered["n"]).to_numpy(dtype=np.float64)
    n_arr = ordered["n"].to_numpy(dtype=np.float64)
    low, high = _wilson_interval(k_arr, n_arr)
    ordered["ci_low"] = low
    ordered["ci_high"] = high
    return ordered


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def calibration_table(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: Strategy = "aic",
    n_bins: int = 10,
) -> pd.DataFrame:
    """Per-bin reliability table behind the calibration curve (H-0013 Phase K).

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned binary labels (``0`` / ``1``) and positive-class probabilities.
    strategy : {"aic", "equal_width", "quantile"}
        Probability-axis binning. ``"aic"`` (default) pools via
        :func:`pycatdap._pooling.optimal_binning`; ``n_bins`` is ignored.
    n_bins : int
        Bin count for ``equal_width`` / ``quantile`` (ignored for ``aic``).

    Returns
    -------
    pandas.DataFrame
        Columns ``bin_low, bin_high, n, prob_pred, prob_true, ci_low, ci_high``.
        One row per occupied bin (Wilson 95% CI on ``prob_true``).
    """
    return _calibration_table(y_true, y_proba, strategy=strategy, n_bins=n_bins)


def brier_score(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
) -> float:
    """Brier score for binary probabilities (H-0013 Phase K).

    ``mean((y_proba - y_true) ** 2)`` — equals
    :func:`sklearn.metrics.brier_score_loss` for binary inputs. Lower is better
    (``0`` = perfect). Binning-independent (computed over all observations).

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned binary labels and positive-class probabilities.

    Returns
    -------
    float
    """
    yt_int, yp = _validate_binary_proba(y_true, y_proba)
    return float(np.mean((yp - yt_int) ** 2))


def expected_calibration_error(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: Strategy = "aic",
    n_bins: int = 10,
) -> float:
    r"""Expected Calibration Error (H-0013 Phase K).

    .. math::

        \mathrm{ECE} = \sum_b \frac{n_b}{N}
            \bigl| \mathrm{prob\_true}_b - \mathrm{prob\_pred}_b \bigr|

    The bin-frequency-weighted mean gap between observed and predicted
    probability. Lower is better (``0`` = perfectly calibrated under the
    chosen binning). Empty bins contribute nothing (excluded from the table).

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned binary labels and positive-class probabilities.
    strategy : {"aic", "equal_width", "quantile"}
        Probability-axis binning (see :func:`calibration_table`).
    n_bins : int
        Bin count for ``equal_width`` / ``quantile``.

    Returns
    -------
    float
    """
    table = _calibration_table(y_true, y_proba, strategy=strategy, n_bins=n_bins)
    if table.empty:  # pragma: no cover - unreachable post-validation
        return 0.0
    n_total = float(table["n"].sum())
    gaps = (table["prob_true"] - table["prob_pred"]).abs().to_numpy(dtype=np.float64)
    weights = table["n"].to_numpy(dtype=np.float64) / n_total
    return float(np.sum(weights * gaps))


def maximum_calibration_error(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: Strategy = "aic",
    n_bins: int = 10,
) -> float:
    r"""Maximum Calibration Error (H-0013 Phase K).

    .. math::

        \mathrm{MCE} = \max_b
            \bigl| \mathrm{prob\_true}_b - \mathrm{prob\_pred}_b \bigr|

    The worst-bin gap between observed and predicted probability. Empty bins
    are excluded.

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned binary labels and positive-class probabilities.
    strategy : {"aic", "equal_width", "quantile"}
        Probability-axis binning (see :func:`calibration_table`).
    n_bins : int
        Bin count for ``equal_width`` / ``quantile``.

    Returns
    -------
    float
    """
    table = _calibration_table(y_true, y_proba, strategy=strategy, n_bins=n_bins)
    if table.empty:  # pragma: no cover - unreachable post-validation
        return 0.0
    gaps = (table["prob_true"] - table["prob_pred"]).abs()
    return float(gaps.max())


def calibration_curve(
    y_true: npt.NDArray[Any] | pd.Series,
    y_proba: npt.NDArray[Any] | pd.Series,
    *,
    strategy: Strategy = "aic",
    n_bins: int = 10,
    backend: Backend = "matplotlib",
    **kwargs: Any,
) -> Any:
    """Reliability diagram with Wilson confidence intervals (H-0013 Phase K).

    Plots observed positive-rate against mean predicted probability per bin,
    with a ``y = x`` perfect-calibration reference and binomial (Wilson) error
    bars. Returns a *figure* (not curve data — use :func:`calibration_table`).

    Parameters
    ----------
    y_true, y_proba : array-like
        Aligned binary labels (``0`` / ``1``) and positive-class probabilities.
    strategy : {"aic", "equal_width", "quantile"}
        Probability-axis binning (see :func:`calibration_table`).
    n_bins : int
        Bin count for ``equal_width`` / ``quantile`` (ignored for ``aic``).
    backend : {"matplotlib", "plotly"}
        Plotting backend.
    **kwargs
        Forwarded to the matplotlib ``Axes.errorbar`` call (e.g. ``ax=``,
        ``color=``, ``markersize=``). The plotly backend ignores ``**kwargs``.

    Returns
    -------
    matplotlib.axes.Axes | plotly.graph_objects.Figure
    """
    return _get_backend_module(backend).calibration_curve(
        y_true, y_proba, strategy=strategy, n_bins=n_bins, **kwargs
    )


__all__ = [
    "brier_score",
    "calibration_curve",
    "calibration_table",
    "expected_calibration_error",
    "maximum_calibration_error",
]
