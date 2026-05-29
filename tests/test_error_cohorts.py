"""Tests for compare_cohorts + detect_drift (H-0014 PR-L4)."""

from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest

from pycatdap.error import (
    CohortComparison,
    DriftReport,
    compare_cohorts,
    detect_drift,
)


def _two_cohorts(
    seed: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Cohort B shifts the 'region' distribution vs cohort A."""
    rng = np.random.default_rng(seed)
    a = pd.DataFrame(
        {
            "region": rng.choice(["north", "south"], size=300, p=[0.5, 0.5]),
            "plan": rng.choice(["basic", "pro"], size=300, p=[0.7, 0.3]),
        }
    )
    b = pd.DataFrame(
        {
            "region": rng.choice(["north", "south"], size=300, p=[0.1, 0.9]),
            "plan": rng.choice(["basic", "pro"], size=300, p=[0.7, 0.3]),
        }
    )
    return a, b


def test_compare_cohorts_returns_comparison() -> None:
    a, b = _two_cohorts()
    cmp = compare_cohorts(a, b)
    assert isinstance(cmp, CohortComparison)
    assert cmp.n_a == 300
    assert cmp.n_b == 300
    assert set(cmp.summary["variable"]) == {"region", "plan"}


def test_shifted_column_is_most_discriminative() -> None:
    a, b = _two_cohorts()
    cmp = compare_cohorts(a, b)
    # 'region' shifted hard, 'plan' did not → region has the lower (more
    # negative) ΔAIC and sorts first.
    assert cmp.summary.iloc[0]["variable"] == "region"
    region = cmp.summary[cmp.summary["variable"] == "region"].iloc[0]
    plan = cmp.summary[cmp.summary["variable"] == "plan"].iloc[0]
    assert region["delta_aic"] < plan["delta_aic"]
    assert region["max_abs_diff"] > plan["max_abs_diff"]


def test_distribution_proportions_sum_to_one() -> None:
    a, b = _two_cohorts()
    cmp = compare_cohorts(a, b)
    dist = cmp.distributions["region"]
    assert dist["prop_a"].sum() == pytest.approx(1.0)
    assert dist["prop_b"].sum() == pytest.approx(1.0)


def test_inputs_not_mutated() -> None:
    a, b = _two_cohorts()
    a0, b0 = a.copy(deep=True), b.copy(deep=True)
    compare_cohorts(a, b)
    pdt.assert_frame_equal(a, a0)
    pdt.assert_frame_equal(b, b0)


def test_comparison_is_frozen() -> None:
    a, b = _two_cohorts()
    cmp = compare_cohorts(a, b)
    with pytest.raises(dataclasses.FrozenInstanceError):
        cmp.n_a = 1  # type: ignore[misc]


def test_no_shared_columns_raises() -> None:
    a = pd.DataFrame({"x": [1, 2, 3]})
    b = pd.DataFrame({"y": [1, 2, 3]})
    with pytest.raises(ValueError, match="share no comparable columns"):
        compare_cohorts(a, b)


def test_continuous_column_binned() -> None:
    rng = np.random.default_rng(1)
    a = pd.DataFrame({"age": rng.integers(20, 40, size=300).astype(float)})
    b = pd.DataFrame({"age": rng.integers(50, 80, size=300).astype(float)})
    cmp = compare_cohorts(a, b)
    # age strongly separates the cohorts → negative ΔAIC
    assert cmp.summary.iloc[0]["variable"] == "age"
    assert cmp.summary.iloc[0]["delta_aic"] < 0


def test_response_delta_present_when_response_given() -> None:
    rng = np.random.default_rng(2)
    n = 300
    a = pd.DataFrame(
        {
            "feat": rng.choice(["x", "y"], size=n),
            "age": rng.integers(20, 70, size=n).astype(float),  # continuous
            "target": rng.integers(0, 2, size=n),
        }
    )
    b = pd.DataFrame(
        {
            "feat": rng.choice(["x", "y"], size=n),
            "age": rng.integers(20, 70, size=n).astype(float),
            "target": rng.integers(0, 2, size=n),
        }
    )
    cmp = compare_cohorts(a, b, response="target")
    assert cmp.response_delta is not None
    assert "shift" in cmp.response_delta.columns
    assert set(cmp.response_delta["variable"]) == {"feat", "age"}
    # response column itself is excluded from the feature comparison
    assert "target" not in set(cmp.summary["variable"])
    # to_html exercises the has_response branch
    pytest.importorskip("jinja2")
    assert "Response-relationship shift" in cmp.to_html()


def test_to_dict_structure() -> None:
    a, b = _two_cohorts()
    d = compare_cohorts(a, b).to_dict()
    assert d["n_a"] == 300
    assert isinstance(d["summary"], list)
    assert "region" in d["distributions"]
    assert d["response_delta"] is None


def test_to_html_renders() -> None:
    pytest.importorskip("jinja2")
    a, b = _two_cohorts()
    html = compare_cohorts(a, b).to_html()
    assert "compare_cohorts" in html
    assert "region" in html


def test_to_html_writes_file(tmp_path: object) -> None:
    pytest.importorskip("jinja2")
    a, b = _two_cohorts()
    out = tmp_path / "cmp.html"  # type: ignore[operator]
    html = compare_cohorts(a, b).to_html(path=out)
    assert out.read_text(encoding="utf-8") == html  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# detect_drift
# ---------------------------------------------------------------------------


def test_detect_drift_ranks_by_magnitude() -> None:
    train, prod = _two_cohorts()
    report = detect_drift(train, prod)
    assert isinstance(report, DriftReport)
    assert report.n_train == 300
    assert report.n_prod == 300
    # most-drifted feature first; |delta_aic| descending
    mags = report.drift_ranking["delta_aic"].abs().tolist()
    assert mags == sorted(mags, reverse=True)
    assert report.drift_ranking.iloc[0]["variable"] == "region"
    assert report.error_rate_prod is None


def test_detect_drift_reports_prod_error_rate() -> None:
    rng = np.random.default_rng(3)
    n = 300
    train = pd.DataFrame({"f": rng.choice(["a", "b"], size=n)})
    prod = pd.DataFrame({"f": rng.choice(["a", "b"], size=n)})
    y_true = rng.integers(0, 2, size=n)
    y_pred = np.where(rng.random(n) < 0.25, 1 - y_true, y_true)
    report = detect_drift(train, prod, y_true=y_true, y_pred=y_pred)
    assert report.error_rate_prod is not None
    assert 0.0 <= report.error_rate_prod <= 1.0


def test_drift_report_frozen_and_to_dict() -> None:
    train, prod = _two_cohorts()
    report = detect_drift(train, prod)
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.n_train = 1  # type: ignore[misc]
    d = report.to_dict()
    assert d["n_train"] == 300
    assert isinstance(d["drift_ranking"], list)
