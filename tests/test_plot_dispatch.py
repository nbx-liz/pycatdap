"""Tests for the pycatdap.plot backend dispatcher (v0.3+)."""

from __future__ import annotations

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

from pycatdap import plot
from pycatdap.catdap1 import catdap1


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


class TestBackendDispatch:
    """The plot.* dispatchers route to the requested backend."""

    def test_default_backend_is_matplotlib(self, tway_table: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.mosaic_plot(tway_table)
        assert isinstance(ax, Axes)

    def test_explicit_matplotlib_backend(self, tway_table: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        ax = plot.barplot_twoway(tway_table, backend="matplotlib")
        assert isinstance(ax, Axes)

    def test_unknown_backend_raises(self, tway_table: pd.DataFrame) -> None:
        with pytest.raises(ValueError, match="Unknown plot backend"):
            plot.mosaic_plot(tway_table, backend="seaborn")  # type: ignore[arg-type]

    def test_plotly_backend_not_implemented(self, tway_table: pd.DataFrame) -> None:
        # plotly may or may not be installed; check the right error message
        with pytest.raises((ImportError, NotImplementedError)) as excinfo:
            plot.mosaic_plot(tway_table, backend="plotly")
        msg = str(excinfo.value)
        assert "plotly" in msg.lower() or "not yet implemented" in msg.lower()


class TestBackwardCompatibilityShim:
    """The legacy pycatdap.plotting path still works."""

    def test_legacy_import_path_works(self, tway_table: pd.DataFrame) -> None:
        from matplotlib.axes import Axes

        from pycatdap.plotting import mosaic_plot

        ax = mosaic_plot(tway_table)
        assert isinstance(ax, Axes)

    def test_legacy_and_canonical_share_implementation(
        self, tway_table: pd.DataFrame
    ) -> None:
        from pycatdap.plot.matplotlib import mosaic_plot as canonical
        from pycatdap.plotting import mosaic_plot as legacy

        assert canonical is legacy


class TestToPlotlyJson:
    """Result objects expose .to_plotly_json() for web frontend consumption."""

    def test_catdap1_to_plotly_json_structure(self, catdap1_result: object) -> None:
        spec = catdap1_result.to_plotly_json()  # type: ignore[attr-defined]
        assert isinstance(spec, dict)
        assert "data" in spec
        assert "layout" in spec
        assert isinstance(spec["data"], list)
        assert spec["data"][0]["type"] == "bar"
        assert spec["data"][0]["orientation"] == "h"

    def test_catdap1_to_plotly_json_colors(self, catdap1_result: object) -> None:
        """Informative variables (negative ΔAIC) should be green, others red."""
        spec = catdap1_result.to_plotly_json()  # type: ignore[attr-defined]
        colors = spec["data"][0]["marker"]["color"]
        values = spec["data"][0]["x"]
        for value, color in zip(values, colors, strict=True):
            if value < 0:
                assert color == "#2ca02c", f"Expected green for {value}"
            else:
                assert color == "#d62728", f"Expected red for {value}"

    def test_catdap2_to_plotly_json_structure(self) -> None:
        from pycatdap.catdap2 import catdap2

        df = pd.DataFrame(
            {
                "Y": ["a"] * 30 + ["b"] * 20,
                "X1": ["p"] * 20 + ["q"] * 10 + ["p"] * 5 + ["q"] * 15,
                "X2": ["m"] * 25 + ["n"] * 25,
            }
        )
        result = catdap2(df, pool=[2, 2, 2], response_name="Y")
        spec = result.to_plotly_json()
        assert isinstance(spec, dict)
        assert "data" in spec
        assert "layout" in spec
        assert "base=" in str(spec["layout"]["title"])
