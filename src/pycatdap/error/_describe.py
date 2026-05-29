"""Natural-language description builders for discovered error slices
(H-0014 PR-L2).

Pure, side-effect-free string helpers shared by :mod:`pycatdap.error._slice`
(the ``ErrorSlice.description`` field) and the discovery engine
(:mod:`pycatdap.error.discovery`, PR-L3). Keeping them here makes the
description grammar independently testable and lets
``to_divexplorer_format`` reuse the exact same rendering.

Grammar
-------
A slice is an AND of per-variable conditions joined by ``" × "``:

- categorical:  ``"marital_status = Never-married"``
- binned numeric (interval value): ``"age ∈ [45, 60]"``

A value is treated as an *interval* (and rendered with ``∈``) when it
begins with ``[`` or ``(`` — otherwise it is an equality (``=``).
"""

from __future__ import annotations

import math
import re
from collections.abc import Sequence

#: Multi-condition join separator (matches Issue #20 acceptance string).
_JOIN = " × "

#: Membership glyph for bounded-interval conditions.
_MEMBER = " ∈ "

#: Equality glyph for categorical conditions.
_EQ = " = "

#: A bounded interval label produced by :func:`interval_label`, e.g.
#: ``"[45, 60]"``. Requires the comma so categorical values that merely
#: start with a bracket (``"[High]"``, ``"(Other)"``) are NOT misread as
#: intervals (HIGH review finding).
_INTERVAL_RE = re.compile(r"^\[[^,]+,[^,]+\]$")

#: A one-sided bound label, e.g. ``"< 45"`` / ``">= 60"``.
_ONESIDED_RE = re.compile(r"^(?:< |>= )\S")


def fmt_number(x: float) -> str:
    """Render a float without a trailing ``.0`` for integer-valued bounds.

    ``45.0 -> "45"``, ``45.5 -> "45.5"``. Non-finite values render as
    ``"-inf"`` / ``"inf"``.

    Parameters
    ----------
    x : float
        The numeric value to format.

    Returns
    -------
    str
        Compact string form.
    """
    if math.isinf(x):
        return "-inf" if x < 0 else "inf"
    if math.isnan(x):
        return "nan"
    # Strip a trailing ``.0`` only for moderate integer-valued bounds;
    # huge floats (``1e20``) would otherwise expand to a 20+ digit int
    # string (review finding). Bin boundaries are never that large.
    if abs(x) < 1e15 and x == int(x):
        return str(int(x))
    return str(x)


def interval_label(code: int, boundaries: Sequence[float]) -> str:
    """Build an interval label for AIC-pooled bin ``code``.

    ``boundaries`` are the ``len(n_bins) - 1`` internal cut points from
    :class:`pycatdap._pooling.PoolingResult`. Bins are half-open
    ``[low, high)`` internally but rendered with closed brackets
    ``[low, high]`` to match the Issue #20 acceptance string; the edge
    bins render one-sided (``< high`` / ``>= low``).

    Parameters
    ----------
    code : int
        Bin code in ``range(len(boundaries) + 1)``.
    boundaries : sequence of float
        Sorted internal boundary values.

    Returns
    -------
    str
        e.g. ``"[45, 60]"``, ``"< 45"``, ``">= 60"``.

    Raises
    ------
    ValueError
        If ``code`` is outside ``range(len(boundaries) + 1)``.
    """
    n = len(boundaries)
    if code < 0 or code > n:
        msg = f"bin code {code} out of range for {n} boundaries"
        raise ValueError(msg)
    if n == 0:
        # Single bin spanning the whole range.
        return "(all)"
    if code == 0:
        return f"< {fmt_number(float(boundaries[0]))}"
    if code == n:
        return f">= {fmt_number(float(boundaries[-1]))}"
    low = fmt_number(float(boundaries[code - 1]))
    high = fmt_number(float(boundaries[code]))
    return f"[{low}, {high}]"


def format_condition(column: str, value: str) -> str:
    """Render a single ``(column, value)`` condition.

    - bounded interval (``"[45, 60]"``) → ``"age ∈ [45, 60]"``
    - one-sided bound (``"< 45"`` / ``">= 60"``) → ``"age < 45"``
      (the operator is already in the value)
    - otherwise categorical → ``"marital_status = Never-married"``

    The interval detection requires the canonical shapes produced by
    :func:`interval_label`, so categorical values that merely look
    bracketed (``"[High]"``, ``"(Other)"``) are rendered as equalities.

    Parameters
    ----------
    column : str
        Variable name.
    value : str
        Category label or interval label.

    Returns
    -------
    str
    """
    if _INTERVAL_RE.match(value):
        return f"{column}{_MEMBER}{value}"
    if _ONESIDED_RE.match(value):
        return f"{column} {value}"
    return f"{column}{_EQ}{value}"


def build_description(conditions: Sequence[tuple[str, str]]) -> str:
    """Join per-variable conditions into a single slice description.

    Parameters
    ----------
    conditions : sequence of (str, str)
        ``(column, value)`` pairs.

    Returns
    -------
    str
        ``" × "``-joined description, e.g.
        ``"age ∈ [45, 60] × marital_status = Never-married"``. Empty
        string for an empty condition list (the whole-dataset slice).
    """
    return _JOIN.join(format_condition(col, val) for col, val in conditions)
