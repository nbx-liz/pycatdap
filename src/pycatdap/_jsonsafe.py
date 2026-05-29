"""JSON-safety helper shared by ``to_plotly_json`` / ``to_dict`` writers.

NaN and +/-Infinity are not valid JSON (RFC 8259) and break strict browser
parsers such as ``JSON.parse`` behind ``react-plotly.js``.  Every public result
object's ``.to_plotly_json()`` must round-trip through
``json.dumps(..., allow_nan=False)`` -- the contract enforced by
``tests/contract/test_plotly_json_contract.py`` (see HISTORY.md H-0015 §A and
BLUEPRINT.md §5.7 / DP-4).
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def scalar_to_json(v: Any) -> Any:
    """Convert a pandas/numpy scalar to a JSON-friendly value.

    Returns ``None`` for NA, NaN, and +/-inf (the latter two are not valid
    JSON per RFC 8259 and break strict JS parsers); preserves finite numerics
    as ``float``; falls back to ``str`` for anything else.

    Parameters
    ----------
    v : Any
        A scalar cell value (pandas/numpy/python scalar).

    Returns
    -------
    Any
        ``None``, a finite ``float``, or a ``str``.
    """
    if pd.isna(v):
        return None
    if isinstance(v, (int, float, np.floating, np.integer)):
        f = float(v)
        return f if np.isfinite(f) else None
    return str(v)
