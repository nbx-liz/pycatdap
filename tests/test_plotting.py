"""Tests for visualization functions."""

from __future__ import annotations

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

from pycatdap.catdap1 import catdap1
from pycatdap.catdap2 import catdap2
from pycatdap.plotting import aic_comparison_plot, barplot_twoway, mosaic_plot


@pytest.fixture()
def catdap1_result() -> object:
    df = pd.DataFrame(
        {
            "Y": ["a"] * 30 + ["b"] * 20,
            "X1": ["p"] * 20 + ["q"] * 10 + ["p"] * 5 + ["q"] * 15,
            "X2": ["m"] * 25 + ["n"] * 25,
        }
    )
    return catdap1(df, response_names=["Y"])


@pytest.fixture()
def catdap2_result() -> object:
    df = pd.DataFrame(
        {
            "Y": ["a"] * 30 + ["b"] * 20,
            "X1": ["p"] * 20 + ["q"] * 10 + ["p"] * 5 + ["q"] * 15,
            "X2": ["m"] * 25 + ["n"] * 25,
        }
    )
    return catdap2(df, pool=[2, 2, 2], response_name="Y")


@pytest.fixture()
def tway_table() -> pd.DataFrame:
    return pd.DataFrame(
        {"p": [20, 5], "q": [10, 15]},
        index=pd.Index(["a", "b"], name="Y"),
    )


class TestAicComparisonPlot:
    def test_returns_axes_catdap1(self, catdap1_result: object) -> None:
        from matplotlib.axes import Axes

        ax = aic_comparison_plot(catdap1_result)
        assert isinstance(ax, Axes)

    def test_returns_axes_catdap2(self, catdap2_result: object) -> None:
        from matplotlib.axes import Axes

        ax = aic_comparison_plot(catdap2_result)
        assert isinstance(ax, Axes)


class TestBarplotTwoway:
    def test_returns_axes(self, tway_table: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = barplot_twoway(tway_table)
        assert isinstance(ax, Axes)


class TestMosaicPlot:
    def test_returns_axes(self, tway_table: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = mosaic_plot(tway_table)
        assert isinstance(ax, Axes)
