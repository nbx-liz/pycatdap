"""CI-integrable suite of data-quality and independence checks (H-0008 PR-D5).

Implements the deepchecks-style API requested by Issue #15:

    import pycatdap

    suite = pycatdap.suite.AICIndependenceSuite(df, response="symptoms")
    result = suite.run()
    assert result.passed, result.summary()

Individual checks are also usable on their own:

    pycatdap.suite.HighCardinalityCheck(max_categories=50).run(df)

Safety
------
Every :class:`Check` is a frozen dataclass. The suite never uses
``eval()`` / ``exec()`` / string-based DSL — the contracts are pure
Python data, so the suite is safe to run on CI against untrusted
DataFrames.
"""

from __future__ import annotations

from pycatdap.suite._base import (
    Check,
    CheckResult,
    Severity,
    SuiteResult,
)
from pycatdap.suite._checks import (
    ConstantColumnCheck,
    HighCardinalityCheck,
    IndependenceCheck,
    PoolingSuggestionCheck,
)
from pycatdap.suite._suites import AICIndependenceSuite

__all__ = [
    "AICIndependenceSuite",
    "Check",
    "CheckResult",
    "ConstantColumnCheck",
    "HighCardinalityCheck",
    "IndependenceCheck",
    "PoolingSuggestionCheck",
    "Severity",
    "SuiteResult",
]
