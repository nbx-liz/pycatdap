"""Core AIC computation for contingency tables.

Implements the AIC statistics for two-way contingency tables as defined by
Sakamoto & Katsura (1980).  Zero-frequency cells use the convention
``0 * ln(0) = 0``.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

# ---------------------------------------------------------------------------
# Safe x*log(y) with 0*log(0) = 0
# ---------------------------------------------------------------------------

try:
    from scipy.special import xlogy as _scipy_xlogy  # type: ignore[import-untyped]

    def _safe_xlogy(
        x: npt.NDArray[np.float64],
        y: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        """Compute ``x * ln(y)`` with the convention ``0 * ln(0) = 0``.

        Uses :func:`scipy.special.xlogy` when available.

        Parameters
        ----------
        x : ndarray
            Frequencies (non-negative).
        y : ndarray
            Denominators (non-negative).

        Returns
        -------
        ndarray
            Element-wise ``x * ln(y)``, with 0 where *x* is zero.
        """
        return np.asarray(_scipy_xlogy(x, y), dtype=np.float64)

except ImportError:  # pragma: no cover – scipy optional

    def _safe_xlogy(
        x: npt.NDArray[np.float64],
        y: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        """Compute ``x * ln(y)`` with the convention ``0 * ln(0) = 0``.

        Pure-numpy fallback when scipy is not installed.
        """
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        # Guard: negative y with non-zero x indicates a bug upstream
        if np.any((y < 0) & (x != 0)):
            msg = "negative y with non-zero x: frequencies must be non-negative"
            raise ValueError(msg)
        return np.where(x == 0, 0.0, x * np.log(np.where(y > 0, y, 1.0)))


# ---------------------------------------------------------------------------
# AIC(E; F) — two-way contingency table model
# ---------------------------------------------------------------------------


def compute_aic_twoway(
    cross_freq: npt.NDArray[np.float64],
    marginal_f: npt.NDArray[np.float64],
) -> float:
    r"""Compute AIC for the two-way table model.

    .. math::

        AIC(E; F) = -2 \sum_{i,j} n_{EF}(i,j) \ln \frac{n_{EF}(i,j)}{n_F(j)}
                    + 2 (C_E - 1) C_F

    Parameters
    ----------
    cross_freq : ndarray, shape (C_E, C_F)
        Cross-frequency table.
    marginal_f : ndarray, shape (C_F,)
        Marginal frequencies of the explanatory variable.

    Returns
    -------
    float
        AIC value for the two-way model.
    """
    if cross_freq.sum() == 0:
        msg = "cross_freq must contain at least one observation"
        raise ValueError(msg)

    c_e: int = cross_freq.shape[0]
    c_f: int = cross_freq.shape[1]

    if marginal_f.shape[0] != c_f:
        msg = (
            f"marginal_f length ({marginal_f.shape[0]}) must equal "
            f"cross_freq columns ({c_f})"
        )
        raise ValueError(msg)

    # n_EF(i,j) / n_F(j) — broadcast marginal_f across rows
    ratio = np.where(marginal_f > 0, cross_freq / marginal_f, 0.0)
    log_likelihood = float(np.sum(_safe_xlogy(cross_freq, ratio)))

    penalty = 2.0 * (c_e - 1) * c_f
    return float(-2.0 * log_likelihood + penalty)


# ---------------------------------------------------------------------------
# AIC(E; φ) — null (base) model
# ---------------------------------------------------------------------------


def compute_base_aic(
    marginal_e: npt.NDArray[np.float64],
    n: int,
) -> float:
    r"""Compute AIC for the null model (no explanatory variable).

    .. math::

        AIC(E; \phi) = -2 \sum_i n_E(i) \ln \frac{n_E(i)}{n} + 2 (C_E - 1)

    Parameters
    ----------
    marginal_e : ndarray, shape (C_E,)
        Marginal frequencies of the response variable.
    n : int
        Total number of observations.

    Returns
    -------
    float
        AIC value for the null model.

    Raises
    ------
    ValueError
        If *n* is not positive.
    """
    if n <= 0:
        msg = "n must be positive; received an empty dataset"
        raise ValueError(msg)

    c_e = len(marginal_e)

    ratio = marginal_e / n
    log_likelihood: float = float(np.sum(_safe_xlogy(marginal_e, ratio)))

    penalty = 2.0 * (c_e - 1)
    return -2.0 * log_likelihood + penalty


# ---------------------------------------------------------------------------
# ΔAIC = AIC(E; F) − AIC(E; φ)
# ---------------------------------------------------------------------------


def compute_delta_aic(
    cross_freq: npt.NDArray[np.float64],
    marginal_e: npt.NDArray[np.float64],
    marginal_f: npt.NDArray[np.float64],
    n: int,
) -> float:
    r"""Compute the delta AIC between two-way and null models.

    .. math::

        \Delta AIC = AIC(E; F) - AIC(E; \phi)

    A negative value indicates that the explanatory variable *F* is
    informative about the response *E*.

    Parameters
    ----------
    cross_freq : ndarray, shape (C_E, C_F)
        Cross-frequency table.
    marginal_e : ndarray, shape (C_E,)
        Marginal frequencies of the response variable.
    marginal_f : ndarray, shape (C_F,)
        Marginal frequencies of the explanatory variable.
    n : int
        Total number of observations.

    Returns
    -------
    float
        ΔAIC value (negative = explanatory variable is useful).
    """
    aic_twoway = compute_aic_twoway(cross_freq, marginal_f)
    aic_base = compute_base_aic(marginal_e, n)
    return aic_twoway - aic_base
