"""Tests for :func:`pycatdap.target_analysis` (H-0008 PR-D3).

``target_analysis(df, response)`` is the target-driven counterpart of
:func:`pycatdap.profile`: it ranks every non-response column by ΔAIC
against ``response`` and keeps the full :class:`TargetSummary` objects
for the top-K most informative columns.

Mirrors the 4-method contract of :class:`ProfileResult` (``.show /
.to_html / .to_dict / .to_plotly_json``) so the result can flow into
LizyStudio / Jupyter exactly like ``profile()``.
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def df_categorical_target() -> pd.DataFrame:
    rng = np.random.default_rng(seed=23)
    n = 200
    sex = rng.choice(["m", "f"], size=n)
    # `informative_cat` correlates strongly with `target` via sex
    target = np.where(sex == "m", "yes", "no")
    flip = rng.random(n) < 0.1
    target = np.where(flip, np.where(target == "yes", "no", "yes"), target)
    return pd.DataFrame(
        {
            "target": target,
            "informative_cat": sex,
            "noisy_cat": rng.choice(["a", "b", "c"], size=n),
            "noisy_num": rng.normal(0, 1, size=n),
        }
    )


@pytest.fixture()
def df_continuous_target() -> pd.DataFrame:
    rng = np.random.default_rng(seed=31)
    n = 200
    x = rng.normal(0, 1, size=n)
    return pd.DataFrame(
        {
            "y_cont": x * 3.0 + rng.normal(0, 0.5, size=n),
            "informative_num": x,
            "noisy_cat": rng.choice(["a", "b"], size=n),
        }
    )


def test_returns_target_analysis_result(df_categorical_target: pd.DataFrame) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target")
    assert isinstance(r, pycatdap.TargetAnalysisResult)
    assert r.response == "target"
    assert r.n_rows == len(df_categorical_target)
    assert r.n_cols == len(df_categorical_target.columns)


def test_response_missing_raises_key_error(
    df_categorical_target: pd.DataFrame,
) -> None:
    with pytest.raises(KeyError, match="response column not found"):
        pycatdap.target_analysis(df_categorical_target, response="does_not_exist")


def test_ranking_contains_all_non_response_columns(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target")
    explanatory = set(df_categorical_target.columns) - {"target"}
    assert set(r.ranking["variable"]) == explanatory
    # response column itself is NOT in the ranking
    assert "target" not in set(r.ranking["variable"])
    # ranking is sorted ascending by delta_aic (most informative first)
    delta_aic_vals = r.ranking["delta_aic"].tolist()
    assert delta_aic_vals == sorted(delta_aic_vals)


def test_ranking_columns_expected_shape(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target")
    assert list(r.ranking.columns) == ["variable", "delta_aic", "kind", "n_obs"]


def test_top_summaries_size_equals_top_k(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    assert len(r.top_summaries) == 2
    # top_summaries keys are the top-K variables in the ranking
    top_2 = r.ranking["variable"].head(2).tolist()
    assert set(r.top_summaries.keys()) == set(top_2)


def test_top_summaries_are_target_summary_instances(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=3)
    for col, summary in r.top_summaries.items():
        # categorical response → TargetSummary
        assert isinstance(summary, pycatdap.TargetSummary)
        assert summary.target == "target"
        assert summary.explanatory == col


def test_top_summaries_with_continuous_response(
    df_continuous_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_continuous_target, response="y_cont", top_k=2)
    for summary in r.top_summaries.values():
        # continuous response → RegressionTargetSummary
        assert isinstance(summary, pycatdap.RegressionTargetSummary)


def test_top_k_caps_at_available_explanatories(
    df_categorical_target: pd.DataFrame,
) -> None:
    # only 3 non-response columns — asking for top_k=10 must NOT crash
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=10)
    assert len(r.top_summaries) == 3


def test_top_k_zero_returns_empty_summaries(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=0)
    assert r.top_summaries == {}
    # ranking is still produced
    assert len(r.ranking) > 0


def test_response_card_describes_response_column(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target")
    assert r.response_card.name == "target"
    assert r.response_card.n_obs == len(df_categorical_target)


def test_informative_variable_ranks_first(
    df_categorical_target: pd.DataFrame,
) -> None:
    """The intentionally-correlated `informative_cat` must beat random columns."""
    r = pycatdap.target_analysis(df_categorical_target, response="target")
    top_variable = r.ranking["variable"].iloc[0]
    assert top_variable == "informative_cat"


def test_to_dict_is_json_serializable(df_categorical_target: pd.DataFrame) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    d = r.to_dict()
    assert d["response"] == "target"
    assert d["n_rows"] == len(df_categorical_target)
    assert "ranking" in d
    assert "top_summaries" in d
    assert "response_card" in d
    # round-trips through json
    json.dumps(d)


def test_to_plotly_json_returns_per_section_specs(
    df_categorical_target: pd.DataFrame,
) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    spec = r.to_plotly_json()
    assert "ranking" in spec
    assert "top_summaries" in spec
    # top_summaries is a dict[col_name -> plotly spec]
    assert isinstance(spec["top_summaries"], dict)
    assert len(spec["top_summaries"]) == 2


def test_to_html_returns_string(df_categorical_target: pd.DataFrame) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    html = r.to_html()
    assert isinstance(html, str)
    assert "<html" in html.lower()
    # the response name should appear in the header
    assert "target" in html
    # ranking table must reach the rendered output
    assert "informative_cat" in html


def test_to_html_writes_atomic(
    df_categorical_target: pd.DataFrame, tmp_path: Path
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    out = tmp_path / "ta.html"
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=1)
    html = r.to_html(path=out)
    assert out.exists()
    assert out.read_text(encoding="utf-8") == html
    assert list(tmp_path.glob("*.tmp")) == []


def test_to_html_raises_clean_import_error_without_jinja2(
    df_categorical_target: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    import sys

    monkeypatch.setitem(sys.modules, "jinja2", None)
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=1)
    with pytest.raises(ImportError, match="jinja2 is required"):
        r.to_html()


def test_show_falls_back_to_stdout(
    df_categorical_target: pd.DataFrame,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import sys

    monkeypatch.setitem(sys.modules, "IPython", None)
    monkeypatch.setitem(sys.modules, "IPython.display", None)
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    r.show()
    out = capsys.readouterr().out
    assert "TargetAnalysisResult" in out
    # ranking table must reach stdout in fallback mode
    assert "informative_cat" in out


def test_show_uses_ipython_when_available(
    df_categorical_target: pd.DataFrame,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """With IPython available, show() prints header + delegates tables to display().

    Covers the IPython-installed branch of show() (lines after the
    try/except). The display() call itself routes to Jupyter and writes
    nothing to stdout, so we only assert the print() side-effects.
    """
    pytest.importorskip("IPython")
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=2)
    r.show()
    out = capsys.readouterr().out
    assert "TargetAnalysisResult" in out
    assert "response='target'" in out


def test_frozen_dataclass(df_categorical_target: pd.DataFrame) -> None:
    r = pycatdap.target_analysis(df_categorical_target, response="target", top_k=1)
    with pytest.raises(FrozenInstanceError):
        r.response = "other"  # type: ignore[misc]


def test_public_re_export() -> None:
    assert pycatdap.target_analysis is not None
    assert pycatdap.TargetAnalysisResult is not None
