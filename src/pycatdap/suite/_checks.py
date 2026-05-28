"""Standard checks for :mod:`pycatdap.suite` (H-0008 PR-D5).

Each check is a ``@dataclass(frozen=True)`` with its thresholds as
constructor arguments — no eval, no string DSL, no mid-run mutation.
The ``run`` method returns one :class:`CheckResult`; columns the check
flagged populate :attr:`CheckResult.affected_columns`.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from pycatdap._target_pair import target_summary
from pycatdap.eda import _detect_kind
from pycatdap.suite._base import CheckResult


def _require_response(response: str | None, df: pd.DataFrame, check_name: str) -> str:
    """Raise ValueError if response is None, KeyError if it is missing."""
    if response is None:
        msg = f"{check_name}: response is required for this check"
        raise ValueError(msg)
    if response not in df.columns:
        msg = f"{check_name}: response column not found: {response!r}"
        raise KeyError(msg)
    return response


@dataclass(frozen=True)
class ConstantColumnCheck:
    """Flag columns whose non-null values are all identical.

    A constant column carries no information for AIC modelling and is
    almost always a data-collection bug.
    """

    name: str = "ConstantColumnCheck"

    def run(self, df: pd.DataFrame, *, response: str | None = None) -> CheckResult:
        affected = [str(col) for col in df.columns if df[col].nunique(dropna=True) <= 1]
        passed = not affected
        return CheckResult(
            name=self.name,
            passed=passed,
            severity="warning",
            message=(
                "no constant columns"
                if passed
                else f"{len(affected)} constant column(s): {', '.join(affected)}"
            ),
            metric=float(len(affected)),
            affected_columns=tuple(affected),
        )


@dataclass(frozen=True)
class HighCardinalityCheck:
    """Flag categorical-like columns whose cardinality is suspiciously high.

    The default thresholds mirror :data:`pycatdap._quality._DEFAULT_QUALITY_THRESHOLDS`:
    a column triggers when ``n_unique > max_categories`` AND
    ``n_unique / n_obs > max_ratio``.
    """

    name: str = "HighCardinalityCheck"
    max_categories: int = 50
    max_ratio: float = 0.5

    def run(self, df: pd.DataFrame, *, response: str | None = None) -> CheckResult:
        affected: list[str] = []
        worst_ratio = 0.0
        for col in df.columns:
            series = df[col]
            n_obs = int(series.notna().sum())
            if n_obs == 0:
                continue
            n_unique = int(series.nunique(dropna=True))
            ratio = n_unique / n_obs
            if n_unique > self.max_categories and ratio > self.max_ratio:
                affected.append(str(col))
                worst_ratio = max(worst_ratio, ratio)
        passed = not affected
        return CheckResult(
            name=self.name,
            passed=passed,
            severity="info",
            message=(
                "no high-cardinality columns"
                if passed
                else (
                    f"{len(affected)} column(s) exceed cardinality threshold "
                    f"(max_categories={self.max_categories}, "
                    f"max_ratio={self.max_ratio}): {', '.join(affected)}"
                )
            ),
            metric=worst_ratio if affected else 0.0,
            affected_columns=tuple(affected),
        )


@dataclass(frozen=True)
class IndependenceCheck:
    """Flag explanatory columns that are NOT informative about response.

    A column is "independent" of the response when its ΔAIC against
    the response exceeds ``delta_aic_max``. The CATDAP convention is
    that ΔAIC ≤ 0 means the column is informative (adding it improves
    the AIC); ΔAIC > 0 means the column is noise that doesn't recoup
    the model-complexity penalty.
    """

    name: str = "IndependenceCheck"
    delta_aic_max: float = 0.0

    def run(self, df: pd.DataFrame, *, response: str | None = None) -> CheckResult:
        resp = _require_response(response, df, self.name)
        affected: list[str] = []
        worst_delta_aic = float("-inf")
        for col in df.columns:
            if col == resp:
                continue
            s = target_summary(df, target=resp, explanatory=col)
            if s.delta_aic > self.delta_aic_max:
                affected.append(str(col))
                worst_delta_aic = max(worst_delta_aic, s.delta_aic)
        passed = not affected
        return CheckResult(
            name=self.name,
            passed=passed,
            severity="warning",
            message=(
                f"every explanatory has ΔAIC ≤ {self.delta_aic_max}"
                if passed
                else (
                    f"{len(affected)} column(s) with ΔAIC > "
                    f"{self.delta_aic_max} vs {resp!r}: {', '.join(affected)}"
                )
            ),
            metric=(
                worst_delta_aic
                if affected and worst_delta_aic != float("-inf")
                else 0.0
            ),
            affected_columns=tuple(affected),
        )


@dataclass(frozen=True)
class PoolingSuggestionCheck:
    """Suggest continuous columns where AIC-optimal binning helps.

    For each continuous explanatory, compares the AIC of optimal
    binning (``bins=None`` → CATDAP-01 search) with the AIC of fixed
    equal-frequency binning (``bins=4``). When the optimal AIC beats
    the fixed AIC by more than ``min_improvement``, the column is
    suggested for explicit pooling.
    """

    name: str = "PoolingSuggestionCheck"
    min_improvement: float = 5.0
    fixed_bins: int = 4

    def run(self, df: pd.DataFrame, *, response: str | None = None) -> CheckResult:
        resp = _require_response(response, df, self.name)
        affected: list[str] = []
        worst_improvement = 0.0
        for col in df.columns:
            if col == resp:
                continue
            if _detect_kind(df[col]) != "continuous":
                continue
            try:
                s_opt = target_summary(df, target=resp, explanatory=col)
                s_fixed = target_summary(
                    df, target=resp, explanatory=col, bins=self.fixed_bins
                )
            except ValueError:  # pragma: no cover
                # Defensive: skip a column where target_summary refuses to
                # build a binning (e.g. exotic dtype, too few non-null
                # observations). Suite must not crash on a single bad
                # column. No reliable fixture exists today, hence the
                # pragma — remove the pragma if a regression introduces
                # one.
                continue
            # Lower delta_aic = better model. Improvement = fixed - optimal.
            improvement = float(s_fixed.delta_aic - s_opt.delta_aic)
            if improvement > self.min_improvement:
                affected.append(str(col))
                worst_improvement = max(worst_improvement, improvement)
        passed = not affected
        return CheckResult(
            name=self.name,
            passed=passed,
            severity="info",
            message=(
                "no continuous columns benefit from pooling beyond "
                f"min_improvement={self.min_improvement}"
                if passed
                else (
                    f"{len(affected)} continuous column(s) gain >"
                    f"{self.min_improvement} ΔAIC from optimal binning: "
                    f"{', '.join(affected)}"
                )
            ),
            metric=worst_improvement,
            affected_columns=tuple(affected),
        )


__all__ = [
    "ConstantColumnCheck",
    "HighCardinalityCheck",
    "IndependenceCheck",
    "PoolingSuggestionCheck",
]
