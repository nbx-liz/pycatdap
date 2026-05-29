"""Tests for ErrorAnalysisResult delegation methods (H-0012 PR-H3).

Covers:

- ``y_true`` / ``y_pred`` fields preserved by ``error_analysis()`` and
  frozen in-place (H-0009 numpy ``writeable=False``)
- :meth:`ErrorAnalysisResult.plot_confusion` delegates correctly for
  binary AND multi-class classification (H-0012 §F-ter), raises for
  regression
- :meth:`ErrorAnalysisResult.residual_plot` delegates correctly for
  regression, raises for classification
- Legacy constructor calls without ``y_true`` / ``y_pred`` still work
  (Claim 3) but delegation methods raise a clear message
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def binary_setup() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(101)
    n = 120
    df = pd.DataFrame(
        {
            "age": rng.choice(["young", "old"], size=n),
            "sex": rng.choice(["M", "F"], size=n),
        }
    )
    y_true = rng.choice([0, 1], size=n)
    y_pred = y_true.copy()
    flip = rng.random(n) < 0.2
    y_pred[flip] = 1 - y_pred[flip]
    return df, y_true, y_pred


@pytest.fixture()
def multiclass_setup() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(102)
    n = 150
    df = pd.DataFrame(
        {
            "group": rng.choice(["G1", "G2", "G3"], size=n),
        }
    )
    y_true = rng.choice(["a", "b", "c"], size=n)
    y_pred = y_true.copy()
    flip = rng.random(n) < 0.3
    other = rng.choice(["a", "b", "c"], size=int(flip.sum()))
    y_pred[flip] = other
    return df, y_true, y_pred


@pytest.fixture()
def regression_setup() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(103)
    n = 200
    df = pd.DataFrame(
        {
            "category": rng.choice(["lo", "hi"], size=n),
            "feature": rng.normal(size=n),
        }
    )
    y_true = rng.normal(loc=5.0, scale=2.0, size=n)
    y_pred = y_true + rng.normal(loc=0.5, scale=1.0, size=n)
    return df, y_true, y_pred


# ---------- y_true / y_pred preservation ----------


def test_error_analysis_stores_y_true_y_pred_binary(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    assert r.y_true is not None
    assert r.y_pred is not None
    assert np.array_equal(r.y_true, y_true)
    assert np.array_equal(r.y_pred, y_pred)


def test_error_analysis_stores_y_true_y_pred_regression(
    regression_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    df, y_true, y_pred = regression_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    assert r.y_true is not None
    assert r.y_pred is not None


def test_stored_y_true_is_frozen(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    assert r.y_true is not None
    with pytest.raises(ValueError, match="read-only|assignment"):
        r.y_true[0] = r.y_true[0]


def test_caller_y_true_array_is_not_frozen_by_error_analysis(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    """error_analysis should defensive-copy y_true / y_pred so the
    caller's array stays mutable after the call."""
    df, y_true, y_pred = binary_setup
    pycatdap.error_analysis(df, y_true, y_pred)
    # Caller's y_true must remain mutable.
    y_true[0] = y_true[0]


# ---------- plot_confusion delegation ----------


def test_result_plot_confusion_binary_matplotlib(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    ax = r.plot_confusion(backend="matplotlib")
    assert isinstance(ax, Axes)


def test_result_plot_confusion_multiclass_matplotlib(
    multiclass_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    """H-0012 §F-ter: multi-class result.plot_confusion() draws a 3×3
    heatmap rather than raising. The wrapper internally fell back to
    error_label, but the raw y_true / y_pred remain available for the
    confusion plot."""
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    df, y_true, y_pred = multiclass_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    assert r.label_kind == "error_label"  # multiclass fallback
    ax = r.plot_confusion(backend="matplotlib")
    assert isinstance(ax, Axes)
    # 3 classes -> 3 ticks
    assert len(ax.get_xticks()) == 3


def test_result_plot_confusion_plotly(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    fig = r.plot_confusion(backend="plotly")
    assert isinstance(fig, go.Figure)


def test_result_plot_confusion_regression_raises(
    regression_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = regression_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    with pytest.raises(ValueError, match="classification-only"):
        r.plot_confusion(backend="matplotlib")


def test_result_plot_confusion_forwards_kwargs(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    ax = r.plot_confusion(backend="matplotlib", normalize="true", cmap="Greens")
    # Title gains the (normalized) suffix from plot_confusion
    assert "normalized" in ax.get_title()


# ---------- residual_plot delegation ----------


def test_result_residual_plot_regression_matplotlib(
    regression_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    df, y_true, y_pred = regression_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    ax = r.residual_plot(backend="matplotlib")
    assert isinstance(ax, Axes)


def test_result_residual_plot_regression_plotly(
    regression_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    df, y_true, y_pred = regression_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    fig = r.residual_plot(backend="plotly", kind="histogram")
    assert isinstance(fig, go.Figure)


def test_result_residual_plot_classification_raises(
    binary_setup: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = binary_setup
    r = pycatdap.error_analysis(df, y_true, y_pred)
    with pytest.raises(ValueError, match="regression-only"):
        r.residual_plot(backend="matplotlib")


# ---------- Legacy / direct construction (Claim 3) ----------


def test_direct_construction_without_y_true_y_pred_works() -> None:
    """Existing test_error_analysis_result.py constructs results
    directly without y_true / y_pred — those calls must still work."""
    from types import MappingProxyType

    from pycatdap.error import ErrorAnalysisResult

    ranking = pd.DataFrame(
        [{"variable": "x", "delta_aic": -1.0, "kind": "categorical", "n_obs": 10}]
    )
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=ranking,
        top_summaries=MappingProxyType({}),
        top_slices=(),
        confusion=None,
        residual_pooling=None,
        n_rows=10,
        n_correct=8,
        n_incorrect=2,
        mae=None,
        rmse=None,
    )
    assert result.y_true is None
    assert result.y_pred is None


def test_legacy_construction_plot_confusion_raises_helpful_message() -> None:
    from types import MappingProxyType

    from pycatdap.error import ErrorAnalysisResult

    ranking = pd.DataFrame(
        [{"variable": "x", "delta_aic": -1.0, "kind": "categorical", "n_obs": 10}]
    )
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=ranking,
        top_summaries=MappingProxyType({}),
        top_slices=(),
        confusion=None,
        residual_pooling=None,
        n_rows=10,
        n_correct=8,
        n_incorrect=2,
        mae=None,
        rmse=None,
    )
    with pytest.raises(ValueError, match="constructed without them"):
        result.plot_confusion()
