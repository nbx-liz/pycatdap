"""Tests for Phase K calibration (H-0013 PR-K1).

Covers:

- metrics: ``brier_score`` / ``expected_calibration_error`` /
  ``maximum_calibration_error`` (hand-computed values + inline reference parity)
- ``calibration_table`` — structure, ordering, Wilson CI, empty-bin handling
- AIC binning — non-degenerate on a strong signal, bounded initial grid
  (H-0013 §B-bis), graceful on degenerate (all-equal) probabilities
- ``calibration_curve`` — both backends, all three strategies
- validation — binary-only, probability range, length, empty
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pycatdap.error import (
    brier_score,
    calibration_curve,
    calibration_table,
    expected_calibration_error,
    maximum_calibration_error,
)
from pycatdap.error.calibration import _AIC_INIT_BINS, _wilson_interval

# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def binary_proba() -> tuple[np.ndarray, np.ndarray]:
    """Mildly miscalibrated binary predictions."""
    rng = np.random.default_rng(11)
    y_proba = rng.uniform(0.0, 1.0, size=200)
    # over-confident: true rate is a shrunk version of the stated proba
    true_rate = 0.2 + 0.6 * y_proba
    y_true = (rng.random(200) < true_rate).astype(int)
    return y_true, y_proba


@pytest.fixture()
def strong_signal() -> tuple[np.ndarray, np.ndarray]:
    """Sharp transition at 0.5 → AIC must keep >= 2 bins."""
    rng = np.random.default_rng(7)
    y_proba = rng.uniform(0.0, 1.0, size=300)
    y_true = (y_proba >= 0.5).astype(int)
    flip = rng.random(300) < 0.05
    y_true[flip] = 1 - y_true[flip]
    return y_true, y_proba


# ---------------------------------------------------------------------------
# brier_score
# ---------------------------------------------------------------------------


def test_brier_score_hand_value() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, 0.4, 0.6, 0.9])
    # (0.01 + 0.16 + 0.16 + 0.01) / 4 = 0.085
    assert brier_score(y_true, y_proba) == pytest.approx(0.085, abs=1e-12)


def test_brier_score_perfect_is_zero() -> None:
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([0.0, 1.0, 0.0, 1.0])
    assert brier_score(y_true, y_proba) == pytest.approx(0.0, abs=1e-12)


def test_brier_score_accepts_bool_labels() -> None:
    y_true = np.array([False, False, True, True])
    y_proba = np.array([0.1, 0.4, 0.6, 0.9])
    assert brier_score(y_true, y_proba) == pytest.approx(0.085, abs=1e-12)


# ---------------------------------------------------------------------------
# expected / maximum calibration error
# ---------------------------------------------------------------------------


def test_ece_mce_hand_value_equal_width() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, 0.4, 0.6, 0.9])
    # 2 equal-width bins: [0,0.5) -> {0.1,0.4} (true 0,0), [0.5,1] -> {0.6,0.9}
    # bin0: pred 0.25 true 0.0 gap 0.25; bin1: pred 0.75 true 1.0 gap 0.25
    ece = expected_calibration_error(y_true, y_proba, strategy="equal_width", n_bins=2)
    mce = maximum_calibration_error(y_true, y_proba, strategy="equal_width", n_bins=2)
    assert ece == pytest.approx(0.25, abs=1e-12)
    assert mce == pytest.approx(0.25, abs=1e-12)


def _ref_ece_equal_width(y_true: np.ndarray, y_proba: np.ndarray, n_bins: int) -> float:
    """Independent reference ECE under equal-width binning over [0, 1]."""
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    codes = np.clip(np.digitize(y_proba, edges[1:-1]), 0, n_bins - 1)
    n = len(y_true)
    ece = 0.0
    for b in np.unique(codes):
        m = codes == b
        nb = int(m.sum())
        gap = abs(float(y_true[m].mean()) - float(y_proba[m].mean()))
        ece += (nb / n) * gap
    return ece


def test_ece_matches_inline_reference(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = binary_proba
    got = expected_calibration_error(y_true, y_proba, strategy="equal_width", n_bins=10)
    ref = _ref_ece_equal_width(y_true, y_proba, 10)
    assert got == pytest.approx(ref, abs=1e-9)


def test_mce_ge_ece(binary_proba: tuple[np.ndarray, np.ndarray]) -> None:
    y_true, y_proba = binary_proba
    for strategy in ("aic", "equal_width", "quantile"):
        ece = expected_calibration_error(y_true, y_proba, strategy=strategy)
        mce = maximum_calibration_error(y_true, y_proba, strategy=strategy)
        assert mce >= ece - 1e-12, f"MCE < ECE for strategy={strategy}"


def test_ece_near_zero_when_calibrated() -> None:
    rng = np.random.default_rng(3)
    # y_proba == true positive rate → well calibrated
    y_proba = rng.uniform(0.0, 1.0, size=5000)
    y_true = (rng.random(5000) < y_proba).astype(int)
    ece = expected_calibration_error(y_true, y_proba, strategy="equal_width", n_bins=10)
    assert ece < 0.05


# ---------------------------------------------------------------------------
# calibration_table
# ---------------------------------------------------------------------------


def test_calibration_table_columns_and_order(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = binary_proba
    table = calibration_table(y_true, y_proba, strategy="equal_width", n_bins=10)
    assert list(table.columns) == [
        "bin_low",
        "bin_high",
        "n",
        "prob_pred",
        "prob_true",
        "ci_low",
        "ci_high",
    ]
    # rows ordered by bin_low ascending
    assert table["bin_low"].is_monotonic_increasing
    # counts sum to the (finite) sample size
    assert int(table["n"].sum()) == int(np.isfinite(y_proba).sum())


def test_calibration_table_ci_brackets_prob_true(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = binary_proba
    table = calibration_table(y_true, y_proba, strategy="equal_width", n_bins=8)
    assert (table["ci_low"] <= table["prob_true"] + 1e-9).all()
    assert (table["prob_true"] <= table["ci_high"] + 1e-9).all()
    assert (table["ci_low"] >= 0.0).all()
    assert (table["ci_high"] <= 1.0).all()


@pytest.mark.parametrize("strategy", ["aic", "equal_width", "quantile"])
def test_calibration_table_all_strategies(
    binary_proba: tuple[np.ndarray, np.ndarray], strategy: str
) -> None:
    y_true, y_proba = binary_proba
    table = calibration_table(y_true, y_proba, strategy=strategy, n_bins=10)
    assert not table.empty
    assert int(table["n"].sum()) == int(np.isfinite(y_proba).sum())


# ---------------------------------------------------------------------------
# AIC binning behaviour (H-0013 §B-bis)
# ---------------------------------------------------------------------------


def test_aic_binning_non_degenerate(
    strong_signal: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = strong_signal
    table = calibration_table(y_true, y_proba, strategy="aic")
    assert len(table) >= 2, "AIC should keep multiple bins on a strong signal"


def test_aic_binning_bounded_initial_grid(
    strong_signal: tuple[np.ndarray, np.ndarray],
) -> None:
    """Regression guard for the §B-bis safeguard: 300 continuous probabilities
    would explode the initial grid to thousands of bins under ``_auto_accuracy``
    (smallest-gap ~1e-4); the explicit ``accuracy=1/_AIC_INIT_BINS`` caps the
    initial grid, so the final (merged) bin count can never exceed it."""
    y_true, y_proba = strong_signal
    table = calibration_table(y_true, y_proba, strategy="aic")
    assert len(table) <= _AIC_INIT_BINS


def test_aic_binning_degenerate_all_equal() -> None:
    """All-equal probabilities collapse to a single bin without crashing."""
    y_true = np.array([0, 1, 0, 1, 1, 0])
    y_proba = np.full(6, 0.5)
    table = calibration_table(y_true, y_proba, strategy="aic")
    assert len(table) == 1
    assert table.loc[0, "prob_pred"] == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# Wilson interval
# ---------------------------------------------------------------------------


def test_wilson_interval_contains_phat() -> None:
    k = np.array([0.0, 5.0, 10.0])
    n = np.array([10.0, 10.0, 10.0])
    low, high = _wilson_interval(k, n)
    p = k / n
    assert (low <= p + 1e-12).all()
    assert (p <= high + 1e-12).all()
    # stays inside [0, 1] even at the boundaries
    assert (low >= 0.0).all() and (high <= 1.0).all()


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------


def test_non_binary_y_true_raises() -> None:
    with pytest.raises(ValueError, match="binary-only"):
        brier_score(np.array([0, 1, 2]), np.array([0.1, 0.5, 0.9]))


def test_proba_out_of_range_raises() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        brier_score(np.array([0, 1]), np.array([0.5, 1.5]))


def test_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="same length"):
        calibration_table(np.array([0, 1, 0]), np.array([0.1, 0.9]))


def test_empty_raises() -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        brier_score(np.array([]), np.array([]))


def test_unknown_strategy_raises(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = binary_proba
    with pytest.raises(ValueError, match="unknown strategy"):
        calibration_table(y_true, y_proba, strategy="bogus")  # type: ignore[arg-type]


def test_non_finite_proba_masked() -> None:
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, np.nan, 0.6, 0.9])
    # NaN row dropped → Brier over the 3 finite rows
    expected = float(np.mean((np.array([0.1, 0.6, 0.9]) - np.array([0, 1, 1])) ** 2))
    assert brier_score(y_true, y_proba) == pytest.approx(expected, abs=1e-12)


# ---------------------------------------------------------------------------
# calibration_curve — matplotlib backend
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("strategy", ["aic", "equal_width", "quantile"])
def test_calibration_curve_matplotlib_returns_axes(
    binary_proba: tuple[np.ndarray, np.ndarray], strategy: str
) -> None:
    pytest.importorskip("matplotlib")
    from matplotlib.axes import Axes

    y_true, y_proba = binary_proba
    ax = calibration_curve(y_true, y_proba, strategy=strategy, backend="matplotlib")
    assert isinstance(ax, Axes)
    assert ax.get_xlabel() == "Mean predicted probability"
    assert ax.get_ylabel() == "Observed frequency"


def test_calibration_curve_matplotlib_accepts_existing_ax(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    plt = pytest.importorskip("matplotlib.pyplot")
    y_true, y_proba = binary_proba
    _fig, ax = plt.subplots()
    ret = calibration_curve(y_true, y_proba, backend="matplotlib", ax=ax)
    assert ret is ax


def test_calibration_curve_matplotlib_kwargs_override(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    """Caller kwargs override the errorbar defaults instead of colliding."""
    pytest.importorskip("matplotlib")
    y_true, y_proba = binary_proba
    # Would raise TypeError (multiple values for 'color'/'label') if the
    # defaults collided with **kwargs instead of merging.
    ax = calibration_curve(
        y_true, y_proba, backend="matplotlib", color="red", label="custom"
    )
    assert ax is not None


# ---------------------------------------------------------------------------
# calibration_curve — plotly backend
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("strategy", ["aic", "equal_width", "quantile"])
def test_calibration_curve_plotly_returns_figure(
    binary_proba: tuple[np.ndarray, np.ndarray], strategy: str
) -> None:
    pytest.importorskip("plotly")
    import plotly.graph_objects as go

    y_true, y_proba = binary_proba
    fig = calibration_curve(y_true, y_proba, strategy=strategy, backend="plotly")
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text is not None
    assert strategy in fig.layout.title.text


def test_calibration_curve_unknown_backend_raises(
    binary_proba: tuple[np.ndarray, np.ndarray],
) -> None:
    y_true, y_proba = binary_proba
    with pytest.raises(ValueError, match="Unknown plot backend"):
        calibration_curve(y_true, y_proba, backend="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# PR-K5 hardening: metric<->table single-source-of-truth (H1)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("strategy", ["aic", "equal_width", "quantile"])
def test_ece_mce_match_table_recomputation(
    binary_proba: tuple[np.ndarray, np.ndarray], strategy: str
) -> None:
    """ECE/MCE must equal a recomputation from calibration_table — the core
    single-source-of-truth invariant of the whole feature."""
    y_true, y_proba = binary_proba
    table = calibration_table(y_true, y_proba, strategy=strategy, n_bins=10)
    n_total = table["n"].sum()
    gaps = (table["prob_true"] - table["prob_pred"]).abs()
    ref_ece = float((table["n"] / n_total * gaps).sum())
    ref_mce = float(gaps.max())

    got_ece = expected_calibration_error(y_true, y_proba, strategy=strategy, n_bins=10)
    got_mce = maximum_calibration_error(y_true, y_proba, strategy=strategy, n_bins=10)
    assert got_ece == pytest.approx(ref_ece, abs=1e-12)
    assert got_mce == pytest.approx(ref_mce, abs=1e-12)


# ---------------------------------------------------------------------------
# PR-K5 hardening: uncovered error paths (H2)
# ---------------------------------------------------------------------------


def test_all_nonfinite_proba_raises() -> None:
    with pytest.raises(ValueError, match="at least one finite"):
        brier_score(np.array([0, 1]), np.array([np.nan, np.nan]))


@pytest.mark.parametrize("n_bins", [0, -1])
def test_n_bins_below_one_raises(
    binary_proba: tuple[np.ndarray, np.ndarray], n_bins: int
) -> None:
    y_true, y_proba = binary_proba
    with pytest.raises(ValueError, match="n_bins must be >= 1"):
        calibration_table(y_true, y_proba, strategy="equal_width", n_bins=n_bins)


def test_y_true_nan_rows_dropped() -> None:
    """A NaN in y_true drops that row (like a NaN y_proba) instead of raising
    a confusing 'classes [0.0, 1.0, nan]' binary error."""
    y_true = np.array([0.0, np.nan, 1.0, 1.0])
    y_proba = np.array([0.1, 0.5, 0.6, 0.9])
    # finite rows: (0,0.1) (1,0.6) (1,0.9) -> Brier over those three
    expected = float(np.mean((np.array([0.1, 0.6, 0.9]) - np.array([0, 1, 1])) ** 2))
    assert brier_score(y_true, y_proba) == pytest.approx(expected, abs=1e-12)


# ---------------------------------------------------------------------------
# PR-K5 hardening: AIC value correctness (H3) + degenerate edges (M4) + M6
# ---------------------------------------------------------------------------


def test_aic_table_hand_value_two_groups() -> None:
    """Two well-separated probability groups with distinct positive rates must
    yield exactly two AIC bins with the expected per-bin values."""
    y_proba = np.concatenate([np.full(50, 0.1), np.full(50, 0.9)])
    # group@0.1 -> 15/50 positive (0.3); group@0.9 -> 35/50 positive (0.7)
    y_true = np.concatenate(
        [
            np.array([1] * 15 + [0] * 35),
            np.array([1] * 35 + [0] * 15),
        ]
    )
    table = calibration_table(y_true, y_proba, strategy="aic")
    assert len(table) == 2
    assert table["prob_pred"].tolist() == pytest.approx([0.1, 0.9])
    assert table["prob_true"].tolist() == pytest.approx([0.3, 0.7])
    # ECE = 0.5*|0.3-0.1| + 0.5*|0.7-0.9| = 0.2
    ece = expected_calibration_error(y_true, y_proba, strategy="aic")
    assert ece == pytest.approx(0.2, abs=1e-12)


@pytest.mark.parametrize("strategy", ["equal_width", "quantile"])
def test_degenerate_all_equal_non_aic(strategy: str) -> None:
    """All-equal probabilities collapse to a single bin for equal_width and
    quantile too (quantile exercises the edges.size < 2 fallback)."""
    y_true = np.array([0, 1, 0, 1, 1, 0])
    y_proba = np.full(6, 0.5)
    table = calibration_table(y_true, y_proba, strategy=strategy, n_bins=10)
    assert len(table) == 1
    assert table.loc[0, "prob_pred"] == pytest.approx(0.5)
    assert table.loc[0, "prob_true"] == pytest.approx(0.5)  # 3/6 positive


def test_aic_single_bin_metrics_and_ci() -> None:
    """Single-bin (all-equal) AIC table: prob_true, CI bounds, and MCE."""
    y_true = np.array([0, 1, 0, 1, 1, 0])
    y_proba = np.full(6, 0.5)
    table = calibration_table(y_true, y_proba, strategy="aic")
    assert len(table) == 1
    assert table.loc[0, "prob_true"] == pytest.approx(0.5)
    assert 0.0 <= table.loc[0, "ci_low"] <= 0.5 <= table.loc[0, "ci_high"] <= 1.0
    # pred == true == 0.5 -> zero gap
    assert maximum_calibration_error(y_true, y_proba, strategy="aic") == pytest.approx(
        0.0, abs=1e-12
    )


# ---------------------------------------------------------------------------
# PR-K5 hardening: Wilson boundary (M5) + pd.Series input (L8)
# ---------------------------------------------------------------------------


def test_wilson_interval_n_equals_one() -> None:
    """Single-observation bins (the AIC fine-bin / small-sample stressor)."""
    k = np.array([0.0, 1.0])  # p = 0 and p = 1 at n = 1
    n = np.array([1.0, 1.0])
    low, high = _wilson_interval(k, n)
    p = k / n
    assert (low >= 0.0).all() and (high <= 1.0).all()
    assert (low <= p + 1e-12).all() and (p <= high + 1e-12).all()
    assert np.isfinite(low).all() and np.isfinite(high).all()


def test_equal_width_single_bin() -> None:
    y_true = np.array([0, 1, 1, 0])
    y_proba = np.array([0.2, 0.4, 0.6, 0.8])
    table = calibration_table(y_true, y_proba, strategy="equal_width", n_bins=1)
    assert len(table) == 1
    assert int(table["n"].sum()) == 4


def test_accepts_pandas_series() -> None:
    """y_true / y_proba may be pandas Series (declared in the contract)."""
    y_true = pd.Series([0, 0, 1, 1])
    y_proba = pd.Series([0.1, 0.4, 0.6, 0.9])
    assert brier_score(y_true, y_proba) == pytest.approx(0.085, abs=1e-12)
    table = calibration_table(y_true, y_proba, strategy="equal_width", n_bins=2)
    assert int(table["n"].sum()) == 4
