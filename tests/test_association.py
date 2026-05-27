"""Tests for pycatdap.association_matrix (H-0006 PR-B2)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap import target_summary


@pytest.fixture()
def df_mixed() -> pd.DataFrame:
    """Mixed categorical / continuous / boolean frame for cross-pair tests."""
    rng = np.random.default_rng(seed=2026)
    n = 80
    cat_a = rng.choice(["x", "y", "z"], size=n)
    bool_a = rng.choice([True, False], size=n)
    # cont_a is partially driven by cat_a (so ΔAIC is informative)
    cont_a = np.where(cat_a == "x", 0.0, 5.0) + rng.normal(0.0, 1.0, size=n)
    cont_b = rng.normal(10.0, 2.0, size=n)
    return pd.DataFrame(
        {"cat_a": cat_a, "bool_a": bool_a, "cont_a": cont_a, "cont_b": cont_b}
    )


@pytest.fixture()
def df_categorical_only() -> pd.DataFrame:
    rng = np.random.default_rng(seed=7)
    n = 100
    return pd.DataFrame(
        {
            "a": rng.choice(["p", "q", "r"], size=n),
            "b": rng.choice(["m", "n"], size=n),
            "c": rng.choice(["x", "y", "z", "w"], size=n),
        }
    )


class TestPublicSurface:
    """association_matrix is re-exported at the top level."""

    def test_importable_from_pycatdap(self) -> None:
        assert hasattr(pycatdap, "association_matrix")
        assert callable(pycatdap.association_matrix)


class TestReturnShape:
    """Return value is a square DataFrame with diagonal NaN."""

    def test_returns_dataframe(self, df_categorical_only: pd.DataFrame) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        assert isinstance(m, pd.DataFrame)

    def test_shape_is_square(self, df_categorical_only: pd.DataFrame) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        n_cols = df_categorical_only.shape[1]
        assert m.shape == (n_cols, n_cols)

    def test_index_and_columns_match_df_columns(
        self, df_categorical_only: pd.DataFrame
    ) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        assert list(m.index) == list(df_categorical_only.columns)
        assert list(m.columns) == list(df_categorical_only.columns)

    def test_diagonal_is_nan(self, df_categorical_only: pd.DataFrame) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        for col in df_categorical_only.columns:
            assert pd.isna(m.loc[col, col]), f"diagonal at {col} must be NaN"

    def test_offdiagonal_is_not_nan(self, df_categorical_only: pd.DataFrame) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        for i in df_categorical_only.columns:
            for j in df_categorical_only.columns:
                if i != j:
                    assert not pd.isna(m.loc[i, j]), (
                        f"off-diagonal ({i}, {j}) must not be NaN"
                    )


class TestNumericalConsistency:
    """Each cell equals target_summary(df, target=i, explanatory=j).delta_aic."""

    def test_cell_matches_target_summary_categorical(
        self, df_categorical_only: pd.DataFrame
    ) -> None:
        m = pycatdap.association_matrix(df_categorical_only)
        cols = list(df_categorical_only.columns)
        for i in cols:
            for j in cols:
                if i == j:
                    continue
                expected = target_summary(
                    df_categorical_only, target=i, explanatory=j
                ).delta_aic
                assert m.loc[i, j] == pytest.approx(expected), (
                    f"cell ({i}, {j}) mismatch"
                )

    def test_cell_matches_target_summary_mixed_dtypes(
        self, df_mixed: pd.DataFrame
    ) -> None:
        """Mixed dtypes route through categorical or regression mode as needed."""
        m = pycatdap.association_matrix(df_mixed)
        cols = list(df_mixed.columns)
        for i in cols:
            for j in cols:
                if i == j:
                    continue
                result = target_summary(df_mixed, target=i, explanatory=j)
                assert m.loc[i, j] == pytest.approx(result.delta_aic), (
                    f"cell ({i}, {j}) mismatch"
                )


class TestAsymmetry:
    """ΔAIC is directional; the matrix is NOT symmetric in general."""

    def test_some_cell_is_asymmetric(self, df_mixed: pd.DataFrame) -> None:
        """At least one (i, j) pair differs from (j, i) — directional info."""
        m = pycatdap.association_matrix(df_mixed)
        cols = list(df_mixed.columns)
        found_asymmetric = False
        for i_idx, i in enumerate(cols):
            for j in cols[i_idx + 1 :]:
                if not np.isclose(m.loc[i, j], m.loc[j, i]):
                    found_asymmetric = True
                    break
            if found_asymmetric:
                break
        assert found_asymmetric, (
            "association_matrix should be asymmetric for mixed dtype data"
        )


class TestParameterForwarding:
    """bins and criterion are forwarded to target_summary."""

    def test_bins_is_forwarded_to_continuous_explanatory(
        self, df_mixed: pd.DataFrame
    ) -> None:
        """Changing bins must change the delta_aic for at least one cell."""
        m_default = pycatdap.association_matrix(df_mixed)
        m_binned = pycatdap.association_matrix(df_mixed, bins=3)
        # cat × continuous cells should be sensitive to bins
        # cat_a as target, cont_a as explanatory
        assert m_default.loc["cat_a", "cont_a"] != pytest.approx(
            m_binned.loc["cat_a", "cont_a"]
        )

    def test_criterion_default_is_bic(self, df_mixed: pd.DataFrame) -> None:
        """Default criterion='bic' matches direct target_summary call."""
        m = pycatdap.association_matrix(df_mixed)
        # cont_a as target, cat_a as explanatory -> regression mode
        ts = target_summary(
            df_mixed, target="cont_a", explanatory="cat_a", criterion="bic"
        )
        assert m.loc["cont_a", "cat_a"] == pytest.approx(ts.delta_aic)

    def test_criterion_aic_changes_regression_cells(
        self, df_mixed: pd.DataFrame
    ) -> None:
        m_bic = pycatdap.association_matrix(df_mixed, criterion="bic")
        m_aic = pycatdap.association_matrix(df_mixed, criterion="aic")
        # At least one continuous-target cell should differ
        assert m_bic.loc["cont_a", "cat_a"] != pytest.approx(
            m_aic.loc["cont_a", "cat_a"]
        )


class TestErrorPaths:
    """Clear errors for invalid input."""

    def test_unknown_measure_raises(self, df_mixed: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="measure"):
            pycatdap.association_matrix(df_mixed, measure="cramers_v")  # type: ignore[arg-type]

    def test_single_column_frame_returns_1x1_nan(self) -> None:
        df = pd.DataFrame({"only": [1, 2, 3, 4]})
        m = pycatdap.association_matrix(df)
        assert m.shape == (1, 1)
        assert pd.isna(m.loc["only", "only"])

    def test_empty_dataframe_raises(self) -> None:
        df = pd.DataFrame()
        with pytest.raises(ValueError, match="at least one column"):
            pycatdap.association_matrix(df)
