"""Cramér's V measure for a 2D contingency table (H-0008 PR-D4).

Pure-numpy implementation — no scipy dependency. The formula is

.. math::

    V = \\sqrt{\\frac{\\chi^2}{n \\cdot \\min(r-1,\\ c-1)}}

where ``chi^2`` is computed from observed vs expected under
independence. V ranges in ``[0, 1]``: 0 for independence, 1 for
perfect association.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def cramers_v(cross_freq: npt.NDArray[np.float64]) -> float:
    """Compute Cramér's V for a 2D contingency table.

    Parameters
    ----------
    cross_freq : ndarray of shape (r, c)
        Contingency table of non-negative frequencies.

    Returns
    -------
    float
        Cramér's V in ``[0, 1]``. Returns 0.0 for degenerate shapes
        (``r == 1`` or ``c == 1``) where the denominator vanishes.

    Examples
    --------
    >>> import numpy as np
    >>> from pycatdap.measures import cramers_v
    >>> cramers_v(np.array([[50.0, 0.0], [0.0, 50.0]]))
    1.0
    """
    cf = np.asarray(cross_freq, dtype=np.float64)
    if cf.ndim != 2:
        msg = f"cramers_v: cross_freq must be 2D; got shape {cf.shape}"
        raise ValueError(msg)

    n = float(cf.sum())
    if n <= 0:
        msg = "cramers_v: cross_freq must contain at least one observation"
        raise ValueError(msg)

    r, c = cf.shape
    denom = n * min(r - 1, c - 1)
    if denom <= 0:
        # 1xN or Nx1 — V is undefined; return 0 (no association detectable)
        return 0.0

    row = cf.sum(axis=1, keepdims=True)
    col = cf.sum(axis=0, keepdims=True)
    expected = (row @ col) / n
    diff_sq = (cf - expected) ** 2
    # np.divide(..., where=...) skips the division for masked cells
    # entirely, so no spurious RuntimeWarning is emitted on tables
    # with an all-zero marginal row or column. Plain
    # ``np.where(expected > 0, diff_sq / expected, 0.0)`` would have
    # produced the right value but raised "invalid value encountered
    # in divide" under ``warnings.filterwarnings('error')``.
    safe = np.divide(diff_sq, expected, out=np.zeros_like(diff_sq), where=expected > 0)
    chi2 = float(np.sum(safe))

    return float(np.sqrt(chi2 / denom))


__all__ = ["cramers_v"]
