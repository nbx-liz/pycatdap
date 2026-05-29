"""Shared plot-backend dispatch for the error subpackage (H-0014 PR-L1).

Single source of truth for the ``matplotlib`` / ``plotly`` dispatch that
was previously duplicated verbatim across :mod:`pycatdap.error.confusion`,
:mod:`pycatdap.error.residual`, and :mod:`pycatdap.error.calibration`.
Phase L's ``compare_cohorts`` becomes the fourth consumer, so the block
is extracted here before that consumer lands (review-agreed deferral
target from the v0.10.0 multi-agent review).

The backend modules are imported lazily inside :func:`get_backend_module`
so that ``import pycatdap.error`` stays free of a hard matplotlib/plotly
dependency (lowest-direct-deps CI safe).
"""

from __future__ import annotations

from typing import Any, Literal

Backend = Literal["matplotlib", "plotly"]


def get_backend_module(backend: Backend) -> Any:
    """Return the plotting implementation module for ``backend``.

    Parameters
    ----------
    backend : {"matplotlib", "plotly"}
        Which plotting backend to dispatch to.

    Returns
    -------
    module
        :mod:`pycatdap.plot.matplotlib` or :mod:`pycatdap.plot.plotly`,
        imported lazily.

    Raises
    ------
    ValueError
        If ``backend`` is neither ``"matplotlib"`` nor ``"plotly"``.
    """
    if backend == "matplotlib":
        from pycatdap.plot import matplotlib as _mpl

        return _mpl
    if backend == "plotly":
        from pycatdap.plot import plotly as _plotly

        return _plotly
    msg = f"Unknown plot backend: {backend!r}. Use 'matplotlib' or 'plotly'."
    raise ValueError(msg)
