"""Tests for pycatdap.target_summary / pycatdap.plot_target (H-0004)."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def cat_df() -> pd.DataFrame:
    """Categorical target × categorical explanatory."""
    rng = np.random.default_rng(0)
    n = 200
    # X correlated with Y to make ΔAIC negative
    y = rng.choice(["a", "b"], size=n, p=[0.6, 0.4])
    x = np.where(
        y == "a",
        rng.choice(["p", "q"], size=n, p=[0.8, 0.2]),
        rng.choice(["p", "q"], size=n, p=[0.2, 0.8]),
    )
    return pd.DataFrame({"y": y, "x": x})


@pytest.fixture()
def cont_df() -> pd.DataFrame:
    """Categorical target × continuous explanatory."""
    rng = np.random.default_rng(1)
    n = 300
    y = rng.choice(["pos", "neg"], size=n)
    x = np.where(y == "pos", rng.normal(5.0, 1.0, n), rng.normal(2.0, 1.0, n))
    return pd.DataFrame({"y": y, "x": x})


@pytest.fixture()
def health_df() -> pd.DataFrame:
    return pycatdap.datasets.load_health_data()


class TestTargetSummaryStructure:
    def test_returns_target_summary(self, cat_df: pd.DataFrame) -> None:
        from pycatdap import TargetSummary, target_summary

        result = target_summary(cat_df, target="y", explanatory="x")
        assert isinstance(result, TargetSummary)

    def test_required_attributes(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        for attr in (
            "target",
            "explanatory",
            "counts",
            "row_prop",
            "col_prop",
            "expected",
            "pearson_residuals",
            "delta_aic",
            "intervals",
        ):
            assert hasattr(result, attr), f"missing attribute: {attr}"

    def test_target_and_explanatory_names_preserved(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert result.target == "y"
        assert result.explanatory == "x"

    def test_counts_total_matches_non_null_rows(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert int(result.counts.to_numpy().sum()) == len(cat_df)

    def test_counts_indexed_by_target_values(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert set(result.counts.index) == {"a", "b"}


class TestProportions:
    def test_row_prop_rows_sum_to_one(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        row_sums = result.row_prop.sum(axis=1).to_numpy()
        np.testing.assert_allclose(row_sums, 1.0, atol=1e-10)

    def test_col_prop_cols_sum_to_one(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        col_sums = result.col_prop.sum(axis=0).to_numpy()
        np.testing.assert_allclose(col_sums, 1.0, atol=1e-10)


class TestExpectedAndResiduals:
    def test_expected_marginals_match(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        # Row sums of expected should match row sums of observed
        np.testing.assert_allclose(
            result.expected.sum(axis=1).to_numpy(),
            result.counts.sum(axis=1).to_numpy(),
            atol=1e-10,
        )
        np.testing.assert_allclose(
            result.expected.sum(axis=0).to_numpy(),
            result.counts.sum(axis=0).to_numpy(),
            atol=1e-10,
        )

    def test_pearson_residual_formula(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        observed = result.counts.to_numpy().astype(float)
        expected = result.expected.to_numpy().astype(float)
        manual = (observed - expected) / np.sqrt(expected)
        np.testing.assert_allclose(
            result.pearson_residuals.to_numpy(), manual, atol=1e-10
        )

    def test_residuals_indicate_strong_association(self, cat_df: pd.DataFrame) -> None:
        """The fixture data has a strong y~x relationship — at least one
        cell should have |residual| > 2."""
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert (np.abs(result.pearson_residuals.to_numpy()) > 2.0).any()


class TestDeltaAic:
    def test_matches_catdap1(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        r1 = pycatdap.catdap1(cat_df, response_names=["y"])
        expected_delta = float(r1.aic.loc["y", "x"])
        assert abs(result.delta_aic - expected_delta) < 1e-9

    def test_negative_for_informative_pair(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert result.delta_aic < 0


class TestContinuousExplanatory:
    def test_bins_none_uses_aic_optimal(self, cont_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cont_df, target="y", explanatory="x")
        # intervals must be populated for continuous explanatory
        assert result.intervals is not None
        assert len(result.intervals) >= 1
        # ΔAIC must match catdap2 with pool=[2, 0]
        r2 = pycatdap.catdap2(
            cont_df[["y", "x"]],
            pool=[2, 0],
            response_name="y",
        )
        expected_delta = float(r2.aic.loc[r2.aic["variable"] == "x", "aic"].iloc[0])
        assert abs(result.delta_aic - expected_delta) < 1e-6

    def test_bins_int_uses_equal_width(self, cont_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cont_df, target="y", explanatory="x", bins=4)
        assert result.intervals is not None
        # n_bins = len(intervals) + 1 should be 4
        assert len(result.intervals) == 3

    def test_bins_explicit_list(self, cont_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(
            cont_df, target="y", explanatory="x", bins=[2.0, 3.5, 5.0]
        )
        assert result.intervals == [2.0, 3.5, 5.0]

    def test_intervals_none_for_categorical(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        assert result.intervals is None


class TestMethods:
    def test_show_does_not_raise(
        self, cat_df: pd.DataFrame, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        result.show()  # Should not raise

    def test_to_dict_is_json_serializable(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        as_dict = result.to_dict()
        # round-trip through JSON to confirm serializability
        encoded = json.dumps(as_dict)
        decoded = json.loads(encoded)
        assert decoded["target"] == "y"
        assert decoded["explanatory"] == "x"
        assert "counts" in decoded
        assert "delta_aic" in decoded

    def test_to_html_returns_string(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        html = result.to_html()
        assert isinstance(html, str)
        assert "<html" in html.lower()
        assert "y" in html and "x" in html

    def test_to_html_writes_file(self, cat_df: pd.DataFrame, tmp_path: Any) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        out = tmp_path / "report.html"
        result.to_html(path=out)
        assert out.exists() and out.stat().st_size > 0

    def test_to_plotly_json_spec(self, cat_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(cat_df, target="y", explanatory="x")
        spec = result.to_plotly_json()
        assert isinstance(spec, dict)
        assert "data" in spec
        assert "layout" in spec


class TestErrors:
    def test_unknown_target_raises_key_error(self, cat_df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            pycatdap.target_summary(cat_df, target="missing", explanatory="x")

    def test_unknown_explanatory_raises_key_error(self, cat_df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            pycatdap.target_summary(cat_df, target="y", explanatory="missing")

    def test_continuous_target_raises_value_error(self, cont_df: pd.DataFrame) -> None:
        # swap: target is the continuous column → should fail
        with pytest.raises(ValueError, match="continuous"):
            pycatdap.target_summary(cont_df, target="x", explanatory="y")

    def test_nan_rows_dropped(self, cat_df: pd.DataFrame) -> None:
        polluted = cat_df.copy()
        polluted.loc[0, "x"] = np.nan
        polluted.loc[1, "y"] = np.nan
        result = pycatdap.target_summary(polluted, target="y", explanatory="x")
        assert int(result.counts.to_numpy().sum()) == len(cat_df) - 2


class TestRealDatasetIntegration:
    def test_health_symptoms_vs_cholesterol(self, health_df: pd.DataFrame) -> None:
        result = pycatdap.target_summary(
            health_df, target="symptoms", explanatory="cholesterol"
        )
        # Sanity: counts sum to all non-null rows
        assert int(result.counts.to_numpy().sum()) == len(
            health_df.dropna(subset=["symptoms", "cholesterol"])
        )
        # ΔAIC agrees with catdap1
        r1 = pycatdap.catdap1(
            health_df[["symptoms", "cholesterol"]],
            response_names=["symptoms"],
        )
        np.testing.assert_allclose(
            result.delta_aic,
            float(r1.aic.loc["symptoms", "cholesterol"]),
            atol=1e-9,
        )


# ---------------------------------------------------------------------------
# plot_target tests
# ---------------------------------------------------------------------------


class TestPlotTargetDispatch:
    def test_cat_cat_auto_returns_axes(self, cat_df: pd.DataFrame) -> None:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib.axes import Axes

        ax = pycatdap.plot_target(cat_df, target="y", explanatory="x")
        assert isinstance(ax, Axes)

    def test_cat_cont_auto_returns_axes(self, cont_df: pd.DataFrame) -> None:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib.axes import Axes

        ax = pycatdap.plot_target(cont_df, target="y", explanatory="x")
        assert isinstance(ax, Axes)

    def test_plotly_backend_returns_figure(self, cat_df: pd.DataFrame) -> None:
        plotly = pytest.importorskip("plotly")
        fig = pycatdap.plot_target(
            cat_df, target="y", explanatory="x", backend="plotly"
        )
        assert isinstance(fig, plotly.graph_objs.Figure)

    def test_continuous_target_auto_raises(self, cont_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="continuous"):
            pycatdap.plot_target(cont_df, target="x", explanatory="y")

    def test_explicit_kind_overrides_auto(self, cat_df: pd.DataFrame) -> None:
        import matplotlib

        matplotlib.use("Agg")
        from matplotlib.axes import Axes

        ax = pycatdap.plot_target(cat_df, target="y", explanatory="x", kind="mosaic")
        assert isinstance(ax, Axes)
