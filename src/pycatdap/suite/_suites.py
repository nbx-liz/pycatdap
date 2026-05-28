"""Preset suite bundles (H-0008 PR-D5).

A *suite* is a bound (DataFrame, response, list[Check]) triple plus a
``.run()`` method that executes every check and packages the per-check
outcomes into a :class:`SuiteResult`.

``AICIndependenceSuite`` is the default bundle requested by Issue #15:

    suite = pycatdap.suite.AICIndependenceSuite(df, response="symptoms")
    result = suite.run()
    assert result.passed, result.summary()
"""

from __future__ import annotations

import pandas as pd

from pycatdap.suite._base import Check, CheckResult, SuiteResult
from pycatdap.suite._checks import (
    ConstantColumnCheck,
    HighCardinalityCheck,
    IndependenceCheck,
    PoolingSuggestionCheck,
)


def _default_checks() -> list[Check]:
    """Default bundle for AICIndependenceSuite."""
    return [
        ConstantColumnCheck(),
        HighCardinalityCheck(),
        IndependenceCheck(),
        PoolingSuggestionCheck(),
    ]


class AICIndependenceSuite:
    """Preset suite bundling the four standard data-quality + independence checks.

    Parameters
    ----------
    df : DataFrame
        Frame to evaluate.
    response : str or None
        Response column; required for :class:`IndependenceCheck` and
        :class:`PoolingSuggestionCheck`. Pass ``None`` to skip
        response-dependent checks (you must also override ``checks``
        in that case).
    checks : sequence of Check or None
        Overrides the default bundle. ``None`` (default) uses
        :func:`_default_checks`.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> suite = pycatdap.suite.AICIndependenceSuite(df, response="Survived")
    >>> result = suite.run()
    >>> isinstance(result.passed, bool)
    True
    """

    name: str = "AICIndependenceSuite"

    def __init__(
        self,
        df: pd.DataFrame,
        *,
        response: str | None = None,
        checks: list[Check] | None = None,
    ) -> None:
        self._df = df
        self._response = response
        self._checks: list[Check] = (
            list(checks) if checks is not None else _default_checks()
        )

    def run(self) -> SuiteResult:
        """Execute every check and return the aggregated :class:`SuiteResult`."""
        results: list[CheckResult] = []
        for check in self._checks:
            results.append(check.run(self._df, response=self._response))
        n_rows, n_cols = self._df.shape
        return SuiteResult(
            suite_name=self.name,
            checks=tuple(results),
            n_rows=n_rows,
            n_cols=n_cols,
            response=self._response,
        )


__all__ = ["AICIndependenceSuite"]
