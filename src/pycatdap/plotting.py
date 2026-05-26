"""v0.2 compatibility shim for the legacy ``pycatdap.plotting`` import path.

The canonical path for visualization in v0.3+ is ``pycatdap.plot``
(with backend dispatch) or ``pycatdap.plot.matplotlib`` (direct).

This shim re-exports the matplotlib backend functions so that existing
v0.2 user code continues to work without modification:

>>> from pycatdap.plotting import mosaic_plot  # still works
>>> from pycatdap.plot.matplotlib import mosaic_plot  # canonical
>>> from pycatdap.plot import mosaic_plot  # backend dispatcher

This shim is preserved through v1.0. v1.0 will add a ``DeprecationWarning``
on use, and v2.0 may remove this module.
"""

from __future__ import annotations

from pycatdap.plot.matplotlib import (
    aic_comparison_plot,
    barplot_twoway,
    mosaic_plot,
)

__all__ = [
    "aic_comparison_plot",
    "barplot_twoway",
    "mosaic_plot",
]
