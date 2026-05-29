"""Reliability-diagram plots for regression + multi-class calibration.

H-0015 PR-M3 (design A): two thin dispatchers reusing the existing
``_backend`` dispatch and the shipped tables. Invariants under test:

* binary ``calibration_curve`` untouched (covered by test_error_calibration.py)
* plotted points equal the table values (plot can't disagree with its metric)
* regression axes auto-scale to the data range (NOT clamped to [0, 1])
* multi-class OvR stays on [0, 1] x [0, 1] with a single y = x reference
* backend dispatch parity: unknown backend raises
"""

from __future__ import annotations

import numpy as np
import pytest

from pycatdap.error import (
    multiclass_calibration_curve,
    multiclass_calibration_table,
    regression_calibration_curve,
    regression_calibration_table,
)


def _reg_data() -> tuple[np.ndarray, np.ndarray]:
    """Predictions spanning ~[0, 100] -> a range well outside [0, 1]."""
    rng = np.random.default_rng(0)
    n = 300
    y_pred = rng.uniform(0.0, 100.0, size=n)
    y_true = y_pred + rng.normal(0.0, 5.0, size=n)
    return y_true, y_pred


def _mc_data() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(1)
    n = 300
    y_true = rng.integers(0, 3, size=n)
    logits = rng.normal(size=(n, 3))
    logits[np.arange(n), y_true] += 1.5  # mild signal
    proba = np.exp(logits)
    proba /= proba.sum(axis=1, keepdims=True)
    return y_true, proba


# --------------------------------------------------------------------------- #
# Regression reliability diagram
# --------------------------------------------------------------------------- #


def test_regression_curve_matplotlib_returns_axes() -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    yt, yp = _reg_data()
    ax = regression_calibration_curve(yt, yp, n_quantiles=5, backend="matplotlib")
    assert isinstance(ax, Axes)


def test_regression_curve_not_clamped_to_unit_interval() -> None:
    """Regression axes must follow the data range, not [0, 1]."""
    pytest.importorskip("matplotlib")
    yt, yp = _reg_data()
    ax = regression_calibration_curve(yt, yp, n_quantiles=5, backend="matplotlib")
    assert ax.get_xlim()[1] > 1.0
    assert ax.get_ylim()[1] > 1.0


def test_regression_curve_accepts_existing_ax() -> None:
    plt = pytest.importorskip("matplotlib.pyplot")
    _fig, ax = plt.subplots()
    yt, yp = _reg_data()
    ret = regression_calibration_curve(yt, yp, ax=ax, backend="matplotlib")
    assert ret is ax


def test_regression_curve_plotly_points_match_table() -> None:
    pytest.importorskip("plotly")
    yt, yp = _reg_data()
    table = regression_calibration_table(yt, yp, n_quantiles=5)
    fig = regression_calibration_curve(yt, yp, n_quantiles=5, backend="plotly")
    model = next(t for t in fig.data if t.name == "model")
    np.testing.assert_allclose(np.asarray(model.x), table["pred_mean"].to_numpy())
    np.testing.assert_allclose(np.asarray(model.y), table["actual_mean"].to_numpy())


# --------------------------------------------------------------------------- #
# Multi-class one-vs-rest reliability diagram
# --------------------------------------------------------------------------- #


def test_multiclass_curve_matplotlib_returns_axes_on_unit_square() -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    yt, proba = _mc_data()
    ax = multiclass_calibration_curve(yt, proba, backend="matplotlib")
    assert isinstance(ax, Axes)
    assert ax.get_xlim() == (0.0, 1.0)
    assert ax.get_ylim() == (0.0, 1.0)


def test_multiclass_curve_plotly_one_trace_per_class() -> None:
    pytest.importorskip("plotly")
    yt, proba = _mc_data()
    fig = multiclass_calibration_curve(yt, proba, backend="plotly")
    names = [t.name for t in fig.data]
    assert "perfect" in names
    assert sum(n != "perfect" for n in names) == 3


def test_multiclass_curve_points_match_per_class_table() -> None:
    pytest.importorskip("plotly")
    yt, proba = _mc_data()
    tables = multiclass_calibration_table(yt, proba)
    fig = multiclass_calibration_curve(yt, proba, backend="plotly")
    for cls, table in tables.items():
        trace = next(t for t in fig.data if t.name == f"class {cls}")
        np.testing.assert_allclose(np.asarray(trace.x), table["prob_pred"].to_numpy())
        np.testing.assert_allclose(np.asarray(trace.y), table["prob_true"].to_numpy())


# --------------------------------------------------------------------------- #
# Backend dispatch parity
# --------------------------------------------------------------------------- #


def test_regression_curve_unknown_backend_raises() -> None:
    yt, yp = _reg_data()
    with pytest.raises(ValueError, match="backend"):
        regression_calibration_curve(yt, yp, backend="ggplot")  # type: ignore[arg-type]


def test_multiclass_curve_unknown_backend_raises() -> None:
    yt, proba = _mc_data()
    with pytest.raises(ValueError, match="backend"):
        multiclass_calibration_curve(yt, proba, backend="ggplot")  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# matplotlib backend: plotted points must equal the table values
# --------------------------------------------------------------------------- #


def test_regression_curve_matplotlib_points_match_table() -> None:
    pytest.importorskip("matplotlib")
    yt, yp = _reg_data()
    table = regression_calibration_table(yt, yp, n_quantiles=5)
    ax = regression_calibration_curve(yt, yp, n_quantiles=5, backend="matplotlib")
    # lines[0] = perfect y=x reference; lines[1] = the errorbar model line.
    model = ax.lines[1]
    np.testing.assert_allclose(
        np.asarray(model.get_xdata(), dtype=float), table["pred_mean"].to_numpy()
    )
    np.testing.assert_allclose(
        np.asarray(model.get_ydata(), dtype=float), table["actual_mean"].to_numpy()
    )


def test_multiclass_curve_matplotlib_points_match_table() -> None:
    pytest.importorskip("matplotlib")
    yt, proba = _mc_data()
    tables = multiclass_calibration_table(yt, proba)
    ax = multiclass_calibration_curve(yt, proba, backend="matplotlib")
    # lines[0] = perfect; lines[1:] = one per non-empty class in tables order.
    for line, (_cls, table) in zip(ax.lines[1:], tables.items(), strict=False):
        np.testing.assert_allclose(
            np.asarray(line.get_xdata(), dtype=float), table["prob_pred"].to_numpy()
        )
        np.testing.assert_allclose(
            np.asarray(line.get_ydata(), dtype=float), table["prob_true"].to_numpy()
        )
