"""Mutual information measure for a 2D contingency table (H-0008 PR-D4).

Pure-numpy implementation in **nats** (natural log). The formula is

.. math::

    I(X; Y) = \\sum_{i, j} p(i, j) \\log \\frac{p(i, j)}{p(i)\\, p(j)}

with the convention ``0 * log(0/0) = 0`` for zero cells, applied via
masked indexing (no scipy dependency).
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def mutual_info(cross_freq: npt.NDArray[np.float64]) -> float:
    """Compute mutual information (in nats) for a 2D contingency table.

    Parameters
    ----------
    cross_freq : ndarray of shape (r, c)
        Contingency table of non-negative frequencies.

    Returns
    -------
    float
        Mutual information ``I(X; Y)`` in nats. ``0`` when ``X`` and
        ``Y`` are independent (within numerical tolerance); strictly
        positive otherwise.

    Examples
    --------
    >>> import numpy as np
    >>> from pycatdap.measures import mutual_info
    >>> round(mutual_info(np.array([[50.0, 0.0], [0.0, 50.0]])), 4)
    0.6931
    """
    cf = np.asarray(cross_freq, dtype=np.float64)
    if cf.ndim != 2:
        msg = f"mutual_info: cross_freq must be 2D; got shape {cf.shape}"
        raise ValueError(msg)

    n = float(cf.sum())
    if n <= 0:
        msg = "mutual_info: cross_freq must contain at least one observation"
        raise ValueError(msg)

    joint = cf / n
    p_row = joint.sum(axis=1, keepdims=True)
    p_col = joint.sum(axis=0, keepdims=True)
    indep = p_row @ p_col

    # Apply 0 * log(0/0) = 0 by masking cells where joint == 0 (which
    # forces indep == 0 as well unless a row or column marginal is 0;
    # in that case the product is also 0 and the cell does not contribute).
    mask = joint > 0
    safe_joint = np.where(mask, joint, 1.0)  # placeholder, masked out below
    safe_indep = np.where(mask & (indep > 0), indep, 1.0)
    log_ratio = np.log(safe_joint / safe_indep)
    contribution = np.where(mask, joint * log_ratio, 0.0)

    return float(contribution.sum())


__all__ = ["mutual_info"]
