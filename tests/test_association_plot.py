"""Tests for pycatdap.association_plot (H-0006 PR-B3).

vcd-style heatmap of Pearson standardized residuals from a two-way
contingency table or a TargetSummary.
"""

from __future__ import annotations

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

import pycatdap
from pycatdap import plot, target_summary


@pytest.fixture()
def cat_df() -> pd.DataFrame:
    rng = np.random.default_rng(seed=2026)
    n = 120
    target_levels = rng.choice(["a", "b", "c"], size=n)
    # Build an explanatory whose distribution depends on target -> non-zero residuals
    expl = np.where(
        target_levels == "a",
        rng.choice(["x", "y"], size=n, p=[0.8, 0.2]),
        rng.choice(["x", "y"], size=n, p=[0.3, 0.7]),
    )
    return pd.DataFrame({"target": target_levels, "expl": expl})


@pytest.fixture()
def ts(cat_df: pd.DataFrame) -> object:
    return target_summary(cat_df, target="target", explanatory="expl")


@pytest.fixture()
def crosstab(cat_df: pd.DataFrame) -> pd.DataFrame:
    return pd.crosstab(cat_df["target"], cat_df["expl"])


class TestPublicSurface:
    def test_importable_from_pycatdap(self) -> None:
        assert hasattr(pycatdap, "association_plot")
        assert callable(pycatdap.association_plot)

    def test_importable_from_pycatdap_plot(self) -> None:
        assert hasattr(plot, "association_plot")
        assert callable(plot.association_plot)

    def test_top_level_and_dispatcher_are_same_object(self) -> None:
        assert pycatdap.association_plot is plot.association_plot


class TestInputTypes:
    """Accepts TargetSummary or pd.DataFrame (raw crosstab)."""

    def test_accepts_target_summary(self, ts: object) -> None:
        from matplotlib.axes import Axes

        ax = plot.association_plot(ts)  # type: ignore[arg-type]
        assert isinstance(ax, Axes)

    def test_accepts_crosstab_dataframe(self, crosstab: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.association_plot(crosstab)
        assert isinstance(ax, Axes)

    def test_rejects_regression_target_summary(self, cat_df: pd.DataFrame) -> None:
        """Continuous target has no Pearson-residual concept; clear pointer."""
        rng = np.random.default_rng(seed=1)
        df_reg = pd.DataFrame(
            {
                "y_cont": rng.normal(0.0, 1.0, size=80),
                "expl": rng.choice(["a", "b"], size=80),
            }
        )
        reg_summary = target_summary(df_reg, target="y_cont", explanatory="expl")
        with pytest.raises(TypeError, match="RegressionTargetSummary"):
            plot.association_plot(reg_summary)  # type: ignore[arg-type]

    def test_rejects_other_types(self) -> None:
        with pytest.raises(TypeError, match="TargetSummary"):
            plot.association_plot([[1, 2], [3, 4]])  # type: ignore[arg-type]


class TestBackendDispatch:
    def test_default_backend_is_matplotlib(self, ts: object) -> None:
        from matplotlib.axes import Axes

        ax = plot.association_plot(ts)  # type: ignore[arg-type]
        assert isinstance(ax, Axes)

    def test_plotly_backend_returns_figure(self, ts: object) -> None:
        pytest.importorskip("plotly")
        from plotly.graph_objects import Figure

        fig = plot.association_plot(ts, backend="plotly")  # type: ignore[arg-type]
        assert isinstance(fig, Figure)

    def test_unknown_backend_raises(self, ts: object) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.association_plot(ts, backend="seaborn")  # type: ignore[arg-type]


class TestResidualComputation:
    """When given a raw crosstab, association_plot computes Pearson residuals."""

    def test_matches_target_summary_residuals(
        self, ts: object, crosstab: pd.DataFrame
    ) -> None:
        """A direct call on the crosstab must reach the same residual matrix
        as target_summary did, i.e. (obs - exp) / sqrt(exp)."""
        ax_from_ts = plot.association_plot(ts)  # type: ignore[arg-type]
        ax_from_df = plot.association_plot(crosstab)

        # Recover the matrices each axes drew.
        z_ts = ax_from_ts.get_images()[0].get_array()
        z_df = ax_from_df.get_images()[0].get_array()
        np.testing.assert_allclose(np.asarray(z_ts), np.asarray(z_df))


class TestColormap:
    """Diverging colormap centered at zero (vcd assoc(shade=TRUE) style)."""

    def test_matplotlib_uses_diverging_norm_centered_at_zero(self, ts: object) -> None:
        ax = plot.association_plot(ts)  # type: ignore[arg-type]
        img = ax.get_images()[0]
        vcenter = getattr(img.norm, "vcenter", None)
        assert vcenter == 0.0

    def test_plotly_uses_diverging_colorscale_centered_at_zero(
        self, ts: object
    ) -> None:
        pytest.importorskip("plotly")

        fig = plot.association_plot(ts, backend="plotly")  # type: ignore[arg-type]
        assert fig.data[0].zmid == 0


class TestThresholdAnnotation:
    """Cells with |residual| > threshold get a '*' annotation."""

    def test_matplotlib_threshold_annotates_strong_residuals(self, ts: object) -> None:
        ax = plot.association_plot(ts, threshold=0.5)  # type: ignore[arg-type]
        # Texts include only the '*' annotations (not axis labels).
        annotations = [t for t in ax.texts if t.get_text() == "*"]
        residuals = ts.pearson_residuals.to_numpy()  # type: ignore[attr-defined]
        expected_count = int(np.sum(np.abs(residuals) > 0.5))
        assert len(annotations) == expected_count

    def test_threshold_none_disables_annotations(self, ts: object) -> None:
        ax = plot.association_plot(ts, threshold=None)  # type: ignore[arg-type]
        annotations = [t for t in ax.texts if t.get_text() == "*"]
        assert annotations == []


class TestAxisLabels:
    """Tick labels match the rows/columns of the residual matrix."""

    def test_matplotlib_axis_labels(self, ts: object) -> None:
        ax = plot.association_plot(ts)  # type: ignore[arg-type]
        ax.figure.canvas.draw()
        xtick_labels = [t.get_text() for t in ax.get_xticklabels()]
        ytick_labels = [t.get_text() for t in ax.get_yticklabels()]
        expected_xs = [str(c) for c in ts.pearson_residuals.columns]  # type: ignore[attr-defined]
        expected_ys = [str(r) for r in ts.pearson_residuals.index]  # type: ignore[attr-defined]
        assert xtick_labels == expected_xs
        assert ytick_labels == expected_ys
