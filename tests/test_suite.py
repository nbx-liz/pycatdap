"""Tests for :mod:`pycatdap.suite` (H-0008 PR-D5).

Deepchecks-style CI-integrable suite per Issue #15. Each :class:`Check`
is a frozen dataclass — no ``eval()`` / ``exec()`` / string-based DSL
so the suite is safe to run on untrusted DataFrames inside CI.

The :class:`AICIndependenceSuite` preset bundles the four standard
checks for the common 'data quality + variables informative about
response' workflow.
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap.suite import (
    AICIndependenceSuite,
    CheckResult,
    ConstantColumnCheck,
    HighCardinalityCheck,
    IndependenceCheck,
    PoolingSuggestionCheck,
    SuiteResult,
)

# -- fixtures --------------------------------------------------------------


@pytest.fixture()
def df_clean() -> pd.DataFrame:
    rng = np.random.default_rng(seed=11)
    n = 60
    cat = rng.choice(["a", "b"], size=n)
    return pd.DataFrame(
        {
            "y": np.where(cat == "a", "yes", "no"),
            "informative": cat,
            "noise_cat": rng.choice(["x", "y"], size=n),
        }
    )


@pytest.fixture()
def df_with_issues() -> pd.DataFrame:
    n = 200
    rng = np.random.default_rng(seed=23)
    return pd.DataFrame(
        {
            "y": rng.choice(["yes", "no"], size=n),
            "constant": ["x"] * n,
            "high_card_str": [f"v-{i % 150}" for i in range(n)],
            "informative": np.where(rng.choice([0, 1], size=n) == 0, "yes", "no"),
            "noise": rng.choice(["a", "b"], size=n),
        }
    )


# -- ConstantColumnCheck ---------------------------------------------------


class TestConstantColumnCheck:
    def test_passes_on_clean_frame(self, df_clean: pd.DataFrame) -> None:
        result = ConstantColumnCheck().run(df_clean)
        assert isinstance(result, CheckResult)
        assert result.passed is True
        assert result.affected_columns == ()

    def test_flags_constant_columns(self, df_with_issues: pd.DataFrame) -> None:
        result = ConstantColumnCheck().run(df_with_issues)
        assert result.passed is False
        assert "constant" in result.affected_columns
        assert result.severity == "warning"


# -- HighCardinalityCheck --------------------------------------------------


class TestHighCardinalityCheck:
    def test_passes_on_clean_frame(self, df_clean: pd.DataFrame) -> None:
        result = HighCardinalityCheck().run(df_clean)
        assert result.passed is True
        assert result.affected_columns == ()

    def test_flags_high_cardinality_columns(self, df_with_issues: pd.DataFrame) -> None:
        result = HighCardinalityCheck().run(df_with_issues)
        assert result.passed is False
        assert "high_card_str" in result.affected_columns
        # info severity per the existing _scan_quality convention
        assert result.severity == "info"

    def test_skips_all_nan_columns(self) -> None:
        """Columns with zero non-null observations must not contribute."""
        df = pd.DataFrame({"nans": [np.nan] * 100, "ok": list(range(100))})
        result = HighCardinalityCheck(max_categories=10).run(df)
        # `nans` has n_obs == 0, so it is silently skipped; verifies the
        # `if n_obs == 0: continue` branch is exercised.
        assert "nans" not in result.affected_columns

    def test_threshold_override(self, df_clean: pd.DataFrame) -> None:
        # Tighten thresholds to trip even the small clean fixture
        # (n_unique > 1 AND ratio > 0 — guaranteed for every column).
        result = HighCardinalityCheck(max_ratio=0.0, max_categories=1).run(df_clean)
        assert result.passed is False


# -- IndependenceCheck -----------------------------------------------------


class TestIndependenceCheck:
    def test_passes_when_all_variables_informative(
        self, df_clean: pd.DataFrame
    ) -> None:
        # `informative` has perfect ΔAIC vs y, `noise_cat` is independent
        # so default threshold (delta_aic_max=0.0) would flag noise_cat.
        # Use a permissive threshold so even noise passes.
        result = IndependenceCheck(delta_aic_max=10.0).run(df_clean, response="y")
        assert result.passed is True

    def test_flags_independent_variables_at_default_threshold(
        self, df_with_issues: pd.DataFrame
    ) -> None:
        result = IndependenceCheck().run(df_with_issues, response="y")
        assert result.passed is False
        # `noise` is independent of y by construction → should flag
        assert "noise" in result.affected_columns
        assert result.severity == "warning"

    def test_requires_response(self, df_clean: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="response"):
            IndependenceCheck().run(df_clean)

    def test_response_missing_raises_key_error(self, df_clean: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            IndependenceCheck().run(df_clean, response="not_a_column")


# -- PoolingSuggestionCheck ------------------------------------------------


class TestPoolingSuggestionCheck:
    def test_passes_when_no_continuous_columns(self, df_clean: pd.DataFrame) -> None:
        # df_clean has no continuous columns; check should pass
        result = PoolingSuggestionCheck().run(df_clean, response="y")
        assert result.passed is True
        assert result.affected_columns == ()

    def test_requires_response(self) -> None:
        df = pd.DataFrame({"y": [0, 1] * 50, "x": np.linspace(0, 1, 100)})
        with pytest.raises(ValueError, match="response"):
            PoolingSuggestionCheck().run(df)

    def test_suggests_pooling_for_informative_continuous(self) -> None:
        rng = np.random.default_rng(0)
        n = 200
        x = rng.normal(0, 1, size=n)
        # y depends strongly on x — AIC-optimal binning beats equal-frequency
        y = (x > 0).astype(int).astype(str)
        df = pd.DataFrame({"y": y, "x": x})
        # default min_improvement is small enough to flag this
        result = PoolingSuggestionCheck(min_improvement=1.0).run(df, response="y")
        assert "x" in result.affected_columns

    def test_silently_skips_degenerate_continuous_columns(self) -> None:
        """A continuous column with all-NaN values must not crash the check.

        target_summary raises ValueError on all-NaN explanatories; the
        check swallows that and moves on.
        """
        n = 100
        df = pd.DataFrame(
            {
                "y": ["a"] * 50 + ["b"] * 50,
                "bad_cont": [np.nan] * n,
            }
        )
        # Should not raise; bad_cont should not appear in affected_columns
        result = PoolingSuggestionCheck().run(df, response="y")
        assert "bad_cont" not in result.affected_columns


# -- AICIndependenceSuite --------------------------------------------------


class TestAICIndependenceSuite:
    def test_run_returns_suite_result(self, df_clean: pd.DataFrame) -> None:
        suite = AICIndependenceSuite(df_clean, response="y")
        result = suite.run()
        assert isinstance(result, SuiteResult)
        assert result.response == "y"
        assert result.n_rows == len(df_clean)
        assert result.n_cols == len(df_clean.columns)

    def test_default_bundles_four_checks(self, df_clean: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_clean, response="y").run()
        names = {c.name for c in result.checks}
        assert {
            "ConstantColumnCheck",
            "HighCardinalityCheck",
            "IndependenceCheck",
            "PoolingSuggestionCheck",
        } <= names

    def test_custom_checks_override_default(self, df_clean: pd.DataFrame) -> None:
        suite = AICIndependenceSuite(
            df_clean, response="y", checks=[ConstantColumnCheck()]
        )
        result = suite.run()
        assert [c.name for c in result.checks] == ["ConstantColumnCheck"]

    def test_passed_true_when_all_checks_pass(self) -> None:
        # build a frame where every default check passes
        df = pd.DataFrame(
            {
                "y": ["yes"] * 25 + ["no"] * 25,
                "x": ["yes"] * 25 + ["no"] * 25,  # perfectly informative
            }
        )
        result = AICIndependenceSuite(df, response="y").run()
        # informative passes IndependenceCheck; no constant; no high-card
        # (only 2 unique); no continuous → PoolingSuggestionCheck passes
        assert result.passed is True

    def test_passed_false_when_any_warning_check_fails(
        self, df_with_issues: pd.DataFrame
    ) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        assert result.passed is False


# -- SuiteResult -----------------------------------------------------------


class TestSuiteResult:
    def test_failures_returns_failed_checks(self, df_with_issues: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        failures = result.failures
        assert all(not c.passed for c in failures)

    def test_summary_returns_string(self, df_with_issues: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        s = result.summary()
        assert isinstance(s, str)
        # at least one failing check name appears
        failing = [c.name for c in result.checks if not c.passed]
        if failing:
            assert any(name in s for name in failing)

    def test_summary_when_all_pass(self) -> None:
        df = pd.DataFrame(
            {
                "y": ["yes"] * 25 + ["no"] * 25,
                "x": ["yes"] * 25 + ["no"] * 25,
            }
        )
        result = AICIndependenceSuite(df, response="y").run()
        s = result.summary()
        assert "passed" in s.lower()

    def test_show_falls_back_to_stdout(
        self,
        df_with_issues: pd.DataFrame,
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        import sys

        monkeypatch.setitem(sys.modules, "IPython", None)
        monkeypatch.setitem(sys.modules, "IPython.display", None)
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        result.show()
        out = capsys.readouterr().out
        assert "SuiteResult" in out

    def test_show_uses_ipython_when_available(
        self,
        df_with_issues: pd.DataFrame,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        pytest.importorskip("IPython")
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        result.show()
        out = capsys.readouterr().out
        assert "SuiteResult" in out

    def test_to_dict_is_json_serializable(self, df_with_issues: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        d = result.to_dict()
        assert d["passed"] in (True, False)
        assert "checks" in d
        json.dumps(d)

    def test_to_plotly_json_returns_spec(self, df_with_issues: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        spec = result.to_plotly_json()
        assert "checks_table" in spec
        assert "data" in spec["checks_table"]
        assert "layout" in spec["checks_table"]

    def test_to_html_returns_string(self, df_with_issues: pd.DataFrame) -> None:
        pytest.importorskip("jinja2")
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        html = result.to_html()
        assert "<html" in html.lower()
        assert "ConstantColumnCheck" in html

    def test_to_html_writes_atomic(
        self, df_with_issues: pd.DataFrame, tmp_path: Path
    ) -> None:
        pytest.importorskip("jinja2")
        out = tmp_path / "suite.html"
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        html = result.to_html(path=out)
        assert out.exists()
        assert out.read_text(encoding="utf-8") == html
        assert list(tmp_path.glob("*.tmp")) == []

    def test_to_html_raises_without_jinja2(
        self,
        df_with_issues: pd.DataFrame,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        import sys

        monkeypatch.setitem(sys.modules, "jinja2", None)
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        with pytest.raises(ImportError, match="jinja2 is required"):
            result.to_html()

    def test_frozen_dataclass(self, df_with_issues: pd.DataFrame) -> None:
        result = AICIndependenceSuite(df_with_issues, response="y").run()
        with pytest.raises(FrozenInstanceError):
            result.suite_name = "other"  # type: ignore[misc]


def test_public_re_exports() -> None:
    """The suite subpackage is reachable from the top-level package."""
    assert pycatdap.suite is not None
    assert pycatdap.suite.AICIndependenceSuite is AICIndependenceSuite
    assert pycatdap.suite.SuiteResult is SuiteResult


def test_check_results_are_frozen() -> None:
    df = pd.DataFrame({"y": ["a", "b"] * 25, "x": ["a", "b"] * 25})
    result = ConstantColumnCheck().run(df)
    with pytest.raises(FrozenInstanceError):
        result.passed = not result.passed  # type: ignore[misc]
