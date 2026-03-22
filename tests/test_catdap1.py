"""Tests for CATDAP-01."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
import pytest

from pycatdap.catdap1 import Catdap1Result, catdap1


@pytest.fixture()
def titanic_like_df() -> pd.DataFrame:
    """Small Titanic-like dataset with known associations."""
    return pd.DataFrame(
        {
            "Survived": ["Yes"] * 40 + ["No"] * 60,
            "Class": (["1st"] * 25 + ["3rd"] * 15 + ["1st"] * 10 + ["3rd"] * 50),
            "Sex": (["Female"] * 30 + ["Male"] * 10 + ["Female"] * 5 + ["Male"] * 55),
            "Embarked": (
                ["S"] * 20
                + ["C"] * 10
                + ["Q"] * 10
                + ["S"] * 30
                + ["C"] * 15
                + ["Q"] * 15
            ),
        }
    )


@pytest.fixture()
def independent_df() -> pd.DataFrame:
    """DataFrame with independent variables (no association)."""
    rng = np.random.default_rng(123)
    n = 500
    return pd.DataFrame(
        {
            "Y": rng.choice(["a", "b", "c"], size=n),
            "X1": rng.choice(["p", "q"], size=n),
            "X2": rng.choice(["m", "n", "o"], size=n),
        }
    )


# ---------------------------------------------------------------------------
# Return type and structure
# ---------------------------------------------------------------------------


class TestCatdap1ReturnType:
    """Tests for Catdap1Result structure."""

    def test_returns_catdap1_result(self, titanic_like_df: pd.DataFrame) -> None:
        result = catdap1(titanic_like_df)
        assert isinstance(result, Catdap1Result)

    def test_aic_is_dataframe(self, titanic_like_df: pd.DataFrame) -> None:
        result = catdap1(titanic_like_df)
        assert isinstance(result.aic, pd.DataFrame)

    def test_aic_shape(self, titanic_like_df: pd.DataFrame) -> None:
        """AIC DataFrame: rows = response vars, columns = explanatory vars."""
        result = catdap1(titanic_like_df)
        n_vars = len(titanic_like_df.columns)
        # All variables as response: n_vars rows, n_vars-1 explanatory each
        assert result.aic.shape[0] == n_vars

    def test_aic_order_is_mapping(self, titanic_like_df: pd.DataFrame) -> None:
        result = catdap1(titanic_like_df)
        assert isinstance(result.aic_order, Mapping)

    def test_tway_tables_is_mapping(self, titanic_like_df: pd.DataFrame) -> None:
        result = catdap1(titanic_like_df)
        assert isinstance(result.tway_tables, Mapping)


# ---------------------------------------------------------------------------
# AIC values and ordering
# ---------------------------------------------------------------------------


class TestCatdap1AicValues:
    """Tests for AIC computation correctness."""

    def test_known_association_negative_aic(
        self, titanic_like_df: pd.DataFrame
    ) -> None:
        """Sex has strong association with Survived → negative ΔAIC."""
        result = catdap1(titanic_like_df, response_names=["Survived"])
        sex_aic = result.aic.loc["Survived", "Sex"]
        assert sex_aic < 0

    def test_aic_order_sorted_ascending(self, titanic_like_df: pd.DataFrame) -> None:
        """aic_order lists should be sorted by AIC ascending (best first)."""
        result = catdap1(titanic_like_df)
        for response_name, ordered_vars in result.aic_order.items():
            aic_values = [result.aic.loc[response_name, v] for v in ordered_vars]
            assert aic_values == sorted(aic_values)

    def test_independent_vars_positive_aic(self, independent_df: pd.DataFrame) -> None:
        """Independent variables should yield ΔAIC >= 0 (approximately)."""
        result = catdap1(independent_df, response_names=["Y"])
        for col in ["X1", "X2"]:
            assert result.aic.loc["Y", col] > -2.0  # allow small stochastic noise


# ---------------------------------------------------------------------------
# Response variable selection
# ---------------------------------------------------------------------------


class TestCatdap1ResponseSelection:
    """Tests for response_names parameter."""

    def test_all_responses_default(self, titanic_like_df: pd.DataFrame) -> None:
        """When response_names=None, all variables are used as response."""
        result = catdap1(titanic_like_df)
        assert set(result.aic.index) == set(titanic_like_df.columns)

    def test_specific_responses(self, titanic_like_df: pd.DataFrame) -> None:
        """When response_names specified, only those used."""
        result = catdap1(titanic_like_df, response_names=["Survived"])
        assert list(result.aic.index) == ["Survived"]

    def test_multiple_responses(self, titanic_like_df: pd.DataFrame) -> None:
        result = catdap1(titanic_like_df, response_names=["Survived", "Class"])
        assert set(result.aic.index) == {"Survived", "Class"}


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


class TestCatdap1Validation:
    """Tests for input validation."""

    def test_empty_dataframe_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            catdap1(pd.DataFrame())

    def test_single_column_raises(self) -> None:
        df = pd.DataFrame({"A": ["x", "y", "z"]})
        with pytest.raises(ValueError, match="at least 2"):
            catdap1(df)

    def test_nonexistent_response_raises(self, titanic_like_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="not found"):
            catdap1(titanic_like_df, response_names=["NonExistent"])


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


class TestCatdap1Immutability:
    """Tests for input DataFrame not being mutated."""

    def test_dataframe_not_mutated(self, titanic_like_df: pd.DataFrame) -> None:
        original = titanic_like_df.copy()
        catdap1(titanic_like_df)
        pd.testing.assert_frame_equal(titanic_like_df, original)
