"""Tiny registry for pluggable association measures (H-0008 PR-D4).

A measure is any callable matching the signature
``Callable[[npt.NDArray[np.float64]], float]`` — i.e. it takes a 2D
contingency table of frequencies and returns a single association
score.

The registry is intentionally minimal: no namespacing, no validation,
no introspection. Custom measures register themselves at import time
via :func:`register`. The standard measures (``"aic"`` / ``"cramers_v"``
/ ``"mutual_info"``) are pre-registered by :mod:`pycatdap.measures`.

There is **no** ``unregister`` function on purpose: hot-swapping a
named measure mid-run leads to non-deterministic
``association_matrix`` results that vary by import order. Tests that
need to clean up after themselves should pop from
``_REGISTRY`` directly.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import numpy.typing as npt

Measure = Callable[[npt.NDArray[np.float64]], float]

_REGISTRY: dict[str, Measure] = {}


def register(name: str, fn: Measure) -> None:
    """Register a measure callable under ``name``.

    Subsequent calls with the same ``name`` overwrite silently — by
    design, so user code can re-import a module that defines its own
    measure without raising on the second pass.

    Parameters
    ----------
    name : str
        Lookup key for :func:`get`.
    fn : Callable[[npt.NDArray[np.float64]], float]
        The measure callable.
    """
    _REGISTRY[name] = fn


def get(name: str) -> Measure:
    """Look up a measure by name.

    Parameters
    ----------
    name : str
        Registered name.

    Returns
    -------
    Measure
        The callable previously passed to :func:`register`.

    Raises
    ------
    KeyError
        If ``name`` is not registered.
    """
    if name not in _REGISTRY:
        msg = f"measure {name!r} is not registered"
        raise KeyError(msg)
    return _REGISTRY[name]


def list_measures() -> list[str]:
    """Return the sorted list of registered measure names."""
    return sorted(_REGISTRY.keys())


__all__ = ["Measure", "get", "list_measures", "register"]
