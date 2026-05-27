"""Tests for pycatdap.plot_pair (H-0006 PR-B1).

plot_pair is a symmetric wrapper that decides which side of (x, y) is
the response based on dtypes, then delegates to plot_target.
"""

from __future__ import annotations

from typing import Any

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

import pycatdap
from pycatdap import plot


def _make_df() -> pd.DataFrame:
    """Build a frame containing one column of every dtype kind we care about."""
    rng = np.random.default_rng(seed=42)
    n = 60
    return pd.DataFrame(
        {
            "cat_a": rng.choice(["x", "y", "z"], size=n),
            "cat_b": rng.choice(["m", "n"], size=n),
            "bool_a": rng.choice([True, False], size=n),
            "cont_a": rng.normal(loc=0.0, scale=1.0, size=n),
            "cont_b": rng.normal(loc=5.0, scale=2.0, size=n),
        }
    )


@pytest.fixture()
def df() -> pd.DataFrame:
    return _make_df()


class _PlotTargetSpy:
    """Capture the (target, explanatory, kwargs) plot_target receives.

    Replaces the real ``plot_target`` symbol on the ``pycatdap.plot`` module
    so we can verify ``plot_pair``'s response-side decision without driving
    a real backend.
    """

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        df: pd.DataFrame,
        target: str,
        explanatory: str,
        **kwargs: Any,
    ) -> str:
        self.calls.append(
            {
                "df": df,
                "target": target,
                "explanatory": explanatory,
                "kwargs": kwargs,
            }
        )
        return "SPY_RETURN"


@pytest.fixture()
def spy(monkeypatch: pytest.MonkeyPatch) -> _PlotTargetSpy:
    spy = _PlotTargetSpy()
    monkeypatch.setattr(plot, "plot_target", spy)
    return spy


class TestPublicSurface:
    """plot_pair is re-exported at both top-level and pycatdap.plot."""

    def test_importable_from_pycatdap(self) -> None:
        assert hasattr(pycatdap, "plot_pair")
        assert callable(pycatdap.plot_pair)

    def test_importable_from_pycatdap_plot(self) -> None:
        assert hasattr(plot, "plot_pair")
        assert callable(plot.plot_pair)

    def test_top_level_and_dispatcher_are_same_object(self) -> None:
        assert pycatdap.plot_pair is plot.plot_pair


class TestResponseRule:
    """plot_pair's dtype-based response-side decision (H-0006 §Proposal)."""

    def test_cat_x_cat_y_response_is_y(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        plot.plot_pair(df, "cat_a", "cat_b")
        assert spy.calls[0]["target"] == "cat_b"
        assert spy.calls[0]["explanatory"] == "cat_a"

    def test_cat_x_cont_y_response_is_x(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        plot.plot_pair(df, "cat_a", "cont_a")
        assert spy.calls[0]["target"] == "cat_a"
        assert spy.calls[0]["explanatory"] == "cont_a"

    def test_cont_x_cat_y_response_is_y(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        plot.plot_pair(df, "cont_a", "cat_a")
        assert spy.calls[0]["target"] == "cat_a"
        assert spy.calls[0]["explanatory"] == "cont_a"

    def test_cont_x_cont_y_response_is_y(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        plot.plot_pair(df, "cont_a", "cont_b")
        assert spy.calls[0]["target"] == "cont_b"
        assert spy.calls[0]["explanatory"] == "cont_a"

    def test_boolean_is_treated_as_discrete_side(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        """Boolean × continuous → boolean wins as target (discrete side rule)."""
        plot.plot_pair(df, "cont_a", "bool_a")
        assert spy.calls[0]["target"] == "bool_a"
        assert spy.calls[0]["explanatory"] == "cont_a"

    def test_boolean_x_categorical_y_is_target(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        """Both-discrete: y wins regardless of which is bool vs cat."""
        plot.plot_pair(df, "bool_a", "cat_a")
        assert spy.calls[0]["target"] == "cat_a"
        assert spy.calls[0]["explanatory"] == "bool_a"


class TestKwargForwarding:
    """plot_pair forwards kind/bins/backend/**kwargs to plot_target."""

    def test_kind_is_forwarded(self, df: pd.DataFrame, spy: _PlotTargetSpy) -> None:
        plot.plot_pair(df, "cat_a", "cont_a", kind="violin")
        assert spy.calls[0]["kwargs"]["kind"] == "violin"

    def test_bins_is_forwarded(self, df: pd.DataFrame, spy: _PlotTargetSpy) -> None:
        plot.plot_pair(df, "cat_a", "cont_a", bins=4)
        assert spy.calls[0]["kwargs"]["bins"] == 4

    def test_backend_is_forwarded(self, df: pd.DataFrame, spy: _PlotTargetSpy) -> None:
        plot.plot_pair(df, "cat_a", "cat_b", backend="plotly")
        assert spy.calls[0]["kwargs"]["backend"] == "plotly"

    def test_extra_kwargs_are_forwarded(
        self, df: pd.DataFrame, spy: _PlotTargetSpy
    ) -> None:
        plot.plot_pair(df, "cat_a", "cat_b", title="hello")
        assert spy.calls[0]["kwargs"]["title"] == "hello"

    def test_default_kind_is_auto(self, df: pd.DataFrame, spy: _PlotTargetSpy) -> None:
        plot.plot_pair(df, "cat_a", "cat_b")
        assert spy.calls[0]["kwargs"]["kind"] == "auto"


class TestErrorPaths:
    """plot_pair surfaces clear errors for invalid input."""

    def test_missing_x_column_raises_keyerror(self, df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            plot.plot_pair(df, "does_not_exist", "cat_a")

    def test_missing_y_column_raises_keyerror(self, df: pd.DataFrame) -> None:
        with pytest.raises(KeyError):
            plot.plot_pair(df, "cat_a", "does_not_exist")

    def test_unknown_backend_raises(self, df: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.plot_pair(df, "cat_a", "cat_b", backend="seaborn")  # type: ignore[arg-type]


class TestEndToEnd:
    """plot_pair actually produces a backend figure object."""

    def test_default_backend_returns_matplotlib_axes(self, df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.plot_pair(df, "cat_a", "cat_b")
        assert isinstance(ax, Axes)

    def test_plotly_backend_returns_figure(self, df: pd.DataFrame) -> None:
        pytest.importorskip("plotly")
        from plotly.graph_objects import Figure

        fig = plot.plot_pair(df, "cat_a", "cat_b", backend="plotly")
        assert isinstance(fig, Figure)

    def test_cat_x_cont_returns_matplotlib_axes(self, df: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.plot_pair(df, "cat_a", "cont_a")
        assert isinstance(ax, Axes)

    def test_cont_x_cont_returns_matplotlib_axes_via_regression_mode(
        self, df: pd.DataFrame
    ) -> None:
        """H-0005 regression mode (scatter) for both-continuous pair."""
        from matplotlib.axes import Axes

        ax = plot.plot_pair(df, "cont_a", "cont_b")
        assert isinstance(ax, Axes)
