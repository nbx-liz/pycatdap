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

from pycatdap.measures._aic import aic
from pycatdap.measures._cramers_v import cramers_v
from pycatdap.measures._mutual_info import mutual_info
from pycatdap.measures._registry import Measure, get, list_measures, register

# Pre-register the standard measures so `get("aic")` etc. work on import.
register("aic", aic)
register("cramers_v", cramers_v)
register("mutual_info", mutual_info)


__all__ = [
    "Measure",
    "aic",
    "cramers_v",
    "get",
    "list_measures",
    "mutual_info",
    "register",
]
