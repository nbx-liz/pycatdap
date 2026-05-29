"""Tests for Phase I confusion visualisation + AIC (H-0012 PR-H1).

Covers:

- ``pycatdap.error.confusion_aic`` — sign convention (negative when
  informative), numerical equivalence with the existing ΔAIC path
- ``pycatdap.error.plot_confusion`` — both backends, binary + multiclass,
  all four normalize modes
- ``pycatdap.error.plot_confusion_by_slice`` — small-multiples grid,
  matplotlib returns ``Figure`` (intentional Axes-rule exception per
  H-0012 §F-bis)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap.error import confusion_aic, plot_confusion, plot_confusion_by_slice

# ---------- confusion_aic ----------


def test_confusion_aic_negative_when_informative() -> None:
    """A near-perfect classifier should yield a strongly negative ΔAIC."""
    rng = np.random.default_rng(0)
    y_true = rng.choice([0, 1], size=200)
    y_pred = y_true.copy()
    # 5% noise — still very informative
    flip = rng.random(len(y_true)) < 0.05
    y_pred[flip] = 1 - y_pred[flip]

    delta = confusion_aic(y_true, y_pred)
    assert delta < 0.0, f"expected negative ΔAIC for informative model, got {delta}"


def test_confusion_aic_positive_when_uninformative() -> None:
    """A pure-random predictor should yield a non-negative ΔAIC."""
    rng = np.random.default_rng(1)
    y_true = rng.choice([0, 1], size=400)
    y_pred = rng.choice([0, 1], size=400)
    delta = confusion_aic(y_true, y_pred)
    # Allow up to a tiny negative due to finite-sample noise; the
    # population value should be ~0 / mildly positive.
    assert delta > -2.0, f"expected non-strongly-negative ΔAIC for noise, got {delta}"


def test_confusion_aic_multiclass() -> None:
    """Multiclass case (3 classes) returns a finite float."""
    rng = np.random.default_rng(2)
    y_true = rng.choice(["a", "b", "c"], size=300)
    y_pred = y_true.copy()
    flip = rng.random(len(y_true)) < 0.2
    other = rng.choice(["a", "b", "c"], size=int(flip.sum()))
    y_pred[flip] = other

    delta = confusion_aic(y_true, y_pred)
    assert np.isfinite(delta)
    assert delta < 0.0  # informative


def test_confusion_aic_matches_catdap1() -> None:
    """confusion_aic must equal catdap1(...).delta_aic for the same crosstab."""
    rng = np.random.default_rng(3)
    y_true = rng.choice([0, 1], size=150)
    y_pred = y_true.copy()
    flip = rng.random(150) < 0.15
    y_pred[flip] = 1 - y_pred[flip]

    df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred})
    r = pycatdap.catdap1(df, response_names=["y_true"])
    catdap_delta = float(r.aic.loc["y_true", "y_pred"])
    direct = confusion_aic(y_true, y_pred)
    assert direct == pytest.approx(catdap_delta, rel=1e-9, abs=1e-9)


def test_confusion_aic_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="must have the same length"):
        confusion_aic([0, 1, 0], [0, 1])


def test_confusion_aic_empty_raises() -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        confusion_aic([], [])


# ---------- plot_confusion (matplotlib backend) ----------


@pytest.fixture()
def binary_labels() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(11)
    y_true = rng.choice([0, 1], size=80)
    y_pred = y_true.copy()
    flip = rng.random(80) < 0.2
    y_pred[flip] = 1 - y_pred[flip]
    return y_true, y_pred


@pytest.fixture()
def multiclass_labels() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(12)
    y_true = rng.choice(["a", "b", "c"], size=90)
    y_pred = y_true.copy()
    flip = rng.random(90) < 0.25
    other = rng.choice(["a", "b", "c"], size=int(flip.sum()))
    y_pred[flip] = other
    return y_true, y_pred


def test_plot_confusion_matplotlib_returns_axes(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    y_true, y_pred = binary_labels
    ax = plot_confusion(y_true, y_pred, backend="matplotlib")
    assert isinstance(ax, Axes)
    assert ax.get_xlabel() == "Predicted"
    assert ax.get_ylabel() == "True"


def test_plot_confusion_matplotlib_accepts_existing_ax(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    plt = pytest.importorskip("matplotlib.pyplot")
    y_true, y_pred = binary_labels
    _fig, ax = plt.subplots()
    ret = plot_confusion(y_true, y_pred, backend="matplotlib", ax=ax)
    assert ret is ax


@pytest.mark.parametrize("normalize", ["true", "pred", "all", None])
def test_plot_confusion_matplotlib_all_normalize_modes(
    binary_labels: tuple[np.ndarray, np.ndarray],
    normalize: str | None,
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = binary_labels
    ax = plot_confusion(y_true, y_pred, normalize=normalize, backend="matplotlib")
    assert ax is not None


def test_plot_confusion_matplotlib_unknown_normalize_raises(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = binary_labels
    with pytest.raises(ValueError, match="unknown normalize"):
        plot_confusion(y_true, y_pred, normalize="bogus", backend="matplotlib")


def test_plot_confusion_matplotlib_multiclass(
    multiclass_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = multiclass_labels
    ax = plot_confusion(y_true, y_pred, backend="matplotlib")
    # Tick count should equal class count
    assert len(ax.get_xticks()) == 3


def test_plot_confusion_explicit_label_order(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    y_true, y_pred = binary_labels
    ax = plot_confusion(y_true, y_pred, labels=[1, 0], backend="matplotlib")
    xticklabels = [t.get_text() for t in ax.get_xticklabels()]
    assert xticklabels == ["1", "0"]


# ---------- plot_confusion (plotly backend) ----------


def test_plot_confusion_plotly_returns_figure(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    y_true, y_pred = binary_labels
    fig = plot_confusion(y_true, y_pred, backend="plotly")
    assert isinstance(fig, go.Figure)


def test_plot_confusion_plotly_multiclass(
    multiclass_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    y_true, y_pred = multiclass_labels
    fig = plot_confusion(y_true, y_pred, backend="plotly", normalize="true")
    assert fig.layout.title.text is not None
    assert "normalized" in fig.layout.title.text


# ---------- plot_confusion_by_slice ----------


@pytest.fixture()
def sliced_df() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(31)
    n = 120
    var = rng.choice(["young", "old"], size=n)
    y_true = rng.choice([0, 1], size=n)
    # Errors concentrate on "young"
    noise_rate = np.where(var == "young", 0.4, 0.1)
    flip = rng.random(n) < noise_rate
    y_pred = y_true.copy()
    y_pred[flip] = 1 - y_pred[flip]
    df = pd.DataFrame({"var": var, "extra": rng.normal(size=n)})
    return df, y_true, y_pred


def test_plot_confusion_by_slice_matplotlib_returns_figure(
    sliced_df: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.figure import Figure

    df, y_true, y_pred = sliced_df
    fig = plot_confusion_by_slice(df, y_true, y_pred, "var", backend="matplotlib")
    # F-bis: matplotlib backend returns Figure (NOT Axes) for grid layouts.
    assert isinstance(fig, Figure)


def test_plot_confusion_by_slice_plotly_returns_figure(
    sliced_df: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    df, y_true, y_pred = sliced_df
    fig = plot_confusion_by_slice(df, y_true, y_pred, "var", backend="plotly")
    assert isinstance(fig, go.Figure)


def test_plot_confusion_by_slice_unknown_var_raises(
    sliced_df: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = sliced_df
    with pytest.raises(KeyError, match="not in df.columns"):
        plot_confusion_by_slice(df, y_true, y_pred, "missing", backend="matplotlib")


def test_plot_confusion_by_slice_length_mismatch_raises(
    sliced_df: tuple[pd.DataFrame, np.ndarray, np.ndarray],
) -> None:
    pytest.importorskip("matplotlib")
    df, y_true, y_pred = sliced_df
    with pytest.raises(ValueError, match="must equal len"):
        plot_confusion_by_slice(
            df, y_true[:10], y_pred[:10], "var", backend="matplotlib"
        )


def test_plot_confusion_by_slice_all_na_raises() -> None:
    pytest.importorskip("matplotlib")
    df = pd.DataFrame({"var": [None, None, None]})
    with pytest.raises(ValueError, match="no non-NA categories"):
        plot_confusion_by_slice(
            df,
            np.array([0, 1, 0]),
            np.array([0, 1, 1]),
            "var",
            backend="matplotlib",
        )


# ---------- backend dispatch ----------


def test_plot_confusion_unknown_backend_raises(
    binary_labels: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_pred = binary_labels
    with pytest.raises(ValueError, match="Unknown plot backend"):
        plot_confusion(y_true, y_pred, backend="ggplot")  # type: ignore[arg-type]


def test_phase_i_exports_from_pycatdap_error() -> None:
    assert hasattr(pycatdap.error, "confusion_aic")
    assert hasattr(pycatdap.error, "plot_confusion")
    assert hasattr(pycatdap.error, "plot_confusion_by_slice")
