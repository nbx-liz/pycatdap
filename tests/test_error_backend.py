"""Tests for the shared plot-backend dispatch (H-0014 PR-L1).

Verifies that the extracted :mod:`pycatdap.error._backend` dispatch is
behaviour-equivalent to the per-module helpers it replaced, and that all
three original consumers now resolve to the same single source of truth.
"""

from __future__ import annotations

import pytest

from pycatdap.error import _backend
from pycatdap.error._backend import get_backend_module


def test_matplotlib_dispatch() -> None:
    pytest.importorskip("matplotlib")
    from pycatdap.plot import matplotlib as expected

    assert get_backend_module("matplotlib") is expected


def test_plotly_dispatch() -> None:
    pytest.importorskip("plotly")
    from pycatdap.plot import plotly as expected

    assert get_backend_module("plotly") is expected


def test_unknown_backend_raises() -> None:
    with pytest.raises(ValueError, match="Unknown plot backend"):
        get_backend_module("seaborn")  # type: ignore[arg-type]


def test_consumers_share_single_dispatch() -> None:
    """confusion/residual/calibration must reference the extracted helper."""
    from pycatdap.error import calibration, confusion, residual

    assert confusion._get_backend_module is _backend.get_backend_module
    assert residual._get_backend_module is _backend.get_backend_module
    assert calibration._get_backend_module is _backend.get_backend_module


def test_backend_literal_shared() -> None:
    """The ``Backend`` Literal alias is re-exported from the same module."""
    from pycatdap.error import calibration, confusion, residual

    assert confusion.Backend is _backend.Backend
    assert residual.Backend is _backend.Backend
    assert calibration.Backend is _backend.Backend
