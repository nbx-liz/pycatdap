"""Tests for pycatdap.aic_heatmap (H-0006 PR-B2)."""

from __future__ import annotations

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

import pycatdap
from pycatdap import plot
from pycatdap.catdap1 import catdap1


@pytest.fixture()
def catdap1_result() -> object:
    rng = np.random.default_rng(seed=11)
    n = 80
    df = pd.DataFrame(
        {
            "Y1": rng.choice(["a", "b"], size=n),
            "Y2": rng.choice(["p", "q", "r"], size=n),
            "X1": rng.choice(["m", "n"], size=n),
            "X2": rng.choice(["u", "v", "w"], size=n),
        }
    )
    return catdap1(df, response_names=["Y1", "Y2"])


@pytest.fixture()
def aic_df() -> pd.DataFrame:
    """A small ΔAIC matrix with both negative and positive values + NaN diagonal."""
    data = pd.DataFrame(
        [
            [np.nan, -5.2, 3.1, -1.8],
            [-4.0, np.nan, 0.5, -2.2],
            [2.0, 1.1, np.nan, 0.0],
        ],
        index=["Y1", "Y2", "Y3"],
        columns=["Y1", "Y2", "Y3", "X1"],
    )
    return data


class TestPublicSurface:
    """aic_heatmap is re-exported at both top-level and pycatdap.plot."""

    def test_importable_from_pycatdap(self) -> None:
        assert hasattr(pycatdap, "aic_heatmap")
        assert callable(pycatdap.aic_heatmap)

    def test_importable_from_pycatdap_plot(self) -> None:
        assert hasattr(plot, "aic_heatmap")
        assert callable(plot.aic_heatmap)

    def test_top_level_and_dispatcher_are_same_object(self) -> None:
        assert pycatdap.aic_heatmap is plot.aic_heatmap


class TestInputTypes:
    """Accepts Catdap1Result or pd.DataFrame."""

    def test_accepts_catdap1_result(self, catdap1_result: object) -> None:
        from matplotlib.axes import Axes

        ax = plot.aic_heatmap(catdap1_result)  # type: ignore[arg-type]
        assert isinstance(ax, Axes)

    def test_accepts_dataframe(self, aic_df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.aic_heatmap(aic_df)
        assert isinstance(ax, Axes)

    def test_rejects_other_types(self) -> None:
        with pytest.raises(TypeError, match="Catdap1Result"):
            plot.aic_heatmap([1, 2, 3])  # type: ignore[arg-type]


class TestBackendDispatch:
    """Backend routing matches the rest of pycatdap.plot."""

    def test_default_backend_is_matplotlib(self, aic_df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.aic_heatmap(aic_df)
        assert isinstance(ax, Axes)

    def test_plotly_backend_returns_figure(self, aic_df: pd.DataFrame) -> None:
        pytest.importorskip("plotly")
        from plotly.graph_objects import Figure

        fig = plot.aic_heatmap(aic_df, backend="plotly")
        assert isinstance(fig, Figure)

    def test_unknown_backend_raises(self, aic_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.aic_heatmap(aic_df, backend="seaborn")  # type: ignore[arg-type]


class TestRenderedValues:
    """The rendered heatmap reflects the underlying matrix."""

    def test_matplotlib_image_data_matches_input(self, aic_df: pd.DataFrame) -> None:
        """imshow's data array should equal the input matrix (NaN preserved)."""
        ax = plot.aic_heatmap(aic_df)
        images = ax.get_images()
        assert len(images) == 1
        rendered = images[0].get_array()
        # Accept both MaskedArray and ndarray return shapes.
        if hasattr(rendered, "filled"):
            rendered_np = np.asarray(rendered.filled(np.nan))
        else:
            rendered_np = np.asarray(rendered)
        np.testing.assert_allclose(rendered_np, aic_df.to_numpy(), equal_nan=True)

    def test_plotly_z_data_matches_input(self, aic_df: pd.DataFrame) -> None:
        pytest.importorskip("plotly")

        fig = plot.aic_heatmap(aic_df, backend="plotly")
        z = fig.data[0].z
        np.testing.assert_allclose(
            np.asarray(z, dtype=float), aic_df.to_numpy(), equal_nan=True
        )

    def test_axis_labels_match_dataframe_axes(self, aic_df: pd.DataFrame) -> None:
        ax = plot.aic_heatmap(aic_df)
        xtick_labels = [t.get_text() for t in ax.get_xticklabels()]
        ytick_labels = [t.get_text() for t in ax.get_yticklabels()]
        # Labels are set after draw; force a draw.
        ax.figure.canvas.draw()
        xtick_labels = [t.get_text() for t in ax.get_xticklabels()]
        ytick_labels = [t.get_text() for t in ax.get_yticklabels()]
        assert xtick_labels == list(aic_df.columns)
        assert ytick_labels == list(aic_df.index)


class TestColormap:
    """Diverging colormap centered at 0."""

    def test_matplotlib_uses_diverging_norm_centered_at_zero(
        self, aic_df: pd.DataFrame
    ) -> None:
        ax = plot.aic_heatmap(aic_df)
        img = ax.get_images()[0]
        norm = img.norm
        # TwoSlopeNorm centers at vcenter; either way vcenter / midpoint = 0.
        vcenter = getattr(norm, "vcenter", None)
        assert vcenter == 0.0, (
            "matplotlib aic_heatmap must use a diverging norm centered at 0"
        )

    def test_plotly_uses_diverging_colorscale_centered_at_zero(
        self, aic_df: pd.DataFrame
    ) -> None:
        pytest.importorskip("plotly")

        fig = plot.aic_heatmap(aic_df, backend="plotly")
        trace = fig.data[0]
        assert trace.zmid == 0
