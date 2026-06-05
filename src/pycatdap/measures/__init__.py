"""Pluggable association measures (H-0008 PR-D4, BLUEPRINT §5.11).

Each measure has the uniform signature
``Callable[[npt.NDArray[np.float64]], float]`` — it takes a 2D
contingency table of frequencies and returns a single association
score.

Standard measures provided
--------------------------
- :func:`aic` — ΔAIC (negative = informative)
- :func:`cramers_v` — Cramér's V (0..1, 0 = independent)
- :func:`mutual_info` — mutual information in nats (≥ 0, 0 = independent)

Registry
--------
- :func:`register` — register a custom measure under a name
- :func:`get` — look up a measure by name
- :func:`list_measures` — list registered measure names

The three standard measures register themselves at import time, so
:func:`pycatdap.measures.get("aic")` returns :func:`aic` without any
extra setup.
"""

from __future__ import annotations

from typing import Any

from pycatdap.measures._aic import aic
from pycatdap.measures._cramers_v import cramers_v
from pycatdap.measures._mutual_info import mutual_info
from pycatdap.measures._registry import Measure, get, list_measures, register

# Pre-register the standard measures so `get("aic")` etc. work on import.
register("aic", aic)
register("cramers_v", cramers_v)
register("mutual_info", mutual_info)


__all__ = [
    "AICMeasure",
    "Measure",
    "aic",
    "cramers_v",
    "get",
    "list_measures",
    "mutual_info",
    "register",
]


def __getattr__(name: str) -> Any:
    """Lazily expose the optional pysubgroup bridge (PEP 562).

    ``AICMeasure`` lives in :mod:`pycatdap.measures._pysubgroup`, which
    imports pysubgroup at module load. Resolving it lazily keeps
    ``import pycatdap.measures`` free of any hard dependency on pysubgroup;
    accessing ``AICMeasure`` without pysubgroup installed raises the
    bridge module's ``ImportError`` pointing at the ``pycatdap[subgroup]``
    extra.
    """
    if name == "AICMeasure":
        from pycatdap.measures._pysubgroup import AICMeasure

        return AICMeasure
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
