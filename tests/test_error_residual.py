"""Tests for Phase J residual visualization (H-0012 PR-H2).

Covers:

- ``residual_plot`` — 3 plot kinds × both backends, color_by mode,
  length-mismatch / unknown-kind errors
- ``residual_by_category`` — categorical + Categorical-dtype + continuous
  (AIC-binned + equal-width) variants × both backends
- ``residual_pool_plot`` — AIC pooled |residual| with boundary lines,
  both backends
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap.error import (
    residual_by_category,
    residual_plot,
    residual_pool_plot,
)


@pytest.fixture()
def reg_data() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(11)
    y_true = rng.normal(loc=10, scale=2.0, size=120)
    y_pred = y_true + rng.normal(loc=0.5, scale=1.0, size=120)
    return y_true, y_pred


# ---------- residual_plot (matplotlib) ----------


@pytest.mark.parametrize(
    "kind",
    ["scatter_pred_resid", "scatter_true_pred", "histogram"],
)
def test_residual_plot_matplotlib_kinds(
    reg_data: tuple[np.ndarray, np.ndarray], kind: str
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    y_true, y_pred = reg_data
    ax = residual_plot(y_true, y_pred, kind=kind, backend="matplotlib")
    assert isinstance(ax, Axes)


def test_residual_plot_matplotlib_accepts_ax(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    plt = pytest.importorskip("matplotlib.pyplot")
    y_true, y_pred = reg_data
    _fig, ax = plt.subplots()
    ret = residual_plot(y_true, y_pred, backend="matplotlib", ax=ax)
    assert ret is ax


def test_residual_plot_color_by_numeric(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = reg_data
    color = np.arange(len(y_true), dtype=float)
    ax = residual_plot(y_true, y_pred, color_by=color, backend="matplotlib")
    assert ax is not None


def test_residual_plot_color_by_length_mismatch_raises(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = reg_data
    with pytest.raises(ValueError, match="color_by length"):
        residual_plot(y_true, y_pred, color_by=np.zeros(5), backend="matplotlib")


def test_residual_plot_unknown_kind_raises(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = reg_data
    with pytest.raises(ValueError, match="unknown kind"):
        residual_plot(y_true, y_pred, kind="weird", backend="matplotlib")


def test_residual_plot_length_mismatch_raises() -> None:
    pytest.importorskip("matplotlib")
    with pytest.raises(ValueError, match="must have the same length"):
        residual_plot([1.0, 2.0, 3.0], [1.0, 2.0], backend="matplotlib")


# ---------- residual_plot (plotly) ----------


@pytest.mark.parametrize(
    "kind",
    ["scatter_pred_resid", "scatter_true_pred", "histogram"],
)
def test_residual_plot_plotly_kinds(
    reg_data: tuple[np.ndarray, np.ndarray], kind: str
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    y_true, y_pred = reg_data
    fig = residual_plot(y_true, y_pred, kind=kind, backend="plotly")
    assert isinstance(fig, go.Figure)


def test_residual_plot_plotly_color_by_numeric(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    y_true, y_pred = reg_data
    fig = residual_plot(
        y_true,
        y_pred,
        color_by=np.arange(len(y_true), dtype=float),
        backend="plotly",
    )
    assert isinstance(fig, go.Figure)


# ---------- residual_by_category ----------


@pytest.fixture()
def reg_df_categorical() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(31)
    n = 150
    group = rng.choice(["A", "B", "C"], size=n)
    y_true = rng.normal(loc=0, scale=1.0, size=n)
    bias = np.where(group == "A", -1.5, np.where(group == "B", 0.5, 1.2))
    y_pred = y_true + bias + rng.normal(0, 0.3, size=n)
    df = pd.DataFrame({"group": group})
    return df, y_true, y_pred


@pytest.fixture()
def reg_df_continuous() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(32)
    n = 200
    x = rng.uniform(0, 10, size=n)
    y_true = x * 2.0 + rng.normal(0, 0.5, size=n)
    # Predictor underestimates when x > 5
    y_pred = y_true.copy()
    y_pred[x > 5] -= 1.5
    df = pd.DataFrame({"x": x})
    return df, y_true, y_pred


def test_residual_by_category_matplotlib_categorical(
    reg_df_categorical: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    df, y_true, y_pred = reg_df_categorical
    ax = residual_by_category(df, y_true, y_pred, "group", backend="matplotlib")
    assert isinstance(ax, Axes)


def test_residual_by_category_matplotlib_continuous_aic_bins(
    reg_df_continuous: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    df, y_true, y_pred = reg_df_continuous
    ax = residual_by_category(df, y_true, y_pred, "x", backend="matplotlib")
    assert isinstance(ax, Axes)


def test_residual_by_category_matplotlib_continuous_equal_width(
    reg_df_continuous: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = reg_df_continuous
    ax = residual_by_category(df, y_true, y_pred, "x", bins=4, backend="matplotlib")
    # 4 equal-width bins -> at most 4 boxes (some may be empty)
    assert ax is not None


def test_residual_by_category_plotly_categorical(
    reg_df_categorical: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    df, y_true, y_pred = reg_df_categorical
    fig = residual_by_category(df, y_true, y_pred, "group", backend="plotly")
    assert isinstance(fig, go.Figure)
    # 3 categories -> 3 Box traces
    assert len(fig.data) == 3


def test_residual_by_category_plotly_continuous(
    reg_df_continuous: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    df, y_true, y_pred = reg_df_continuous
    fig = residual_by_category(df, y_true, y_pred, "x", bins=3, backend="plotly")
    assert isinstance(fig, go.Figure)


def test_residual_by_category_categorical_dtype_preserves_order() -> None:
    pytest.importorskip("matplotlib")
    df = pd.DataFrame(
        {
            "g": pd.Categorical(
                ["high", "low", "high", "low"], categories=["low", "high"]
            )
        }
    )
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([0.5, 1.5, 2.5, 3.5])
    ax = residual_by_category(df, y_true, y_pred, "g", backend="matplotlib")
    labels = [t.get_text() for t in ax.get_xticklabels()]
    assert labels == ["low", "high"]


def test_residual_by_category_unknown_var_raises(
    reg_df_categorical: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = reg_df_categorical
    with pytest.raises(KeyError, match="not in df.columns"):
        residual_by_category(df, y_true, y_pred, "missing", backend="matplotlib")


def test_residual_by_category_length_mismatch_raises(
    reg_df_categorical: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = reg_df_categorical
    with pytest.raises(ValueError, match="does not match"):
        residual_by_category(
            df, y_true[:10], y_pred[:10], "group", backend="matplotlib"
        )


def test_residual_by_category_no_finite_continuous_raises() -> None:
    pytest.importorskip("matplotlib")
    df = pd.DataFrame({"x": [np.nan, np.nan, np.nan]})
    with pytest.raises(ValueError, match="no finite values"):
        residual_by_category(
            df,
            np.array([1.0, 2.0, 3.0]),
            np.array([0.5, 1.5, 2.5]),
            "x",
            backend="matplotlib",
        )


# ---------- residual_pool_plot ----------


def test_residual_pool_plot_matplotlib(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    y_true, y_pred = reg_data
    ax = residual_pool_plot(y_true, y_pred, n_bins=4, backend="matplotlib")
    assert isinstance(ax, Axes)
    assert "AIC-pooled" in ax.get_title()


def test_residual_pool_plot_plotly(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    y_true, y_pred = reg_data
    fig = residual_pool_plot(y_true, y_pred, n_bins=4, backend="plotly")
    assert isinstance(fig, go.Figure)


# ---------- exports + backend dispatch ----------


def test_phase_j_exports_from_pycatdap_error() -> None:
    assert hasattr(pycatdap.error, "residual_plot")
    assert hasattr(pycatdap.error, "residual_by_category")
    assert hasattr(pycatdap.error, "residual_pool_plot")


def test_residual_plot_unknown_backend_raises(
    reg_data: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_pred = reg_data
    with pytest.raises(ValueError, match="Unknown plot backend"):
        residual_plot(y_true, y_pred, backend="bogus")  # type: ignore[arg-type]
