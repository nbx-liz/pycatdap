"""Regression + multi-class OvR calibration (H-0014 PR-L5).

The binary calibration suite (tests/test_error_calibration.py) must keep
passing UNCHANGED — that is the regression guard that the binary path was
not touched. These tests cover only the new functions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest

from pycatdap.error import (
    calibration_table,
    expected_calibration_error,
    multiclass_calibration_table,
    multiclass_expected_calibration_error,
    regression_calibration_error,
    regression_calibration_table,
)

# ---------------------------------------------------------------------------
# Regression calibration
# ---------------------------------------------------------------------------


def test_regression_table_columns_and_rows() -> None:
    rng = np.random.default_rng(0)
    y_pred = rng.uniform(0, 100, size=500)
    y_true = y_pred + rng.normal(0, 5, size=500)
    table = regression_calibration_table(y_true, y_pred, n_quantiles=5)
    assert list(table.columns) == [
        "bin_low",
        "bin_high",
        "n",
        "pred_mean",
        "actual_mean",
        "ci_low",
        "ci_high",
    ]
    assert len(table) <= 5
    assert table["n"].sum() == 500
    # bins ordered ascending by bin_low
    assert table["bin_low"].is_monotonic_increasing


def test_regression_perfectly_calibrated_low_error() -> None:
    # y_true == y_pred exactly → pred_mean == actual_mean per bin → error ~0
    y_pred = np.linspace(0, 100, 500)
    y_true = y_pred.copy()
    err = regression_calibration_error(y_true, y_pred, n_quantiles=10)
    assert err == pytest.approx(0.0, abs=1e-9)


def test_regression_biased_predictions_positive_error() -> None:
    y_pred = np.linspace(0, 100, 500)
    y_true = y_pred + 20.0  # constant under-prediction
    err = regression_calibration_error(y_true, y_pred, n_quantiles=10)
    assert err == pytest.approx(20.0, abs=1e-6)


def test_regression_ci_present_and_bracketing() -> None:
    rng = np.random.default_rng(1)
    y_pred = rng.uniform(0, 10, size=400)
    y_true = y_pred + rng.normal(0, 2, size=400)
    table = regression_calibration_table(y_true, y_pred, n_quantiles=4)
    assert (table["ci_low"] <= table["actual_mean"]).all()
    assert (table["actual_mean"] <= table["ci_high"]).all()


def test_regression_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="same length"):
        regression_calibration_table([1.0, 2.0, 3.0], [1.0, 2.0])


def test_regression_all_nan_raises() -> None:
    with pytest.raises(ValueError, match="finite"):
        regression_calibration_table([np.nan, np.nan], [np.nan, np.nan])


def test_regression_invalid_n_quantiles_raises() -> None:
    with pytest.raises(ValueError, match="n_quantiles"):
        regression_calibration_table([1.0, 2.0], [1.0, 2.0], n_quantiles=0)


def test_regression_constant_predictions_collapse() -> None:
    # near-constant predictions collapse to a single band without error
    y_pred = np.full(100, 5.0)
    y_true = np.full(100, 7.0)
    table = regression_calibration_table(y_true, y_pred, n_quantiles=10)
    assert len(table) == 1
    assert table.iloc[0]["pred_mean"] == pytest.approx(5.0)
    assert table.iloc[0]["actual_mean"] == pytest.approx(7.0)


def test_regression_n_quantiles_one() -> None:
    table = regression_calibration_table(
        [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], n_quantiles=1
    )
    assert len(table) == 1
    assert table.iloc[0]["n"] == 3


def test_regression_pandas_series_input() -> None:
    s_pred = pd.Series(np.linspace(0, 1, 50))
    s_true = pd.Series(np.linspace(0, 1, 50))
    err = regression_calibration_error(s_true, s_pred, n_quantiles=5)
    assert err == pytest.approx(0.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Multi-class one-vs-rest calibration
# ---------------------------------------------------------------------------


def _multiclass_data(
    seed: int = 0, n: int = 600, k: int = 3
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    proba = rng.dirichlet(np.ones(k), size=n)
    y_true = np.array([rng.choice(k, p=row) for row in proba])
    return y_true, proba


def test_multiclass_table_one_per_class() -> None:
    yt, proba = _multiclass_data(k=3)
    tables = multiclass_calibration_table(yt, proba, strategy="equal_width", n_bins=5)
    assert set(tables.keys()) == {0, 1, 2}
    for tbl in tables.values():
        assert "prob_pred" in tbl.columns
        assert "prob_true" in tbl.columns


def test_multiclass_two_class_equals_binary() -> None:
    """OvR on a 2-class problem reduces exactly to the binary table."""
    rng = np.random.default_rng(2)
    n = 400
    p1 = rng.uniform(0, 1, size=n)
    proba = np.column_stack([1 - p1, p1])
    yt = (rng.uniform(0, 1, size=n) < p1).astype(int)

    multi = multiclass_calibration_table(yt, proba, strategy="equal_width", n_bins=8)
    binary = calibration_table(
        (yt == 1).astype(int), p1, strategy="equal_width", n_bins=8
    )
    pdt.assert_frame_equal(
        multi[1].reset_index(drop=True), binary.reset_index(drop=True)
    )


def test_multiclass_ece_macro_average() -> None:
    yt, proba = _multiclass_data(k=3)
    macro = multiclass_expected_calibration_error(
        yt, proba, strategy="equal_width", n_bins=5
    )
    per_class = [
        expected_calibration_error(
            (yt == c).astype(int), proba[:, c], strategy="equal_width", n_bins=5
        )
        for c in range(3)
    ]
    assert macro == pytest.approx(float(np.mean(per_class)))


def test_multiclass_explicit_classes() -> None:
    yt = np.array(["cat", "dog", "cat", "bird"])
    proba = np.array(
        [
            [0.7, 0.2, 0.1],
            [0.1, 0.8, 0.1],
            [0.6, 0.3, 0.1],
            [0.2, 0.1, 0.7],
        ]
    )
    tables = multiclass_calibration_table(
        yt, proba, classes=["cat", "dog", "bird"], strategy="equal_width", n_bins=3
    )
    assert set(tables.keys()) == {"cat", "dog", "bird"}


def test_multiclass_non_2d_proba_raises() -> None:
    yt = np.array([0, 1, 2])
    with pytest.raises(ValueError, match="2D"):
        multiclass_calibration_table(yt, np.array([0.1, 0.2, 0.3]))


def test_multiclass_length_mismatch_raises() -> None:
    yt = np.array([0, 1, 2])
    proba = np.array([[0.5, 0.5], [0.5, 0.5]])  # 2 rows vs 3 labels
    with pytest.raises(ValueError, match="same length"):
        multiclass_calibration_table(yt, proba)


def test_multiclass_class_count_mismatch_raises() -> None:
    yt = np.array([0, 1, 2, 0])
    proba = np.array(
        [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]]
    )  # 2 cols, 3 classes
    with pytest.raises(ValueError, match="number of classes"):
        multiclass_calibration_table(yt, proba)


def test_multiclass_table_is_readonly_mapping() -> None:
    from types import MappingProxyType

    yt, proba = _multiclass_data(k=3)
    tables = multiclass_calibration_table(yt, proba, strategy="equal_width", n_bins=5)
    assert isinstance(tables, MappingProxyType)


def test_binary_calibration_unchanged_smoke() -> None:
    """The binary path still works exactly as before (regression guard)."""
    rng = np.random.default_rng(3)
    yt = rng.integers(0, 2, size=300)
    yp = rng.uniform(0, 1, size=300)
    table = calibration_table(yt, yp, strategy="equal_width", n_bins=10)
    assert "prob_true" in table.columns
    ece = expected_calibration_error(yt, yp, strategy="equal_width", n_bins=10)
    assert 0.0 <= ece <= 1.0
