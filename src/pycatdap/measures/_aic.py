"""AIC measure for a 2D contingency table (H-0008 PR-D4).

Wraps :func:`pycatdap._aic.compute_delta_aic` so it accepts a single
2D ``cross_freq`` and derives the row/column marginals internally,
matching the uniform ``Measure`` signature
``Callable[[npt.NDArray[np.float64]], float]``.

The returned value is the **delta AIC** (two-way model minus null
model), so negative = informative explanatory variable, positive =
the explanatory variable is noise relative to the model-complexity
penalty.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from pycatdap._aic import compute_delta_aic


def aic(cross_freq: npt.NDArray[np.float64]) -> float:
    """Compute ΔAIC for a 2D contingency table.

    Parameters
    ----------
    cross_freq : ndarray of shape (C_E, C_F)
        Contingency table. Rows are response (E) categories, columns
        are explanatory (F) categories.

    Returns
    -------
    float
        ΔAIC = AIC(E; F) − AIC(E; ∅). Negative = explanatory variable
        is informative; positive = explanatory variable is noise.

    Raises
    ------
    ValueError
        If ``cross_freq`` is not 2D or has zero total mass.

    Examples
    --------
    >>> import numpy as np
    >>> from pycatdap.measures import aic
    >>> aic(np.array([[50.0, 0.0], [0.0, 50.0]])) < 0
    True
    """
    cf = np.asarray(cross_freq, dtype=np.float64)
    if cf.ndim != 2:
        msg = f"aic: cross_freq must be 2D; got shape {cf.shape}"
        raise ValueError(msg)
    marginal_e = cf.sum(axis=1)
    marginal_f = cf.sum(axis=0)
    n = int(cf.sum())
    return compute_delta_aic(cf, marginal_e, marginal_f, n)


__all__ = ["aic"]
