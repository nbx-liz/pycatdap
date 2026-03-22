"""Tests for CATDAP-02."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
import pytest

from pycatdap._subset_search import SubsetResult, search_best_subset
from pycatdap.catdap2 import Catdap2Result, catdap2

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def categorical_df() -> pd.DataFrame:
    """All-categorical dataset with a known strong explanatory variable."""
    rng = np.random.default_rng(42)
    n = 300
    # X1 is strongly associated with Y
    x1 = rng.choice(["a", "b", "c"], size=n)
    y = np.where(x1 == "a", "yes", np.where(x1 == "b", "no", "maybe"))
    # X2 is independent noise
    x2 = rng.choice(["p", "q"], size=n)
    return pd.DataFrame({"Y": y, "X1": x1, "X2": x2})


@pytest.fixture()
def mixed_df() -> pd.DataFrame:
    """Dataset with both categorical and continuous variables."""
    rng = np.random.default_rng(42)
    n = 200
    cont = np.concatenate([rng.normal(3, 1, n // 2), rng.normal(7, 1, n // 2)])
    cat = rng.choice(["m", "f"], size=n)
    response = np.array(["low"] * (n // 2) + ["high"] * (n // 2))
    return pd.DataFrame({"Y": response, "Cont": cont, "Cat": cat})


# ---------------------------------------------------------------------------
# SubsetResult / search_best_subset
# ---------------------------------------------------------------------------


class TestSubsetSearch:
    """Tests for the stepwise subset search algorithm."""

    def test_returns_list_of_subset_results(self, categorical_df: pd.DataFrame) -> None:
        results = search_best_subset(categorical_df, "Y", ["X1", "X2"])
        assert isinstance(results, list)
        assert all(isinstance(r, SubsetResult) for r in results)

    def test_single_var_ranking(self, categorical_df: pd.DataFrame) -> None:
        """Best single variable should be X1 (strong association)."""
        results = search_best_subset(categorical_df, "Y", ["X1", "X2"], max_vars=1)
        single_results = [r for r in results if r.n_vars == 1]
        assert len(single_results) >= 1
        # Best single var should be X1
        assert single_results[0].variables == ("X1",)

    def test_two_var_subsets(self, categorical_df: pd.DataFrame) -> None:
        """Should include 2-variable subsets."""
        results = search_best_subset(categorical_df, "Y", ["X1", "X2"])
        two_var = [r for r in results if r.n_vars == 2]
        assert len(two_var) >= 1

    def test_subset_result_immutable(self, categorical_df: pd.DataFrame) -> None:
        """variables field should be tuple (immutable)."""
        results = search_best_subset(categorical_df, "Y", ["X1", "X2"])
        for r in results:
            assert isinstance(r.variables, tuple)

    def test_sorted_by_n_vars_then_aic(self, categorical_df: pd.DataFrame) -> None:
        """Results should be grouped by n_vars, sorted by AIC within."""
        results = search_best_subset(categorical_df, "Y", ["X1", "X2"])
        prev_nvars = 0
        prev_aic = float("-inf")
        for r in results:
            if r.n_vars > prev_nvars:
                prev_nvars = r.n_vars
                prev_aic = r.aic
            else:
                assert r.aic >= prev_aic
                prev_aic = r.aic


# ---------------------------------------------------------------------------
# catdap2 — all categorical
# ---------------------------------------------------------------------------


class TestCatdap2AllCategorical:
    """Tests for catdap2 with all categorical variables (pool=2)."""

    def test_returns_catdap2_result(self, categorical_df: pd.DataFrame) -> None:
        result = catdap2(
            categorical_df,
            pool=[2, 2, 2],
            response_name="Y",
        )
        assert isinstance(result, Catdap2Result)

    def test_base_aic_is_float(self, categorical_df: pd.DataFrame) -> None:
        result = catdap2(categorical_df, pool=[2, 2, 2], response_name="Y")
        assert isinstance(result.base_aic, float)
        assert np.isfinite(result.base_aic)

    def test_aic_dataframe_shape(self, categorical_df: pd.DataFrame) -> None:
        result = catdap2(categorical_df, pool=[2, 2, 2], response_name="Y")
        assert isinstance(result.aic, pd.DataFrame)
        # Should have one row per explanatory variable
        assert len(result.aic) == 2  # X1, X2

    def test_best_single_var_is_x1(self, categorical_df: pd.DataFrame) -> None:
        """X1 is strongly associated; should rank first."""
        result = catdap2(categorical_df, pool=[2, 2, 2], response_name="Y")
        assert result.aic_order[0] == "X1"

    def test_subsets_populated(self, categorical_df: pd.DataFrame) -> None:
        result = catdap2(categorical_df, pool=[2, 2, 2], response_name="Y")
        assert isinstance(result.subsets, list)
        assert len(result.subsets) >= 1

    def test_dataframe_not_mutated(self, categorical_df: pd.DataFrame) -> None:
        original = categorical_df.copy()
        catdap2(categorical_df, pool=[2, 2, 2], response_name="Y")
        pd.testing.assert_frame_equal(categorical_df, original)


# ---------------------------------------------------------------------------
# catdap2 — with continuous variables
# ---------------------------------------------------------------------------


class TestCatdap2WithContinuous:
    """Tests for catdap2 with continuous variable pooling."""

    def test_continuous_pooling(self, mixed_df: pd.DataFrame) -> None:
        result = catdap2(
            mixed_df,
            pool=[2, 1, 2],
            response_name="Y",
        )
        assert isinstance(result, Catdap2Result)

    def test_intervals_populated(self, mixed_df: pd.DataFrame) -> None:
        """Continuous variables should have interval boundaries."""
        result = catdap2(mixed_df, pool=[2, 1, 2], response_name="Y")
        assert isinstance(result.intervals, Mapping)
        assert "Cont" in result.intervals

    def test_equal_pooling_dispatch(self, mixed_df: pd.DataFrame) -> None:
        """pool=0 should use equal pooling."""
        result = catdap2(
            mixed_df,
            pool=[2, 0, 2],
            response_name="Y",
        )
        assert "Cont" in result.intervals


# ---------------------------------------------------------------------------
# catdap2 — validation
# ---------------------------------------------------------------------------


class TestCatdap2Validation:
    """Tests for input validation."""

    def test_missing_response_raises(self, categorical_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="response"):
            catdap2(categorical_df, pool=[2, 2, 2], response_name="NonExist")

    def test_pool_length_mismatch_raises(self, categorical_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="pool"):
            catdap2(categorical_df, pool=[2, 2], response_name="Y")

    def test_empty_dataframe_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            catdap2(pd.DataFrame(), response_name="Y")
