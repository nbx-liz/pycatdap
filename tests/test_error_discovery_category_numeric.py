"""Numeric columns shipped as ``category`` dtype must still be AIC-binned.

H-0016 follow-up. ``_is_continuous`` used ``pd.api.types.is_numeric_dtype``,
which is ``False`` for the ``category`` dtype even when its categories are
numeric. A high-cardinality numeric column arriving as ``category`` (common
after ``read_csv(dtype="category")`` or sklearn pipelines) therefore escaped
binning and was treated as a raw categorical — the combinatorial blow-up
behind the 2026-05-30 OOM incident.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from pycatdap.error import discover_error_slices
from pycatdap.error.discovery import _is_continuous, _prepare_frame


def test_is_continuous_true_for_numeric_category() -> None:
    """A category dtype with many numeric categories is continuous."""
    values = np.arange(100, dtype=np.int64)
    s = pd.Series(values).astype("category")
    assert s.dtype.name == "category"
    assert _is_continuous(s) is True


def test_is_continuous_false_for_low_card_numeric_category() -> None:
    """Few distinct numeric categories stay discrete (like plain numeric)."""
    s = pd.Series([0, 1, 2, 0, 1, 2] * 10).astype("category")
    assert _is_continuous(s) is False


def test_is_continuous_false_for_string_category() -> None:
    """High-cardinality *string* categories are genuine categoricals."""
    s = pd.Series([f"v{i}" for i in range(100)]).astype("category")
    assert _is_continuous(s) is False


def test_numeric_category_column_is_binned_in_prepare_frame() -> None:
    """The prepared frame must collapse a numeric-category column to a few
    interval-label bins, not keep ~100 raw codes."""
    n = 400
    rng = np.random.default_rng(0)
    raw = rng.integers(0, 100, size=n)
    df = pd.DataFrame({"x": pd.Series(raw).astype("category")})
    response = np.where(rng.random(n) < 0.3, "incorrect", "correct").astype(object)
    prepared = _prepare_frame(df, ["x"], response)
    # Binned -> far fewer distinct values than the ~100 raw categories.
    assert prepared["x"].nunique() < 50
    # And rendered as interval labels.
    assert any("[" in str(v) or "," in str(v) for v in prepared["x"].dropna().unique())


def test_numeric_category_does_not_explode_search() -> None:
    """Discovery over a numeric-category column behaves like the binned
    numeric case: a small, bounded candidate count (no per-value blow-up)."""
    n = 600
    rng = np.random.default_rng(1)
    df = pd.DataFrame(
        {
            "age": pd.Series(rng.integers(18, 90, size=n)).astype("category"),
            "grp": rng.choice(["a", "b"], size=n).astype(object),
        }
    )
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.3, 1 - yt, yt)
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=30)
    # Binned "age" contributes a handful of interval cells, not ~70 raw codes;
    # level-1 evaluation stays small. Guard against regression to per-value.
    assert result.n_evaluated < 60
    assert result.truncated is False
