"""Direct unit tests for :mod:`pycatdap._quality` (H-0008 PR-D2).

These tests construct cards directly (via :class:`pycatdap.VariableCard`)
so the warning logic is exercised without the full ``profile()`` /
``quality_report()`` pipeline. Coverage of the same paths via the
higher-level APIs lives in ``test_profile.py`` and
``test_quality_report.py`` — this file pins the helper's behavior so
future refactors of the dispatch layer cannot silently regress it.
"""

from __future__ import annotations

import pandas as pd
import pytest

from pycatdap import VariableCard
from pycatdap._quality import (
    _DEFAULT_QUALITY_THRESHOLDS,
    QualityWarning,
    _scan_quality,
)


def _card(
    name: str,
    kind: str,
    *,
    n_obs: int,
    n_missing: int = 0,
    n_unique: int = 1,
) -> VariableCard:
    """Build a minimal VariableCard for warning-scanner tests."""
    return VariableCard(
        name=name,
        kind=kind,
        n_obs=n_obs,
        n_missing=n_missing,
        n_unique=n_unique,
        top_value=None,
        top_freq=None,
        stats=None,
        delta_aic_vs_response=None,
        intervals=None,
    )


@pytest.fixture()
def empty_df() -> pd.DataFrame:
    return pd.DataFrame({"_": [0]})


def test_empty_cards_yields_no_warnings(empty_df: pd.DataFrame) -> None:
    assert _scan_quality(empty_df, [], _DEFAULT_QUALITY_THRESHOLDS) == []


def test_normal_card_yields_no_warnings(empty_df: pd.DataFrame) -> None:
    card = _card("good", "continuous", n_obs=100, n_missing=10, n_unique=50)
    assert _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS) == []


def test_constant_column_warning(empty_df: pd.DataFrame) -> None:
    card = _card("const", "categorical", n_obs=100, n_missing=0, n_unique=1)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    assert len(warnings) == 1
    assert warnings[0].kind == "constant"
    assert warnings[0].severity == "warning"
    assert warnings[0].column == "const"
    assert warnings[0].metric == 1.0


def test_constant_short_circuits_other_warnings(empty_df: pd.DataFrame) -> None:
    # high missing AND constant — only one constant warning should fire
    # (the missing-rate warning still fires *before* the short-circuit
    # because the code checks missing_rate first; this test pins that
    # ordering so we know the short-circuit gates the *later* checks).
    card = _card("c", "categorical", n_obs=100, n_missing=80, n_unique=1)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    kinds = [w.kind for w in warnings]
    assert "constant" in kinds
    # high_cardinality must NOT appear because of the continue after constant
    assert "high_cardinality" not in kinds
    assert "id_candidate" not in kinds


def test_high_missing_warning(empty_df: pd.DataFrame) -> None:
    card = _card("hm", "continuous", n_obs=100, n_missing=80, n_unique=20)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    high_missing_warnings = [w for w in warnings if w.kind == "high_missing"]
    assert len(high_missing_warnings) == 1
    assert high_missing_warnings[0].severity == "warning"
    assert high_missing_warnings[0].metric == pytest.approx(0.80)


def test_id_candidate_warning_for_categorical(empty_df: pd.DataFrame) -> None:
    # every non-null value unique, categorical kind
    card = _card("id", "categorical", n_obs=200, n_missing=0, n_unique=200)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    assert any(w.kind == "id_candidate" for w in warnings)


def test_id_candidate_skipped_for_continuous(empty_df: pd.DataFrame) -> None:
    # continuous columns with all-unique values are NOT flagged as IDs
    # (a continuous variable can legitimately have all-distinct samples)
    card = _card("price", "continuous", n_obs=200, n_missing=0, n_unique=200)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    assert not any(w.kind == "id_candidate" for w in warnings)


def test_high_cardinality_info_warning(empty_df: pd.DataFrame) -> None:
    # unique_ratio = 150/200 = 0.75 > 0.5 AND n_unique 150 > 50
    card = _card("hc", "categorical", n_obs=200, n_missing=0, n_unique=150)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    hc = [w for w in warnings if w.kind == "high_cardinality"]
    assert len(hc) == 1
    assert hc[0].severity == "info"
    assert hc[0].metric == pytest.approx(0.75)


def test_threshold_override(empty_df: pd.DataFrame) -> None:
    # default `high_missing=0.5` would skip this card; tighten to 0.1
    card = _card("hm", "continuous", n_obs=100, n_missing=20, n_unique=80)
    thresholds = dict(_DEFAULT_QUALITY_THRESHOLDS)
    thresholds["high_missing"] = 0.1
    warnings = _scan_quality(empty_df, [card], thresholds)
    assert any(w.kind == "high_missing" for w in warnings)


def test_returns_list_of_quality_warning(empty_df: pd.DataFrame) -> None:
    """The helper's return shape is locked-in for downstream consumers."""
    card = _card("c", "categorical", n_obs=10, n_missing=0, n_unique=1)
    warnings = _scan_quality(empty_df, [card], _DEFAULT_QUALITY_THRESHOLDS)
    assert isinstance(warnings, list)
    assert all(isinstance(w, QualityWarning) for w in warnings)
