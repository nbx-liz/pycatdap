"""Tests for the PR-G3 output helpers of :class:`ErrorAnalysisResult`.

Covers ``to_plotly_json`` / ``to_html`` / ``to_divexplorer_format``.

``to_html`` requires jinja2; per memory ``feedback_to_html_lowest_deps_jinja2_guard``
every test in this file starts with ``pytest.importorskip("jinja2")`` so
the ``Quality (lowest-direct deps)`` CI matrix does not fail (it does
not install the ``[plotly]`` extras).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

import pycatdap


@pytest.fixture
def binary_result() -> pycatdap.ErrorAnalysisResult:
    import numpy as np

    rng = np.random.default_rng(seed=7)
    n = 200
    age = rng.choice(["young", "old"], size=n)
    sex = rng.choice(["M", "F"], size=n)
    y_true = np.where(age == "old", 1, 0)
    flip_p = np.where(age == "young", 0.4, 0.05)
    flips = rng.random(n) < flip_p
    y_pred = np.where(flips, 1 - y_true, y_true)
    df = pd.DataFrame(
        {
            "age": age,
            "sex": sex,
            "y_true": y_true.astype(int),
            "y_pred": y_pred.astype(int),
        }
    )
    return pycatdap.error_analysis(df, "y_true", "y_pred", top_k=2)


@pytest.fixture
def regression_result() -> pycatdap.ErrorAnalysisResult:
    import numpy as np

    rng = np.random.default_rng(seed=23)
    n = 200
    group = rng.choice(["lo", "hi"], size=n)
    y_true = np.where(group == "hi", 10.0, 0.0) + rng.normal(0, 1.0, size=n)
    bias = np.where(group == "hi", -3.0, 0.0)
    y_pred = y_true + bias + rng.normal(0, 0.5, size=n)
    df = pd.DataFrame(
        {
            "group": group,
            "noisy": rng.choice(["x", "y"], size=n),
            "y_true": y_true,
            "y_pred": y_pred,
        }
    )
    return pycatdap.error_analysis(df, "y_true", "y_pred", top_k=2)


# ---------- to_plotly_json ----------


def test_to_plotly_json_classification_sections(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    spec = binary_result.to_plotly_json()
    assert "feature_ranking" in spec
    assert "confusion" in spec
    assert "top_summaries" in spec
    assert spec["feature_ranking"]["data"][0]["type"] == "bar"
    assert spec["confusion"]["data"][0]["type"] == "bar"


def test_to_plotly_json_regression_omits_confusion(
    regression_result: pycatdap.ErrorAnalysisResult,
) -> None:
    spec = regression_result.to_plotly_json()
    assert "feature_ranking" in spec
    assert "confusion" not in spec
    assert "top_summaries" in spec


def test_to_plotly_json_is_json_serialisable(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    spec = binary_result.to_plotly_json()
    json.dumps(spec)


# ---------- to_html ----------


def test_to_html_classification_returns_str(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    html = binary_result.to_html()
    assert isinstance(html, str)
    assert "<html" in html.lower()
    assert "error_analysis" in html
    assert "Feature ranking" in html


def test_to_html_includes_confusion_section(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    html = binary_result.to_html()
    assert "Confusion" in html
    # All 4 canonical labels surface even when their count is 0.
    for cat in ("TP", "FP", "FN", "TN"):
        assert cat in html


def test_to_html_includes_top_slices_table(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    html = binary_result.to_html()
    if binary_result.top_slices:
        assert "error slices" in html


def test_to_html_regression_omits_confusion(
    regression_result: pycatdap.ErrorAnalysisResult,
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    html = regression_result.to_html()
    assert "MAE" in html
    assert "RMSE" in html
    assert "Confusion" not in html


def test_to_html_atomic_write_to_disk(
    binary_result: pycatdap.ErrorAnalysisResult,
    tmp_path: Path,
) -> None:
    pytest.importorskip("jinja2")
    pytest.importorskip("plotly")
    out = tmp_path / "report.html"
    html = binary_result.to_html(path=out)
    assert out.exists()
    assert out.read_text(encoding="utf-8") == html


# ---------- to_divexplorer_format ----------


def test_to_divexplorer_format_columns(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    df = binary_result.to_divexplorer_format()
    assert list(df.columns) == [
        "description",
        "size",
        "error_rate",
        "delta_aic",
        "pearson_residual",
        "error_category",
        "variable",
        "category",
    ]


def test_to_divexplorer_format_one_row_per_slice(
    binary_result: pycatdap.ErrorAnalysisResult,
) -> None:
    df = binary_result.to_divexplorer_format()
    assert len(df) == len(binary_result.top_slices)
    if not df.empty:
        for _, row in df.iterrows():
            assert row["description"] == f"{row['variable']} = {row['category']}"
            assert abs(row["pearson_residual"]) >= 2.0


def test_to_divexplorer_format_empty_when_no_slices() -> None:
    import numpy as np

    df = pd.DataFrame(
        {
            "x": np.arange(50),
            "y_true": [0, 1] * 25,
            "y_pred": [0, 1] * 25,  # perfect classifier
        }
    )
    r = pycatdap.error_analysis(df, "y_true", "y_pred")
    out = r.to_divexplorer_format()
    assert out.empty
    # Empty but typed: column set must still match.
    assert "description" in out.columns
