"""Tests for pycatdap.profile core (H-0007 PR-C1).

HTML rendering (.to_html) is covered separately in test_profile_html.py
once PR-C2 lands. This module covers the data layer and the
show / to_dict / to_plotly_json methods.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from typing import Any

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def df_mixed() -> pd.DataFrame:
    rng = np.random.default_rng(seed=11)
    n = 120
    cat = rng.choice(["a", "b", "c"], size=n)
    return pd.DataFrame(
        {
            "target": rng.choice(["yes", "no"], size=n),
            "cat": cat,
            "cont": np.where(cat == "a", 0.0, 5.0) + rng.normal(0.0, 1.0, size=n),
            "bool_col": rng.choice([True, False], size=n),
        }
    )


@pytest.fixture()
def df_with_quality_issues() -> pd.DataFrame:
    """Frame exercising every default quality-warning kind."""
    n = 200
    return pd.DataFrame(
        {
            # high_missing: > 50% NaN
            "almost_all_nan": [np.nan] * 110 + list(range(90)),
            # constant: single value
            "constant": ["x"] * n,
            # id_candidate: every row unique categorical
            "id_like": [f"id-{i}" for i in range(n)],
            # high_cardinality: many unique numerics framed as strings to
            # avoid the id_candidate trigger (we need > 50 distinct AND
            # nunique / n_obs > 0.5 AND less than n unique, so 150 unique)
            "high_card": [f"v-{i % 150}" for i in range(n)],
            # normal column for contrast
            "good": [i % 3 for i in range(n)],
        }
    )


class TestPublicSurface:
    """profile, ProfileResult, VariableCard, QualityWarning are exported."""

    @pytest.mark.parametrize(
        "name",
        ["profile", "ProfileResult", "VariableCard", "QualityWarning"],
    )
    def test_re_export(self, name: str) -> None:
        assert hasattr(pycatdap, name), f"pycatdap.{name} missing"


class TestBasicShape:
    """profile() returns a ProfileResult with the documented fields."""

    def test_returns_profile_result(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert isinstance(result, pycatdap.ProfileResult)

    def test_has_all_documented_fields(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        for name in (
            "overview",
            "variables",
            "association",
            "top_subsets",
            "quality_warnings",
            "response",
            "n_rows",
            "n_cols",
        ):
            assert hasattr(result, name), f"ProfileResult.{name} missing"

    def test_n_rows_n_cols_match_input(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert result.n_rows == df_mixed.shape[0]
        assert result.n_cols == df_mixed.shape[1]


class TestOverview:
    """overview dict reports table-level statistics."""

    def test_overview_has_expected_keys(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        for key in (
            "n_rows",
            "n_cols",
            "n_missing",
            "missing_rate",
            "n_duplicates",
            "memory_bytes",
            "dtype_counts",
        ):
            assert key in result.overview, f"overview missing {key!r}"

    def test_overview_dtype_counts_is_dict(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert isinstance(result.overview["dtype_counts"], dict)

    def test_overview_duplicates_match_pandas(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert result.overview["n_duplicates"] == int(df_mixed.duplicated().sum())


class TestVariableCards:
    """One VariableCard per input column with type-appropriate fields."""

    def test_one_card_per_column(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert len(result.variables) == df_mixed.shape[1]
        assert [c.name for c in result.variables] == list(df_mixed.columns)

    def test_kind_detection_matches_eda(self, df_mixed: pd.DataFrame) -> None:
        from pycatdap.eda import _detect_kind

        result = pycatdap.profile(df_mixed)
        for card in result.variables:
            assert card.kind == _detect_kind(df_mixed[card.name])

    def test_continuous_card_has_stats(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        cont_card = next(c for c in result.variables if c.name == "cont")
        assert cont_card.stats is not None
        for stat_key in ("mean", "std", "min", "q25", "median", "q75", "max"):
            assert stat_key in cont_card.stats

    def test_categorical_card_has_no_stats(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        cat_card = next(c for c in result.variables if c.name == "cat")
        assert cat_card.stats is None

    def test_top_value_matches_value_counts(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        cat_card = next(c for c in result.variables if c.name == "cat")
        expected_top = df_mixed["cat"].value_counts().index[0]
        assert cat_card.top_value == expected_top


class TestAssociation:
    """association field is the m × m ΔAIC matrix."""

    def test_association_is_dataframe(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert isinstance(result.association, pd.DataFrame)

    def test_association_matches_direct_call(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        direct = pycatdap.association_matrix(df_mixed)
        np.testing.assert_allclose(
            result.association.to_numpy(),
            direct.to_numpy(),
            equal_nan=True,
        )


class TestWithResponse:
    """response= adds delta_aic_vs_response on each card + top_subsets."""

    def test_top_subsets_present_with_response(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed, response="target", top_k_subsets=2)
        assert result.top_subsets is not None
        assert hasattr(result.top_subsets, "aic")  # Catdap2Result-like

    def test_top_subsets_none_without_response(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert result.top_subsets is None

    def test_delta_aic_populated_for_non_response_columns(
        self, df_mixed: pd.DataFrame
    ) -> None:
        result = pycatdap.profile(df_mixed, response="target")
        for card in result.variables:
            if card.name == "target":
                # response column has no self-ΔAIC
                assert card.delta_aic_vs_response is None
            else:
                assert card.delta_aic_vs_response is not None

    def test_delta_aic_none_without_response(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        for card in result.variables:
            assert card.delta_aic_vs_response is None

    def test_response_field_records_input(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed, response="target")
        assert result.response == "target"

    def test_response_none_when_not_provided(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        assert result.response is None

    def test_unknown_response_raises(self, df_mixed: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            pycatdap.profile(df_mixed, response="does_not_exist")


class TestQualityWarnings:
    """Four default warning kinds + custom thresholds."""

    def test_high_missing_fires(self, df_with_quality_issues: pd.DataFrame) -> None:
        result = pycatdap.profile(df_with_quality_issues)
        kinds = {(w.kind, w.column) for w in result.quality_warnings}
        assert ("high_missing", "almost_all_nan") in kinds

    def test_constant_fires(self, df_with_quality_issues: pd.DataFrame) -> None:
        result = pycatdap.profile(df_with_quality_issues)
        kinds = {(w.kind, w.column) for w in result.quality_warnings}
        assert ("constant", "constant") in kinds

    def test_id_candidate_fires(self, df_with_quality_issues: pd.DataFrame) -> None:
        result = pycatdap.profile(df_with_quality_issues)
        kinds = {(w.kind, w.column) for w in result.quality_warnings}
        assert ("id_candidate", "id_like") in kinds

    def test_high_cardinality_fires(self, df_with_quality_issues: pd.DataFrame) -> None:
        result = pycatdap.profile(df_with_quality_issues)
        kinds = {(w.kind, w.column) for w in result.quality_warnings}
        assert ("high_cardinality", "high_card") in kinds

    def test_clean_dataframe_has_no_warnings(self) -> None:
        n = 100
        df = pd.DataFrame(
            {
                "a": [i % 3 for i in range(n)],
                "b": [i % 5 for i in range(n)],
            }
        )
        result = pycatdap.profile(df)
        assert result.quality_warnings == []

    def test_custom_threshold_overrides_default(self) -> None:
        df = pd.DataFrame({"col": [np.nan] * 35 + list(range(65))})
        # 35% missing — default threshold (0.5) would NOT fire,
        # but a custom 0.3 SHOULD fire.
        default = pycatdap.profile(df)
        assert all(w.kind != "high_missing" for w in default.quality_warnings)
        custom = pycatdap.profile(df, quality_thresholds={"high_missing": 0.3})
        kinds = {w.kind for w in custom.quality_warnings}
        assert "high_missing" in kinds


class TestMethods:
    """show / to_dict / to_plotly_json behave per spec."""

    def test_to_dict_is_jsonable(self, df_mixed: pd.DataFrame) -> None:
        import json

        result = pycatdap.profile(df_mixed, response="target")
        as_dict = result.to_dict()
        # Round-trip through json without TypeError.
        serialized = json.dumps(as_dict, default=str)
        assert isinstance(serialized, str)

    def test_to_dict_has_all_top_level_sections(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed, response="target")
        as_dict = result.to_dict()
        for section in (
            "overview",
            "variables",
            "association",
            "top_subsets",
            "quality_warnings",
            "response",
        ):
            assert section in as_dict

    def test_to_plotly_json_returns_dict(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        spec = result.to_plotly_json()
        assert isinstance(spec, dict)

    def test_show_executes(self, df_mixed: pd.DataFrame, capsys: Any) -> None:
        result = pycatdap.profile(df_mixed)
        # show() should not raise; output content varies (Jupyter inline /
        # plain text fallback) so we don't assert on stdout shape.
        result.show()


class TestFrozenDataclasses:
    """ProfileResult / VariableCard / QualityWarning are immutable."""

    def test_profile_result_is_frozen(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        with pytest.raises(FrozenInstanceError):
            result.n_rows = 999  # type: ignore[misc]

    def test_variable_card_is_frozen(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        card = result.variables[0]
        with pytest.raises(FrozenInstanceError):
            card.name = "renamed"  # type: ignore[misc]

    def test_quality_warning_is_frozen(self) -> None:
        warning = pycatdap.QualityWarning(
            severity="warning",
            kind="constant",
            column="col",
            message="msg",
            metric=0.0,
        )
        with pytest.raises(FrozenInstanceError):
            warning.column = "other"  # type: ignore[misc]

    def test_variable_card_has_documented_fields(self, df_mixed: pd.DataFrame) -> None:
        result = pycatdap.profile(df_mixed)
        card = result.variables[0]
        names = {f.name for f in fields(card)}
        expected = {
            "name",
            "kind",
            "n_obs",
            "n_missing",
            "n_unique",
            "top_value",
            "top_freq",
            "stats",
            "delta_aic_vs_response",
            "intervals",
        }
        assert expected <= names


class TestParameterForwarding:
    """bins / criterion / top_k_subsets reach the underlying routines."""

    def test_top_k_subsets_controls_catdap2(self, df_mixed: pd.DataFrame) -> None:
        # nvar=2 should run catdap2 with at most 2 explanatory subset size
        result = pycatdap.profile(df_mixed, response="target", top_k_subsets=2)
        # Catdap2Result.aic columns include "n_vars" or similar; verify by
        # checking that the result keeps an "aic" frame at all (smoke test).
        assert result.top_subsets is not None
        assert hasattr(result.top_subsets, "aic")
