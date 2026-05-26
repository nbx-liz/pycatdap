"""Tests for plot_variable and plot_missing dispatchers and backends."""

from __future__ import annotations

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")

from pycatdap import plot, plot_missing, plot_variable  # noqa: E402

_HAS_PLOTLY = True
try:
    import plotly.graph_objects as _go
except ImportError:  # pragma: no cover
    _HAS_PLOTLY = False


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "cont": [1.0, 2.5, 3.0, 4.5, 5.0, 6.5, 7.0, 8.5, 9.0, 10.5],
            "cat": ["a", "b", "a", "c", "a", "b", "c", "a", "b", "c"],
            "missing": [1.0, np.nan, 3.0, np.nan, 5.0, np.nan, 7.0, 8.0, 9.0, 10.0],
        }
    )


class TestPlotVariableMatplotlib:
    def test_returns_axes_continuous(self, sample_df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot_variable(sample_df, "cont")
        assert isinstance(ax, Axes)

    def test_returns_axes_categorical(self, sample_df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot_variable(sample_df, "cat")
        assert isinstance(ax, Axes)

    def test_explicit_hist(self, sample_df: pd.DataFrame) -> None:
        ax = plot_variable(sample_df, "cont", kind="hist")
        assert len(ax.patches) > 0  # histogram has patch rectangles

    def test_explicit_bar(self, sample_df: pd.DataFrame) -> None:
        ax = plot_variable(sample_df, "cat", kind="bar")
        # Bar chart has 3 categories -> 3 bars
        assert len(ax.patches) == 3

    def test_missing_column_raises(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(KeyError, match="not found"):
            plot_variable(sample_df, "nonexistent")

    def test_invalid_kind_raises(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="kind must be"):
            plot_variable(sample_df, "cont", kind="violin")


@pytest.mark.skipif(not _HAS_PLOTLY, reason="plotly not installed")
class TestPlotVariablePlotly:
    def test_returns_figure_continuous(self, sample_df: pd.DataFrame) -> None:
        fig = plot_variable(sample_df, "cont", backend="plotly")
        assert isinstance(fig, _go.Figure)
        assert fig.data[0].type == "histogram"

    def test_returns_figure_categorical(self, sample_df: pd.DataFrame) -> None:
        fig = plot_variable(sample_df, "cat", backend="plotly")
        assert isinstance(fig, _go.Figure)
        assert fig.data[0].type == "bar"

    def test_invalid_kind_raises(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="kind must be"):
            plot_variable(sample_df, "cont", kind="violin", backend="plotly")


class TestPlotMissingMatplotlib:
    def test_returns_axes(self, sample_df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot_missing(sample_df)
        assert isinstance(ax, Axes)

    def test_counts_match_isna(self, sample_df: pd.DataFrame) -> None:
        ax = plot_missing(sample_df)
        heights = [p.get_height() for p in ax.patches]
        expected = sample_df.isna().sum().to_list()
        assert heights == expected


@pytest.mark.skipif(not _HAS_PLOTLY, reason="plotly not installed")
class TestPlotMissingPlotly:
    def test_returns_figure(self, sample_df: pd.DataFrame) -> None:
        fig = plot_missing(sample_df, backend="plotly")
        assert isinstance(fig, _go.Figure)
        assert fig.data[0].type == "bar"

    def test_counts_match_isna(self, sample_df: pd.DataFrame) -> None:
        fig = plot_missing(sample_df, backend="plotly")
        ys = list(fig.data[0].y)
        expected = sample_df.isna().sum().to_list()
        assert ys == expected


class TestDispatcherRouting:
    def test_plot_variable_unknown_backend(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.plot_variable(sample_df, "cont", backend="seaborn")  # type: ignore[arg-type]

    def test_plot_missing_unknown_backend(self, sample_df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.plot_missing(sample_df, backend="seaborn")  # type: ignore[arg-type]
