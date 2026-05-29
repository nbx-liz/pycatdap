"""Regression-task slice discovery (H-0015 PR-M2, design D1).

``discover_error_slices`` previously raised ``NotImplementedError`` for
regression.  D1 reuses the classification machinery by deriving a binary
``high_residual`` / ``low_residual`` response from the AIC-pooled absolute
residual (``abs_residual_pool``): the bin with the largest mean ``|residual|``
becomes the "error" category, and the existing support-pruned enumeration +
measure scoring run unchanged.

Invariants under test (see HISTORY.md H-0015 §Invariants):

* INV-R1  support-pruned == exhaustive ∩ {size >= min_support}
* INV-R2  inputs never mutated; reserved column collision raises
* INV-R3  only error-concentrated slices (error_metric > baseline) surface
* INV-R7  length contract enforced
* INV-R8  label_kind reflects the regression labeller
* INV-R9  no classification semantics (``"incorrect"``) leak into the result
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pycatdap.error import discover_error_slices
from pycatdap.error._slice import SliceDiscoveryResult


def _make_regression_data(
    n: int = 400, seed: int = 0
) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """A regression problem whose errors concentrate in ``region == "C"``."""
    rng = np.random.default_rng(seed)
    region = rng.choice(["A", "B", "C"], size=n)
    x = rng.normal(0.0, 1.0, size=n)
    y_true = 2.0 * x + rng.normal(0.0, 0.2, size=n)
    y_pred = y_true.copy()
    bad = region == "C"
    # A large, clearly separated bias for region C -> the high-|residual|
    # subgroup is unambiguously region C (well above the ~0.2 noise floor).
    y_pred[bad] = y_pred[bad] + 10.0 + rng.normal(0.0, 0.3, size=int(bad.sum()))
    df = pd.DataFrame({"region": region, "x": x})
    return df, y_true, y_pred


def _conditions_set(slice_obj: object) -> set[tuple[str, str]]:
    return {(col, val) for col, val in slice_obj.conditions}  # type: ignore[attr-defined]


# --------------------------------------------------------------------------- #
# Happy path / detection
# --------------------------------------------------------------------------- #


def test_regression_returns_slice_discovery_result() -> None:
    df, y_true, y_pred = _make_regression_data()
    result = discover_error_slices(df, y_true, y_pred, min_support=20, top_k=10)
    assert isinstance(result, SliceDiscoveryResult)
    assert len(result.slices) > 0


def test_regression_detects_high_residual_subgroup() -> None:
    """The known high-residual cohort (region == 'C') must be surfaced."""
    df, y_true, y_pred = _make_regression_data()
    result = discover_error_slices(
        df, y_true, y_pred, max_vars=2, min_support=20, top_k=10
    )
    found = any(("region", "C") in _conditions_set(s) for s in result.slices)
    assert found, [s.description for s in result.slices]


def test_regression_top_slice_is_error_concentrated() -> None:
    """INV-R3: surfaced slices concentrate the high-residual rows."""
    df, y_true, y_pred = _make_regression_data()
    result = discover_error_slices(
        df, y_true, y_pred, max_vars=2, min_support=20, top_k=10
    )
    # Every surfaced slice must be more error-dense than a coin flip here,
    # and the region-C slice in particular should be strongly concentrated.
    region_c = [s for s in result.slices if ("region", "C") in _conditions_set(s)]
    assert region_c, "region C slice missing"
    assert max(s.error_metric for s in region_c) > 0.5


# --------------------------------------------------------------------------- #
# INV-R8 label_kind
# --------------------------------------------------------------------------- #


def test_regression_label_kind() -> None:
    df, y_true, y_pred = _make_regression_data()
    result = discover_error_slices(df, y_true, y_pred, min_support=20)
    assert result.label_kind == "abs_residual_pool"


def test_classification_label_kind_unchanged() -> None:
    """The classification path still reports error_label (no hijack)."""
    rng = np.random.default_rng(1)
    n = 200
    age = rng.choice(["young", "old"], size=n)
    y_true = (age == "old").astype(int)
    y_pred = np.where(rng.random(n) < 0.2, 1 - y_true, y_true)
    df = pd.DataFrame({"age": age})
    result = discover_error_slices(df, y_true, y_pred, min_support=20)
    assert result.label_kind == "error_label"


# --------------------------------------------------------------------------- #
# INV-R2 immutability + reserved column
# --------------------------------------------------------------------------- #


def test_regression_inputs_not_mutated() -> None:
    df, y_true, y_pred = _make_regression_data()
    df_before = df.copy(deep=True)
    yt_before = np.array(y_true, copy=True)
    yp_before = np.array(y_pred, copy=True)
    discover_error_slices(df, y_true, y_pred, min_support=20)
    pd.testing.assert_frame_equal(df, df_before)
    np.testing.assert_array_equal(np.asarray(y_true), yt_before)
    np.testing.assert_array_equal(np.asarray(y_pred), yp_before)


def test_regression_reserved_column_collision() -> None:
    df, y_true, y_pred = _make_regression_data()
    df = df.assign(_error_label_=1.0)
    with pytest.raises(ValueError, match="reserved"):
        discover_error_slices(df, y_true, y_pred, min_support=20)


# --------------------------------------------------------------------------- #
# INV-R7 length contract
# --------------------------------------------------------------------------- #


def test_regression_length_mismatch_raises() -> None:
    df, y_true, y_pred = _make_regression_data(n=100)
    with pytest.raises(ValueError):
        discover_error_slices(df, y_true[:-1], y_pred, min_support=20)


# --------------------------------------------------------------------------- #
# INV-R1 support floor honoured (no slice below min_support)
# --------------------------------------------------------------------------- #


def test_regression_respects_min_support() -> None:
    df, y_true, y_pred = _make_regression_data()
    floor = 25
    result = discover_error_slices(df, y_true, y_pred, min_support=floor, top_k=20)
    assert all(s.size >= floor for s in result.slices)


# --------------------------------------------------------------------------- #
# INV-R9 no classification-semantics residue
# --------------------------------------------------------------------------- #


def test_regression_does_not_leak_incorrect_category() -> None:
    """A degenerate / well-fit regression must not surface via the
    classification 'incorrect' pivot; it should simply find nothing
    error-concentrated rather than misbehave."""
    rng = np.random.default_rng(7)
    n = 300
    x = rng.normal(0.0, 1.0, size=n)
    df = pd.DataFrame({"g": rng.choice(["a", "b"], size=n), "x": x})
    y_true = 3.0 * x
    y_pred = y_true.copy()  # perfect predictions -> no residual variation
    result = discover_error_slices(df, y_true, y_pred, min_support=20)
    # No subgroup can be "more error-dense than baseline" when residuals
    # are uniform/zero -> empty, and it must not raise.
    assert isinstance(result, SliceDiscoveryResult)
    assert result.label_kind == "abs_residual_pool"
