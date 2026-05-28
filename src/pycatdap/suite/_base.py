"""Suite base types (H-0008 PR-D5).

deepchecks-style CI-integrable suite per Issue #15. Each individual
:class:`Check` is a frozen dataclass exposing a ``run`` method that
returns a single :class:`CheckResult`. :class:`SuiteResult` aggregates
multiple :class:`CheckResult` instances and exposes the canonical
``.passed`` boolean for CI assertions:

    suite = AICIndependenceSuite(df, response="symptoms")
    result = suite.run()
    assert result.passed, result.summary()

Safety
------
Every Check is a frozen dataclass. The suite never uses ``eval()`` /
``exec()`` / string-based DSL — the contracts are pure Python data, so
the suite is safe to run on CI against untrusted DataFrames.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Protocol

import pandas as pd

Severity = Literal["info", "warning"]


@dataclass(frozen=True)
class CheckResult:
    """The outcome of running a single :class:`Check`.

    Attributes
    ----------
    name : str
        Class name of the check that produced this result.
    passed : bool
        ``True`` when the check found nothing actionable, ``False``
        when it flagged at least one column / row.
    severity : {"info", "warning"}
        ``"warning"`` failures flip the parent :attr:`SuiteResult.passed`
        to ``False``; ``"info"`` failures are advisory only.
    message : str
        Human-readable summary describing the finding.
    metric : float or None
        Aggregated numeric metric the check used (e.g. worst-column
        cardinality ratio). ``None`` when no single metric makes sense.
    affected_columns : list[str]
        Column names the check flagged. Empty when ``passed`` is True.
    """

    name: str
    passed: bool
    severity: Severity
    message: str
    metric: float | None
    affected_columns: list[str]


class Check(Protocol):
    """Structural type for a check class.

    Implementations are typically frozen dataclasses so their
    thresholds are immutable after construction (no mid-run mutation
    of the contract).

    ``name`` is declared as ``@property`` so frozen dataclasses (whose
    attributes are effectively read-only) can satisfy this Protocol
    under ``mypy --strict``.
    """

    @property
    def name(self) -> str: ...

    def run(
        self,
        df: pd.DataFrame,
        *,
        response: str | None = None,
    ) -> CheckResult: ...


@dataclass(frozen=True)
class SuiteResult:
    """Aggregated result of running a :class:`Suite`.

    Attributes
    ----------
    suite_name : str
        Class name of the suite that produced this result.
    checks : list[CheckResult]
        Per-check outcomes in execution order.
    n_rows, n_cols : int
        Shape of the inspected frame.
    response : str or None
        Response column the suite was bound to, if any.
    """

    suite_name: str
    checks: list[CheckResult]
    n_rows: int
    n_cols: int
    response: str | None

    @property
    def passed(self) -> bool:
        """``True`` iff no ``"warning"``-severity check failed.

        ``"info"``-severity failures (e.g. high cardinality) do NOT
        flip ``passed`` to ``False`` — they are advisory only.
        """
        return not any((not c.passed) and c.severity == "warning" for c in self.checks)

    @property
    def warnings(self) -> list[CheckResult]:
        """Sub-list of checks that did NOT pass, in original order."""
        return [c for c in self.checks if not c.passed]

    def summary(self) -> str:
        """One-line summary suitable for an ``assert`` message."""
        if not self.warnings:
            return (
                f"{self.suite_name}: all {len(self.checks)} checks passed "
                f"({self.n_rows} rows × {self.n_cols} cols)"
            )
        by_sev: Counter[str] = Counter(c.severity for c in self.warnings)
        sev_str = ", ".join(f"{n} {sev}" for sev, n in sorted(by_sev.items()))
        failing = ", ".join(c.name for c in self.warnings)
        return (
            f"{self.suite_name}: {len(self.warnings)} of {len(self.checks)} "
            f"checks failed ({sev_str}) — {failing}"
        )

    def show(self) -> None:
        """Render the result inline (Jupyter) or print to stdout."""
        header = (
            f"SuiteResult[{self.suite_name}] — "
            f"{self.n_rows} rows × {self.n_cols} cols · "
            f"{'passed' if self.passed else 'failed'}"
        )
        try:
            from IPython.display import display
        except ImportError:
            print(header)
            print(self.summary())
            if self.checks:
                print(self._checks_table().to_string())
            return

        print(header)
        display(self.summary())
        if self.checks:
            display(self._checks_table())

    def _checks_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "check": c.name,
                    "passed": c.passed,
                    "severity": c.severity,
                    "metric": c.metric,
                    "affected": ", ".join(c.affected_columns)
                    if c.affected_columns
                    else "",
                    "message": c.message,
                }
                for c in self.checks
            ]
        )

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a single-file HTML report (jinja2)."""
        try:
            from jinja2 import Environment, select_autoescape
        except ImportError as exc:
            msg = (
                "jinja2 is required for HTML reports. "
                "Install it with: pip install 'pycatdap[plotly]'"
            )
            raise ImportError(msg) from exc

        from importlib.resources import files as _resource_files

        template_text = (
            _resource_files("pycatdap.templates")
            .joinpath("suite_result.html.j2")
            .read_text(encoding="utf-8")
        )
        env = Environment(autoescape=select_autoescape(default=True))
        template = env.from_string(template_text)

        from pycatdap._version import __version__

        html = template.render(
            suite_name=self.suite_name,
            response=self.response,
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            checks=self.checks,
            passed=self.passed,
            summary_line=self.summary(),
            pycatdap_version=__version__,
        )

        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")

        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return {
            "suite_name": self.suite_name,
            "response": self.response,
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "passed": self.passed,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "severity": c.severity,
                    "message": c.message,
                    "metric": c.metric,
                    "affected_columns": list(c.affected_columns),
                }
                for c in self.checks
            ],
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return a Plotly Table spec for the checks list (DP-4)."""
        return {"checks_table": _checks_table_spec(self.checks)}


def _checks_table_spec(checks: Sequence[CheckResult]) -> dict[str, Any]:
    return {
        "data": [
            {
                "type": "table",
                "header": {
                    "values": [
                        "check",
                        "passed",
                        "severity",
                        "metric",
                        "affected",
                        "message",
                    ],
                    "align": "left",
                },
                "cells": {
                    "values": [
                        [c.name for c in checks],
                        [c.passed for c in checks],
                        [c.severity for c in checks],
                        [c.metric for c in checks],
                        [", ".join(c.affected_columns) for c in checks],
                        [c.message for c in checks],
                    ],
                    "align": "left",
                },
            }
        ],
        "layout": {"title": "Suite checks"},
    }


__all__ = [
    "Check",
    "CheckResult",
    "Severity",
    "SuiteResult",
]
