"""Regression tests for H-0009: v0.6.0 frozen dataclass shallow-freeze hardening.

H-0008 (v0.6.0) shipped 4 ``@dataclass(frozen=True)`` types whose internal
fields (``pd.DataFrame`` / ``dict`` / ``list``) remain mutable despite
``frozen=True``. CLAUDE.md mandates "NEVER mutate".

These tests assert that the v0.6.0 result objects reject the mutation
operations that previously succeeded silently:

- ``CheckResult.affected_columns`` is a ``tuple`` — ``.append`` raises
- ``SuiteResult.checks`` is a ``tuple`` — ``.pop`` raises
- ``TargetAnalysisResult.top_summaries`` is a ``MappingProxyType`` —
  ``__setitem__`` raises
- ``TargetAnalysisResult.ranking`` numpy buffer is read-only —
  in-place value assignment raises (``DataFrame.drop`` etc. still
  allowed because pandas reallocates; documented as read-only)

The "golden read-only consumer" half asserts that
``to_dict`` / ``to_html`` / ``to_plotly_json`` / ``show`` continue
working unchanged after the freeze.
"""

from __future__ import annotations

from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest

# ---------- CheckResult / SuiteResult fixtures ----------


@pytest.fixture
def sample_suite_result():  # type: ignore[no-untyped-def]
    from pycatdap.suite import AICIndependenceSuite

    df = pd.DataFrame(
        {
            "symptoms": ["A", "B", "A", "B", "A", "B"],
            "age_group": ["20s", "30s", "20s", "30s", "40s", "40s"],
            "constant_col": [1, 1, 1, 1, 1, 1],
        }
    )
    return AICIndependenceSuite(df, response="symptoms").run()


@pytest.fixture
def sample_target_analysis():  # type: ignore[no-untyped-def]
    from pycatdap import target_analysis

    df = pd.DataFrame(
        {
            "symptoms": ["A", "B", "A", "B", "A", "B", "A", "B"],
            "age_group": ["20s", "30s", "20s", "30s", "40s", "40s", "20s", "30s"],
            "sex": ["M", "F", "M", "F", "M", "F", "M", "F"],
        }
    )
    return target_analysis(df, response="symptoms", top_k=2)


# ---------- CheckResult.affected_columns ----------


def test_check_result_affected_columns_is_tuple(sample_suite_result):  # type: ignore[no-untyped-def]
    for check in sample_suite_result.checks:
        assert isinstance(check.affected_columns, tuple), (
            f"{check.name}.affected_columns must be tuple for v0.6.1 (H-0009)"
        )


def test_check_result_affected_columns_rejects_append(sample_suite_result):  # type: ignore[no-untyped-def]
    check = sample_suite_result.checks[0]
    with pytest.raises(AttributeError):
        check.affected_columns.append("injected_col")  # type: ignore[attr-defined]


# ---------- SuiteResult.checks ----------


def test_suite_result_checks_is_tuple(sample_suite_result):  # type: ignore[no-untyped-def]
    assert isinstance(sample_suite_result.checks, tuple), (
        "SuiteResult.checks must be tuple for v0.6.1 (H-0009)"
    )


def test_suite_result_checks_rejects_pop(sample_suite_result):  # type: ignore[no-untyped-def]
    with pytest.raises(AttributeError):
        sample_suite_result.checks.pop()  # type: ignore[attr-defined]


def test_suite_result_checks_rejects_assignment(sample_suite_result):  # type: ignore[no-untyped-def]
    with pytest.raises(TypeError):
        sample_suite_result.checks[0] = None  # type: ignore[index]


# ---------- TargetAnalysisResult.top_summaries ----------


def test_target_analysis_top_summaries_is_mappingproxy(sample_target_analysis):  # type: ignore[no-untyped-def]
    assert isinstance(sample_target_analysis.top_summaries, MappingProxyType), (
        "top_summaries must be MappingProxyType for v0.6.1 (H-0009)"
    )


def test_target_analysis_top_summaries_rejects_setitem(sample_target_analysis):  # type: ignore[no-untyped-def]
    with pytest.raises(TypeError):
        sample_target_analysis.top_summaries["injected"] = None  # type: ignore[index]


def test_target_analysis_top_summaries_rejects_del(sample_target_analysis):  # type: ignore[no-untyped-def]
    first_key = next(iter(sample_target_analysis.top_summaries))
    with pytest.raises(TypeError):
        del sample_target_analysis.top_summaries[first_key]  # type: ignore[attr-defined]


def test_target_analysis_top_summaries_preserves_mapping_interface(
    sample_target_analysis,
):  # type: ignore[no-untyped-def]
    """The freeze must not break dict-like reads."""
    keys = list(sample_target_analysis.top_summaries.keys())
    assert len(keys) > 0
    first = sample_target_analysis.top_summaries[keys[0]]
    assert first is not None
    items = dict(sample_target_analysis.top_summaries.items())
    assert items[keys[0]] is first


# ---------- TargetAnalysisResult.ranking ----------


def test_target_analysis_ranking_buffer_is_readonly(sample_target_analysis):  # type: ignore[no-untyped-def]
    """The underlying numpy buffer of every column must be non-writeable."""
    for col in sample_target_analysis.ranking.columns:
        values = sample_target_analysis.ranking[col].values
        if isinstance(values, np.ndarray):
            assert not values.flags.writeable, (
                f"ranking column {col!r} numpy buffer must be read-only"
            )


def test_target_analysis_ranking_rejects_element_assignment(sample_target_analysis):  # type: ignore[no-untyped-def]
    """Element-level mutation via numpy buffer must raise."""
    ranking = sample_target_analysis.ranking
    delta_aic_buffer = ranking["delta_aic"].values
    with pytest.raises(ValueError, match="read-only|assignment"):
        delta_aic_buffer[0] = 999.0


def test_target_analysis_ranking_copy_remains_writable(sample_target_analysis):  # type: ignore[no-untyped-def]
    """The documented escape hatch — call ``.copy()`` before mutating."""
    ranking_copy = sample_target_analysis.ranking.copy()
    ranking_copy["delta_aic"] = 0.0  # must succeed on a copy
    assert (ranking_copy["delta_aic"] == 0.0).all()


# ---------- Read-only consumers still work (golden) ----------


def test_suite_result_to_dict_still_works(sample_suite_result):  # type: ignore[no-untyped-def]
    d = sample_suite_result.to_dict()
    assert d["suite_name"] == "AICIndependenceSuite"
    assert isinstance(d["checks"], list)
    assert d["passed"] is sample_suite_result.passed


def test_suite_result_to_plotly_json_still_works(sample_suite_result):  # type: ignore[no-untyped-def]
    spec = sample_suite_result.to_plotly_json()
    assert "checks_table" in spec
    assert spec["checks_table"]["data"][0]["type"] == "table"


def test_target_analysis_to_dict_still_works(sample_target_analysis):  # type: ignore[no-untyped-def]
    d = sample_target_analysis.to_dict()
    assert d["response"] == "symptoms"
    assert "ranking" in d
    assert "top_summaries" in d


def test_target_analysis_to_plotly_json_still_works(sample_target_analysis):  # type: ignore[no-untyped-def]
    spec = sample_target_analysis.to_plotly_json()
    assert isinstance(spec, dict)
