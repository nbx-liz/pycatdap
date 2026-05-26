"""Plotly backend for pycatdap visualization.

This module is part of the v0.3+ dual-backend plotting API. Plotly
implementations are introduced incrementally; until each function is
implemented, calling it raises ``NotImplementedError`` with a pointer
to the tracking issue.

See ``pycatdap.plot`` for the dispatcher and the canonical entry points.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

    from pycatdap.catdap1 import Catdap1Result
    from pycatdap.catdap2 import Catdap2Result


def _import_plotly() -> Any:
    """Import plotly.graph_objects or raise with install instructions."""
    try:
        import plotly.graph_objects as go

        return go
    except ImportError:
        msg = (
            "plotly is required for the Plotly backend. "
            "Install it with: pip install 'pycatdap[plotly]'"
        )
        raise ImportError(msg) from None


def aic_comparison_plot(
    result: Catdap1Result | Catdap2Result,
    response: str | None = None,
    **kwargs: Any,
) -> Any:
    """Horizontal bar chart of ΔAIC values (Plotly).

    .. note::
       Implementation pending. Tracked in `GitHub Issue #12
       <https://github.com/nbx-liz/pycatdap/issues/12>`_.
    """
    _import_plotly()  # eager check so users get the install message first
    msg = (
        "Plotly backend for aic_comparison_plot is not yet implemented. "
        "See https://github.com/nbx-liz/pycatdap/issues/12. "
        "Use backend='matplotlib' in the meantime."
    )
    raise NotImplementedError(msg)


def barplot_twoway(table: pd.DataFrame, **kwargs: Any) -> Any:
    """Stacked proportional bar chart for a two-way frequency table (Plotly).

    .. note::
       Implementation pending. Tracked in `GitHub Issue #12
       <https://github.com/nbx-liz/pycatdap/issues/12>`_.
    """
    _import_plotly()
    msg = (
        "Plotly backend for barplot_twoway is not yet implemented. "
        "See https://github.com/nbx-liz/pycatdap/issues/12. "
        "Use backend='matplotlib' in the meantime."
    )
    raise NotImplementedError(msg)


def mosaic_plot(table: pd.DataFrame, **kwargs: Any) -> Any:
    """Mosaic plot for a two-way frequency table (Plotly).

    .. note::
       Implementation pending. Tracked in `GitHub Issue #12
       <https://github.com/nbx-liz/pycatdap/issues/12>`_.
    """
    _import_plotly()
    msg = (
        "Plotly backend for mosaic_plot is not yet implemented. "
        "See https://github.com/nbx-liz/pycatdap/issues/12. "
        "Use backend='matplotlib' in the meantime."
    )
    raise NotImplementedError(msg)
