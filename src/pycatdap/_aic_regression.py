"""Gaussian regression AIC for piecewise-constant models (H-0005).

Extends the categorical CATDAP AIC machinery to continuous targets without
discretizing Y. The model assumes y_j = mean(bin(j)) + epsilon_j with iid
Gaussian errors of shared variance.

Reference implementation: nbx-liz/AdvancedCATDAP scoring.py:Scorer. See
``docs/research/h0005-continuous-target.md`` for the derivation, cross-pair
comparability proof, and cross-check verdict.

The formulas:

    RSS    = sum_i sum_{j in bin i} (y_j - mean_i)^2          (within-bin SS)
    AIC    = n * log(RSS / n)  +  penalty(k_means + 1, n)
    AIC_0  = n * log(TSS / n)  +  penalty(2, n)               (null: y = mean)
    dAIC   = AIC - AIC_0

The ``+ 1`` in ``k_means + 1`` counts the shared variance parameter; matches
AdvancedCATDAP's convention. Penalty depends on ``criterion``:

    "bic":  log(n) * k     (Schwarz 1978; recommended for changepoint
                            structures per Yao 1988)
    "aic":  2 * k          (classical AIC; Akaike 1973)
    "aicc": 2k + 2k(k+1) / (n - k - 1)
                           (Hurvich and Tsai 1989 small-sample correction;
                            here k includes the variance parameter, matching
                            AdvancedCATDAP)

The "model-independent constant" n*log(2*pi) + n that appears in the full
Gaussian AIC cancels in dAIC, so it is dropped here.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import numpy.typing as npt

Criterion = Literal["aic", "aicc", "bic"]

EPSILON_RSS = 1e-10  # Floor for RSS to avoid log(0) when prediction is perfect.


def _penalty(k: int, n: int, criterion: Criterion) -> float:
    """AIC-family complexity penalty for *k* parameters on *n* observations.

    Parameters
    ----------
    k : int
        Total parameter count (including the variance parameter).
    n : int
        Sample size.
    criterion : {"aic", "aicc", "bic"}
        Penalty family.

    Returns
    -------
    float
        The additive penalty. For AICc with ``n <= k + 1`` returns ``inf``.

    Examples
    --------
    >>> round(_penalty(3, 100, "aic"), 4)
    6.0
    >>> round(_penalty(3, 100, "bic"), 4)
    13.8155
    >>> round(_penalty(3, 100, "aicc"), 4)
    6.25
    """
    if criterion == "aic":
        return 2.0 * k
    if criterion == "bic":
        return float(np.log(n)) * k
    if criterion == "aicc":
        if n <= k + 1:
            return float("inf")
        return 2.0 * k + 2.0 * k * (k + 1) / (n - k - 1)
    msg = f"unknown criterion: {criterion!r} (expected 'aic', 'aicc', or 'bic')"
    raise ValueError(msg)


def compute_rss(
    y: npt.NDArray[np.float64],
    group_idx: npt.NDArray[np.intp],
) -> tuple[float, int]:
    """Within-group residual sum of squares and number of non-empty groups.

    Vectorized via :func:`numpy.bincount` with weights, equivalent to
    ``sum_i sum_{j in bin i} (y_j - mean_i)^2`` but O(N) and without
    materializing per-bin arrays.

    Parameters
    ----------
    y : ndarray of float64
        Target values, length n.
    group_idx : ndarray of intp
        Non-negative group code per observation, length n. Empty groups (no
        observations) are skipped automatically.

    Returns
    -------
    rss : float
        Within-group sum of squared deviations. Floored at ``EPSILON_RSS``.
    k_means : int
        Count of non-empty groups (one mean parameter per group).

    Examples
    --------
    >>> import numpy as np
    >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    >>> idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
    >>> rss, k = compute_rss(y, idx)
    >>> round(rss, 6), k
    (4.0, 2)
    """
    if len(y) == 0:
        return EPSILON_RSS, 0
    minlength = int(group_idx.max()) + 1 if len(group_idx) > 0 else 1
    counts = np.bincount(group_idx, minlength=minlength)
    valid = counts > 0
    k_means = int(np.count_nonzero(valid))

    sum_y = np.bincount(group_idx, weights=y, minlength=minlength)
    sum_y2 = np.bincount(group_idx, weights=y * y, minlength=minlength)
    term2 = np.zeros_like(sum_y)
    term2[valid] = (sum_y[valid] ** 2) / counts[valid]
    rss = float(np.sum(sum_y2 - term2))
    rss = max(rss, EPSILON_RSS)
    return rss, k_means


def compute_gaussian_aic(
    y: npt.NDArray[np.float64],
    group_idx: npt.NDArray[np.intp],
    criterion: Criterion = "bic",
) -> float:
    """AIC of a piecewise-constant Gaussian regression model.

    The constant ``n * log(2 * pi) + n`` from the full Gaussian AIC is
    dropped because it cancels in dAIC.

    Parameters
    ----------
    y : ndarray of float64
    group_idx : ndarray of intp
    criterion : {"aic", "aicc", "bic"}

    Returns
    -------
    float

    Examples
    --------
    >>> import numpy as np
    >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    >>> idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
    >>> round(compute_gaussian_aic(y, idx, "aic"), 4)
    3.5672
    """
    n = len(y)
    if n == 0:
        return float("inf")
    rss, k_means = compute_rss(y, group_idx)
    k = k_means + 1  # +1 for shared variance parameter
    return float(n * np.log(rss / n) + _penalty(k, n, criterion))


def compute_gaussian_null_aic(
    y: npt.NDArray[np.float64],
    criterion: Criterion = "bic",
) -> float:
    """AIC of the null Gaussian model ``y = global mean + epsilon``.

    Two parameters: the global mean and the variance.

    Parameters
    ----------
    y : ndarray of float64
    criterion : {"aic", "aicc", "bic"}

    Returns
    -------
    float

    Examples
    --------
    >>> import numpy as np
    >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    >>> round(compute_gaussian_null_aic(y, "aic"), 4)
    10.4185
    """
    n = len(y)
    if n == 0:
        return float("inf")
    mean = float(np.mean(y))
    tss = float(np.sum((y - mean) ** 2))
    tss = max(tss, EPSILON_RSS)
    return float(n * np.log(tss / n) + _penalty(2, n, criterion))


def compute_delta_aic_regression(
    y: npt.NDArray[np.float64],
    group_idx: npt.NDArray[np.intp],
    criterion: Criterion = "bic",
) -> tuple[float, float]:
    """Delta-AIC and R-squared for a piecewise-constant Gaussian regression.

    ``delta_aic = compute_gaussian_aic(...) - compute_gaussian_null_aic(...)``
    ``r_squared = 1 - RSS / TSS``

    Parameters
    ----------
    y : ndarray of float64
    group_idx : ndarray of intp
    criterion : {"aic", "aicc", "bic"}

    Returns
    -------
    delta_aic : float
        Negative when the binned model fits better than the null. Same sign
        convention as the categorical mode (more negative = more informative).
    r_squared : float
        Coefficient of determination, ``1 - RSS / TSS``. Clipped to
        ``[0, 1 - EPSILON_RSS / TSS]`` for numerical safety.

    Examples
    --------
    >>> import numpy as np
    >>> y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    >>> idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
    >>> delta, r2 = compute_delta_aic_regression(y, idx, "aic")
    >>> round(delta, 4), round(r2, 4)
    (-6.8513, 0.7714)
    """
    n = len(y)
    if n == 0:
        return float("inf"), 0.0
    rss, k_means = compute_rss(y, group_idx)
    mean = float(np.mean(y))
    tss = float(np.sum((y - mean) ** 2))
    tss = max(tss, EPSILON_RSS)
    r_squared = 1.0 - rss / tss
    r_squared = max(0.0, min(1.0, r_squared))

    aic = n * np.log(rss / n) + _penalty(k_means + 1, n, criterion)
    aic_null = n * np.log(tss / n) + _penalty(2, n, criterion)
    return float(aic - aic_null), float(r_squared)
