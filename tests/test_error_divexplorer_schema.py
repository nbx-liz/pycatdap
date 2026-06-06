"""Tests for the DivExplorer 0.2.x schema output (H-0019, #32).

``to_divexplorer_format(schema="divexplorer")`` emits the real DivExplorer
0.2.x columns (``support / itemset / error / error_div / error_t / length /
support_count``) on both ``SliceDiscoveryResult`` and ``ErrorAnalysisResult``.
``schema="native"`` (the default) keeps the legacy pycatdap-native columns
unchanged.

divexplorer is an **optional** dependency (it pulls scikit-learn / mlxtend /
igraph and is therefore not a pycatdap extra — see HISTORY H-0019 §B). The
cross-test uses ``pytest.importorskip("divexplorer")``; everything else runs
without it.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pytest

import pycatdap
import pycatdap.error

_DIVEXPLORER_COLUMNS = [
    "support",
    "itemset",
    "error",
    "error_div",
    "error_t",
    "length",
    "support_count",
]
_SLICE_NATIVE_COLUMNS = [
    "description",
    "size",
    "error_rate",
    "delta_aic",
    "measure_value",
    "n_error_in_slice",
]


def _make_slice_result(seed: int = 0, n: int = 300):
    """Build a SliceDiscoveryResult where errors concentrate on ``a == x``."""
    rng = np.random.RandomState(seed)
    a = rng.choice(["x", "y"], n)
    b = rng.choice(["p", "q"], n)
    err = ((a == "x") & (rng.rand(n) < 0.7)) | ((a == "y") & (rng.rand(n) < 0.15))
    y_true = np.zeros(n, dtype=int)
    y_pred = err.astype(int)  # error_label == (y_true != y_pred) == err
    df = pd.DataFrame({"a": a, "b": b})
    result = pycatdap.error.discover_error_slices(
        df, y_true, y_pred, max_vars=2, top_k=5
    )
    return df, y_true, y_pred, result


# ---------- native schema is unchanged (backward compat) ----------


def test_native_schema_is_default_and_unchanged() -> None:
    _, _, _, result = _make_slice_result()
    default = result.to_divexplorer_format()
    native = result.to_divexplorer_format(schema="native")
    assert list(default.columns) == _SLICE_NATIVE_COLUMNS
    pd.testing.assert_frame_equal(default, native)


# ---------- new fields on SliceDiscoveryResult ----------


def test_slice_result_stores_n_total_and_base_error_rate() -> None:
    _, _, _, result = _make_slice_result()
    assert result.n_total == 300
    assert 0.0 < result.base_error_rate < 1.0
    d = result.to_dict()
    assert d["n_total"] == 300
    assert "base_error_rate" in d


# ---------- divexplorer schema ----------


def test_divexplorer_schema_columns_and_dtypes() -> None:
    _, _, _, result = _make_slice_result()
    dx = result.to_divexplorer_format(schema="divexplorer")
    assert list(dx.columns) == _DIVEXPLORER_COLUMNS
    assert dx["support"].dtype == np.float64
    assert dx["itemset"].dtype == object
    assert dx["error_div"].dtype == np.float64
    assert dx["length"].dtype == np.int64
    assert dx["support_count"].dtype == np.float64
    assert all(isinstance(it, frozenset) for it in dx["itemset"])


def test_divexplorer_support_length_and_itemset() -> None:
    _, _, _, result = _make_slice_result()
    dx = result.to_divexplorer_format(schema="divexplorer")
    for slice_, row in zip(result.slices, dx.itertuples(index=False), strict=True):
        expected_itemset = frozenset(f"{var}={val}" for var, val in slice_.conditions)
        assert row.itemset == expected_itemset
        assert row.length == len(expected_itemset)
        assert row.support == pytest.approx(slice_.size / result.n_total)
        assert row.support_count == pytest.approx(float(slice_.size))


def test_divexplorer_error_div_uses_overall_rate() -> None:
    _, _, _, result = _make_slice_result()
    dx = result.to_divexplorer_format(schema="divexplorer")
    for slice_, row in zip(result.slices, dx.itertuples(index=False), strict=True):
        assert row.error == pytest.approx(slice_.error_metric)
        assert row.error_div == pytest.approx(
            slice_.error_metric - result.base_error_rate
        )
        assert row.error_t == pytest.approx(slice_.measure_value)


def test_divexplorer_params_override_stored_values() -> None:
    _, _, _, result = _make_slice_result()
    dx = result.to_divexplorer_format(
        schema="divexplorer", n_total=1000, overall_error_rate=0.5
    )
    first = next(iter(result.slices))
    row = dx.iloc[0]
    assert row["support"] == pytest.approx(first.size / 1000)
    assert row["error_div"] == pytest.approx(first.error_metric - 0.5)


def test_divexplorer_missing_n_total_raises() -> None:
    _, _, _, result = _make_slice_result()
    broken = dataclasses.replace(result, n_total=0)
    with pytest.raises(ValueError, match=r"n_total"):
        broken.to_divexplorer_format(schema="divexplorer")


def test_divexplorer_empty_slices_returns_typed_empty_frame() -> None:
    rng = np.random.RandomState(1)
    n = 120
    df = pd.DataFrame({"a": rng.choice(["x", "y"], n), "b": rng.choice(["p", "q"], n)})
    y_true = np.zeros(n, dtype=int)
    y_pred = np.zeros(n, dtype=int)  # zero errors -> no slices
    result = pycatdap.error.discover_error_slices(df, y_true, y_pred, max_vars=2)
    assert result.slices == ()
    dx = result.to_divexplorer_format(schema="divexplorer")
    assert list(dx.columns) == _DIVEXPLORER_COLUMNS
    assert len(dx) == 0
    assert dx["support"].dtype == np.float64
    assert dx["length"].dtype == np.int64


def test_invalid_schema_raises() -> None:
    _, _, _, result = _make_slice_result()
    with pytest.raises(ValueError, match=r"schema"):
        result.to_divexplorer_format(schema="bogus")  # type: ignore[arg-type]


# ---------- ErrorAnalysisResult ----------


def test_error_analysis_divexplorer_schema() -> None:
    df, y_true, y_pred, _ = _make_slice_result()
    result = pycatdap.error_analysis(df, y_true, y_pred, top_k=5)
    dx = result.to_divexplorer_format(schema="divexplorer")
    assert list(dx.columns) == _DIVEXPLORER_COLUMNS
    # native still default + unchanged
    native = result.to_divexplorer_format()
    assert "pearson_residual" in native.columns
    # single-variable cells -> length 1 itemsets, auto n_total from n_rows
    assert len(dx) > 0
    assert (dx["length"] == 1).all()
    assert dx["support_count"].max() <= len(df)


def test_divexplorer_manual_construction_requires_overall_rate() -> None:
    """A result built outside discover_error_slices keeps the sentinel
    base_error_rate=0.0; error_div is only correct when the caller passes
    overall_error_rate explicitly (documents the MEDIUM review finding)."""
    _, _, _, result = _make_slice_result()
    manual = dataclasses.replace(result, base_error_rate=0.0)
    first = next(iter(result.slices))
    # without override: error_div degenerates to the raw rate (sentinel 0.0)
    degenerate = manual.to_divexplorer_format(schema="divexplorer")
    assert degenerate.iloc[0]["error_div"] == pytest.approx(first.error_metric)
    # with override: correct divergence
    corrected = manual.to_divexplorer_format(
        schema="divexplorer", overall_error_rate=result.base_error_rate
    )
    assert corrected.iloc[0]["error_div"] == pytest.approx(
        first.error_metric - result.base_error_rate
    )


# ---------- cross-test vs real DivExplorer 0.2.x (#32 AC) ----------


def test_divexplorer_cross_column_compatible() -> None:
    dx_mod = pytest.importorskip("divexplorer")
    df, y_true, y_pred, result = _make_slice_result()
    pyc = result.to_divexplorer_format(schema="divexplorer")

    # real DivExplorer on the same data with an explicit error outcome
    err = (np.asarray(y_true) != np.asarray(y_pred)).astype(int)
    dxf = df.assign(error=err)
    real = dx_mod.DivergenceExplorer(dxf).get_pattern_divergence(
        min_support=0.05, boolean_outcomes=["error"]
    )

    # column-name compatible (same 7 columns, order-insensitive)
    assert set(pyc.columns) == set(real.columns)
    # the itemsets pycatdap surfaces also appear in DivExplorer's output
    real_itemsets = set(real["itemset"])
    assert any(it in real_itemsets for it in pyc["itemset"])
