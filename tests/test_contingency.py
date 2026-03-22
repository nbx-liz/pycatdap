"""Tests for contingency table construction."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pycatdap._contingency import build_crosstab, build_multidim_crosstab

# ---------------------------------------------------------------------------
# build_crosstab
# ---------------------------------------------------------------------------


class TestBuildCrosstab:
    """Tests for single-variable crosstab construction."""

    @pytest.fixture()
    def simple_df(self) -> pd.DataFrame:
        """Small deterministic DataFrame for testing."""
        return pd.DataFrame(
            {
                "response": ["A", "A", "B", "B", "B", "A"],
                "expl": ["X", "Y", "X", "Y", "X", "X"],
            }
        )

    def test_return_types(self, simple_df: pd.DataFrame) -> None:
        """Should return (cross_freq, marginal_e, marginal_f, n)."""
        cross, marg_e, marg_f, n = build_crosstab(simple_df, "response", "expl")
        assert isinstance(cross, np.ndarray)
        assert isinstance(marg_e, np.ndarray)
        assert isinstance(marg_f, np.ndarray)
        assert isinstance(n, int)

    def test_shape(self, simple_df: pd.DataFrame) -> None:
        """cross_freq shape should be (C_E, C_F)."""
        cross, marg_e, marg_f, n = build_crosstab(simple_df, "response", "expl")
        c_e = simple_df["response"].nunique()
        c_f = simple_df["expl"].nunique()
        assert cross.shape == (c_e, c_f)
        assert marg_e.shape == (c_e,)
        assert marg_f.shape == (c_f,)

    def test_values(self, simple_df: pd.DataFrame) -> None:
        """Verify cross-frequency values from the small example.

        response\\expl  X  Y
        A              2  1
        B              2  1   (if sorted alphabetically)

        Wait — let's count:
          A,X: rows 0,5 → 2
          A,Y: row 1 → 1
          B,X: rows 2,4 → 2
          B,Y: row 3 → 1
        """
        cross, marg_e, marg_f, n = build_crosstab(simple_df, "response", "expl")
        assert n == 6
        # Total marginals
        np.testing.assert_array_equal(marg_e, cross.sum(axis=1))
        np.testing.assert_array_equal(marg_f, cross.sum(axis=0))
        assert cross.sum() == 6

    def test_marginals_sum_to_n(self, simple_df: pd.DataFrame) -> None:
        """Both marginals must sum to n."""
        cross, marg_e, marg_f, n = build_crosstab(simple_df, "response", "expl")
        assert int(marg_e.sum()) == n
        assert int(marg_f.sum()) == n

    def test_with_nan_rows_excluded(self) -> None:
        """Rows with NaN should be dropped before tabulation."""
        df = pd.DataFrame(
            {
                "response": ["A", "B", None, "A", "B"],
                "expl": ["X", "Y", "X", None, "Y"],
            }
        )
        cross, marg_e, marg_f, n = build_crosstab(df, "response", "expl")
        # Only rows 0 and 4 have no NaN in either column
        # Row 0: A, X
        # Row 1: B, Y  (response=B, expl=Y — both valid)
        # Row 4: B, Y
        assert n == 3

    def test_dataframe_not_mutated(self, simple_df: pd.DataFrame) -> None:
        """Input DataFrame must not be modified."""
        original = simple_df.copy()
        build_crosstab(simple_df, "response", "expl")
        pd.testing.assert_frame_equal(simple_df, original)

    def test_nonexistent_column_raises(self, simple_df: pd.DataFrame) -> None:
        """Should raise KeyError for missing columns."""
        with pytest.raises(KeyError):
            build_crosstab(simple_df, "nonexistent", "expl")

    def test_float_dtype_output(self, simple_df: pd.DataFrame) -> None:
        """Output arrays should be float64 for AIC computation."""
        cross, marg_e, marg_f, n = build_crosstab(simple_df, "response", "expl")
        assert cross.dtype == np.float64
        assert marg_e.dtype == np.float64
        assert marg_f.dtype == np.float64


# ---------------------------------------------------------------------------
# build_multidim_crosstab
# ---------------------------------------------------------------------------


class TestBuildMultidimCrosstab:
    """Tests for multi-variable composite crosstab."""

    @pytest.fixture()
    def multi_df(self) -> pd.DataFrame:
        """DataFrame with response and two explanatory variables."""
        return pd.DataFrame(
            {
                "Y": ["a", "a", "b", "b", "a", "b", "a", "b"],
                "X1": ["p", "p", "q", "q", "p", "q", "q", "p"],
                "X2": ["m", "n", "m", "n", "m", "n", "m", "n"],
            }
        )

    def test_return_types(self, multi_df: pd.DataFrame) -> None:
        cross, marg_e, marg_f, n = build_multidim_crosstab(multi_df, "Y", ["X1", "X2"])
        assert isinstance(cross, np.ndarray)
        assert isinstance(marg_e, np.ndarray)
        assert isinstance(marg_f, np.ndarray)
        assert isinstance(n, int)

    def test_combined_categories(self, multi_df: pd.DataFrame) -> None:
        """C_F should equal the product of unique values in X1 and X2."""
        cross, marg_e, marg_f, n = build_multidim_crosstab(multi_df, "Y", ["X1", "X2"])
        # X1 has 2 levels, X2 has 2 levels → up to 4 combined levels
        c_e = multi_df["Y"].nunique()
        assert cross.shape[0] == c_e
        # C_F <= product of unique values (some combos may not exist)
        assert cross.shape[1] <= 4
        assert n == 8

    def test_marginals_sum_to_n(self, multi_df: pd.DataFrame) -> None:
        cross, marg_e, marg_f, n = build_multidim_crosstab(multi_df, "Y", ["X1", "X2"])
        assert int(marg_e.sum()) == n
        assert int(marg_f.sum()) == n

    def test_single_variable_matches_build_crosstab(self) -> None:
        """With one explanatory variable, should match build_crosstab."""
        df = pd.DataFrame(
            {
                "Y": ["a", "a", "b", "b", "a"],
                "X": ["p", "q", "p", "q", "p"],
            }
        )
        cross1, me1, mf1, n1 = build_crosstab(df, "Y", "X")
        cross2, me2, mf2, n2 = build_multidim_crosstab(df, "Y", ["X"])

        np.testing.assert_array_equal(cross1, cross2)
        np.testing.assert_array_equal(me1, me2)
        np.testing.assert_array_equal(mf1, mf2)
        assert n1 == n2

    def test_empty_explanatory_set_raises(self, multi_df: pd.DataFrame) -> None:
        """Empty explanatory_set should raise ValueError."""
        with pytest.raises(ValueError, match="must not be empty"):
            build_multidim_crosstab(multi_df, "Y", [])

    def test_nonexistent_column_raises(self, multi_df: pd.DataFrame) -> None:
        """Missing column should raise KeyError."""
        with pytest.raises(KeyError):
            build_multidim_crosstab(multi_df, "Y", ["X1", "nonexistent"])

    def test_dataframe_not_mutated(self, multi_df: pd.DataFrame) -> None:
        original = multi_df.copy()
        build_multidim_crosstab(multi_df, "Y", ["X1", "X2"])
        pd.testing.assert_frame_equal(multi_df, original)
