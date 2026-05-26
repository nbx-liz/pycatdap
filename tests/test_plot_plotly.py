"""Tests for the Plotly backend of pycatdap.plot."""

from __future__ import annotations

import pandas as pd
import pytest

go = pytest.importorskip("plotly.graph_objects")  # auto-skip when plotly missing

from pycatdap import plot  # noqa: E402
from pycatdap.catdap1 import catdap1  # noqa: E402
from pycatdap.catdap2 import catdap2  # noqa: E402


@pytest.fixture()
def tway_table() -> pd.DataFrame:
    return pd.DataFrame(
        {"p": [20, 5], "q": [10, 15]},
        index=pd.Index(["a", "b"], name="Y"),
    )


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


class TestMosaicPlotPlotly:
    def test_returns_figure(self, tway_table: pd.DataFrame) -> None:
        fig = plot.mosaic_plot(tway_table, backend="plotly")
        assert isinstance(fig, go.Figure)

    def test_layout_axes_are_unit_square(self, tway_table: pd.DataFrame) -> None:
        fig = plot.mosaic_plot(tway_table, backend="plotly")
        assert tuple(fig.layout.xaxis.range) == (0, 1)
        assert tuple(fig.layout.yaxis.range) == (0, 1)

    def test_traces_one_per_cell(self, tway_table: pd.DataFrame) -> None:
        # 2 rows x 2 cols = 4 cells
        fig = plot.mosaic_plot(tway_table, backend="plotly")
        assert len(fig.data) == 4

    def test_zero_total_raises(self) -> None:
        empty = pd.DataFrame(
            {"p": [0, 0], "q": [0, 0]},
            index=pd.Index(["a", "b"], name="Y"),
        )
        with pytest.raises(ValueError, match="table sum must be positive"):
            plot.mosaic_plot(empty, backend="plotly")


class TestBarplotTwowayPlotly:
    def test_returns_figure(self, tway_table: pd.DataFrame) -> None:
        fig = plot.barplot_twoway(tway_table, backend="plotly")
        assert isinstance(fig, go.Figure)

    def test_stacked_barmode(self, tway_table: pd.DataFrame) -> None:
        fig = plot.barplot_twoway(tway_table, backend="plotly")
        assert fig.layout.barmode == "stack"

    def test_one_trace_per_row(self, tway_table: pd.DataFrame) -> None:
        # 2 rows -> 2 traces
        fig = plot.barplot_twoway(tway_table, backend="plotly")
        assert len(fig.data) == 2

    def test_proportions_sum_to_one_per_column(self, tway_table: pd.DataFrame) -> None:
        fig = plot.barplot_twoway(tway_table, backend="plotly")
        # Sum across stacked traces for each x should be ~1.0
        for col_idx in range(len(tway_table.columns)):
            total = sum(trace.y[col_idx] for trace in fig.data)
            assert total == pytest.approx(1.0, abs=1e-9)


class TestAicComparisonPlotPlotly:
    def test_returns_figure(self, catdap1_result: object) -> None:
        fig = plot.aic_comparison_plot(catdap1_result, backend="plotly")
        assert isinstance(fig, go.Figure)

    def test_horizontal_bar(self, catdap1_result: object) -> None:
        fig = plot.aic_comparison_plot(catdap1_result, backend="plotly")
        assert fig.data[0].orientation == "h"

    def test_color_mapping_by_sign(self, catdap1_result: object) -> None:
        fig = plot.aic_comparison_plot(catdap1_result, backend="plotly")
        values = fig.data[0].x
        colors = fig.data[0].marker.color
        for v, c in zip(values, colors, strict=True):
            if v < 0:
                assert c == "#2ca02c", f"Expected green for {v}, got {c}"
            else:
                assert c == "#d62728", f"Expected red for {v}, got {c}"

    def test_catdap2_result_renders(self, catdap2_result: object) -> None:
        fig = plot.aic_comparison_plot(catdap2_result, backend="plotly")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
