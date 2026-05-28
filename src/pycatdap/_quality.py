"""Shared quality-scan helpers (H-0008 PR-D1).

Lifted out of :mod:`pycatdap.profile` so that the upcoming
:func:`pycatdap.quality_report` (H-0008 PR-D2) and :mod:`pycatdap.suite`
(PR-D5) can reuse the same warning logic without circular imports.

This module is intentionally side-effect-free: callers build their
``Sequence[_QualitySubject]`` (typically ``list[VariableCard]``) and
pass it in. The Protocol keeps :mod:`_quality` independent of
:mod:`profile`, so :mod:`profile` can import from here without a cycle.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Protocol

import pandas as pd

WarningKind = Literal["high_cardinality", "constant", "id_candidate", "high_missing"]
WarningSeverity = Literal["info", "warning"]


_DEFAULT_QUALITY_THRESHOLDS: dict[str, float] = {
    "high_cardinality": 0.5,  # nunique / n_obs threshold
    "high_cardinality_abs_min": 50.0,  # AND nunique > this
    "high_missing": 0.5,
}


@dataclass(frozen=True)
class QualityWarning:
    """One quality finding emitted by :func:`_scan_quality`.

    Attributes
    ----------
    severity : {"info", "warning"}
        Severity tag for UI rendering.
    kind : {"high_cardinality", "constant", "id_candidate", "high_missing"}
        The specific finding category.
    column : str
        Affected column name.
    message : str
        Human-readable description.
    metric : float
        The numeric value that triggered the warning (e.g. missing rate,
        cardinality ratio).
    """

    severity: WarningSeverity
    kind: WarningKind
    column: str
    message: str
    metric: float


class _QualitySubject(Protocol):
    """Structural type that :func:`_scan_quality` consumes.

    :class:`pycatdap.profile.VariableCard` satisfies this by attribute
    shape — no inheritance required. Keeping :mod:`_quality` Protocol-
    typed avoids importing :class:`VariableCard`, which would create a
    cycle with :mod:`pycatdap.profile`.

    Attributes are declared as ``@property`` so the Protocol matches both
    frozen and mutable dataclasses: a bare ``name: str`` annotation on a
    Protocol implies the attribute is settable, which excludes
    ``frozen=True`` dataclasses like ``VariableCard`` from the structural
    match.
    """

    @property
    def name(self) -> str: ...
    @property
    def kind(self) -> str: ...
    @property
    def n_obs(self) -> int: ...
    @property
    def n_missing(self) -> int: ...
    @property
    def n_unique(self) -> int: ...


def _scan_quality(
    df: pd.DataFrame,
    cards: Sequence[_QualitySubject],
    thresholds: dict[str, float],
) -> list[QualityWarning]:
    """Emit data-quality warnings for each column card.

    Parameters
    ----------
    df : DataFrame
        The source frame. Currently unused inside the loop (the cards
        already carry the aggregated stats) but kept on the signature
        for forward compatibility with checks that need column dtypes
        or sample values.
    cards : sequence of _QualitySubject
        Per-column summary objects (typically ``list[VariableCard]``).
    thresholds : dict
        Must contain ``"high_cardinality"`` (ratio), ``"high_cardinality_abs_min"``
        (nunique floor), and ``"high_missing"`` (rate). See
        :data:`_DEFAULT_QUALITY_THRESHOLDS`.

    Returns
    -------
    list[QualityWarning]
        Warnings in column order. A constant column short-circuits the
        remaining checks for that column (other warnings would double-
        trigger).
    """
    del df  # currently unused; kept for API symmetry with future checks
    warnings: list[QualityWarning] = []
    high_card_ratio = thresholds["high_cardinality"]
    high_card_abs = thresholds["high_cardinality_abs_min"]
    high_missing = thresholds["high_missing"]

    for card in cards:
        # n_obs == 0 would require a zero-row DataFrame, which fails earlier
        # inside association_matrix; no defensive check needed here.
        missing_rate = card.n_missing / card.n_obs

        if missing_rate > high_missing:
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="high_missing",
                    column=card.name,
                    message=(
                        f"{missing_rate * 100:.1f}% of values are missing "
                        f"(threshold {high_missing * 100:.0f}%)"
                    ),
                    metric=missing_rate,
                )
            )

        if card.n_unique <= 1:
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="constant",
                    column=card.name,
                    message="column has at most one distinct non-null value",
                    metric=float(card.n_unique),
                )
            )
            continue  # other warnings would double-trigger

        if (
            card.kind in {"categorical", "other"}
            and card.n_unique == card.n_obs - card.n_missing
        ):
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="id_candidate",
                    column=card.name,
                    message="every non-null value is unique (identifier?)",
                    metric=1.0,
                )
            )
            continue

        unique_ratio = card.n_unique / card.n_obs if card.n_obs else 0.0
        if unique_ratio > high_card_ratio and card.n_unique > high_card_abs:
            warnings.append(
                QualityWarning(
                    severity="info",
                    kind="high_cardinality",
                    column=card.name,
                    message=(
                        f"{card.n_unique} distinct values "
                        f"({unique_ratio * 100:.1f}% of rows; threshold "
                        f"{high_card_ratio * 100:.0f}% and > "
                        f"{int(high_card_abs)})"
                    ),
                    metric=unique_ratio,
                )
            )

    return warnings


__all__ = [
    "QualityWarning",
    "WarningKind",
    "WarningSeverity",
    "_DEFAULT_QUALITY_THRESHOLDS",
    "_QualitySubject",
    "_scan_quality",
]
