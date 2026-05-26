"""Tests for pycatdap.eda (describe + DescribeResult)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pycatdap import describe
from pycatdap.eda import DescribeResult


@pytest.fixture()
def mixed_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x_cont": [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5],
            "x_cat": ["a", "b", "a", "c", "a", "b", "c", "a", "b", "c"],
            "x_bool": [True, False, True, True, False, True, False, True, False, True],
            "x_missing": [1.0, np.nan, 3.0, np.nan, 5.0, 6.0, 7.0, np.nan, 9.0, 10.0],
        }
    )


class TestDescribeResultStructure:
    def test_returns_describe_result(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert isinstance(result, DescribeResult)

    def test_n_rows_n_cols(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.n_rows == 10
        assert result.n_cols == 4

    def test_summary_index_matches_columns(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert list(result.summary.index) == list(mixed_df.columns)

    def test_repr(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert "n_rows=10" in repr(result)
        assert "n_cols=4" in repr(result)


class TestKindDetection:
    def test_continuous_detection(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.summary.loc["x_cont", "kind"] == "continuous"

    def test_categorical_string_detection(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.summary.loc["x_cat", "kind"] == "categorical"

    def test_boolean_detection(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.summary.loc["x_bool", "kind"] == "boolean"

    def test_csv_string_columns_detected_as_categorical(self) -> None:
        """Titanic-style data (StringDtype after CSV read) is categorical."""
        from pycatdap.datasets import load_titanic

        df = load_titanic()
        result = describe(df)
        for col in ["Class", "Sex", "Age", "Survived"]:
            assert result.summary.loc[col, "kind"] == "categorical", col


class TestSummaryFields:
    def test_n_missing_correct(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.summary.loc["x_missing", "n_missing"] == 3
        assert result.summary.loc["x_cont", "n_missing"] == 0

    def test_n_unique_correct(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        assert result.summary.loc["x_cat", "n_unique"] == 3

    def test_top_and_top_freq(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        # x_cat: a=4, b=3, c=3 -> top=a
        assert result.summary.loc["x_cat", "top"] == "a"
        assert result.summary.loc["x_cat", "top_freq"] == 4

    def test_continuous_stats_present(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        row = result.summary.loc["x_cont"]
        assert row["mean"] == pytest.approx(6.0)
        assert row["min"] == 1.5
        assert row["max"] == 10.5

    def test_continuous_stats_absent_for_categorical(
        self, mixed_df: pd.DataFrame
    ) -> None:
        result = describe(mixed_df)
        row = result.summary.loc["x_cat"]
        # Stored as None internally; surfaced as NaN by pandas when the column
        # is mixed (continuous rows present in the same DataFrame).
        assert pd.isna(row["mean"])
        assert pd.isna(row["std"])
        assert pd.isna(row["min"])


class TestSerialization:
    def test_to_dict_round_trip(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        d = result.to_dict()
        assert d["n_rows"] == 10
        assert d["n_cols"] == 4
        assert "variables" in d
        assert set(d["variables"].keys()) == set(mixed_df.columns)

    def test_to_html_returns_string(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        html = result.to_html()
        assert isinstance(html, str)
        assert "<table" in html
        assert "x_cont" in html

    def test_to_html_writes_file(
        self, mixed_df: pd.DataFrame, tmp_path: object
    ) -> None:
        from pathlib import Path

        path = Path(tmp_path) / "describe.html"  # type: ignore[arg-type]
        result = describe(mixed_df)
        result.to_html(path)
        assert path.exists()
        assert "<table" in path.read_text()

    def test_to_plotly_json_structure(self, mixed_df: pd.DataFrame) -> None:
        result = describe(mixed_df)
        spec = result.to_plotly_json()
        assert spec["data"][0]["type"] == "table"
        assert "n_rows=10" in str(spec["layout"]["title"])


class TestEdgeCases:
    def test_empty_columns_raises(self) -> None:
        empty = pd.DataFrame()
        with pytest.raises(ValueError, match="no columns"):
            describe(empty)

    def test_all_missing_column(self) -> None:
        df = pd.DataFrame({"all_nan": [np.nan, np.nan, np.nan]})
        result = describe(df)
        row = result.summary.loc["all_nan"]
        assert row["n_missing"] == 3
        assert row["n_unique"] == 0
        assert row["top"] is None
