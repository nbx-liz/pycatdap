"""Tests for D5 fetch loaders (H-0017, #25).

Three sklearn-backed UCI fetchers added for slice-discovery / fully
categorical CATDAP demos:

- ``fetch_wine_quality`` — UCI red+white combined (6,497 rows), ``color``
  column distinguishes the two sources; ``quality`` is the target.
- ``fetch_bank_marketing`` — UCI bank marketing (45,211 rows); the
  generic OpenML ``V1..V16`` columns are renamed to the UCI names.
- ``fetch_mushroom`` — UCI mushroom (8,124 rows), all categorical;
  ``class`` is the target.

All fetchers raise :class:`ImportError` when ``scikit-learn`` is not
installed (that test runs in any environment). The network-bound tests
use ``pytest.importorskip("sklearn")`` and the ``@pytest.mark.slow``
marker so they are excluded from default CI (see
``feedback_make_ci_d4_network_hang``).
"""

from __future__ import annotations

import sys
from unittest import mock

import pandas as pd
import pytest

import pycatdap

_D5_LOADERS = ["fetch_wine_quality", "fetch_bank_marketing", "fetch_mushroom"]


# ---------- ImportError fallback (runs without sklearn) ----------


@pytest.mark.parametrize("loader_name", _D5_LOADERS)
def test_d5_fetchers_raise_importerror_without_sklearn(loader_name: str) -> None:
    """Each loader must surface a clear ImportError pointing at the
    ``pycatdap[data]`` extras when scikit-learn is unimportable."""
    loader = getattr(pycatdap.datasets, loader_name)
    with (
        mock.patch.dict(sys.modules, {"sklearn": None, "sklearn.datasets": None}),
        pytest.raises(ImportError, match=r"pycatdap\[data\]"),
    ):
        loader()


# ---------- exports ----------


def test_d5_loaders_exposed_on_datasets_module() -> None:
    for name in _D5_LOADERS:
        assert hasattr(pycatdap.datasets, name)


# ---------- network-bound smoke tests (slow + sklearn) ----------


@pytest.mark.slow
def test_fetch_wine_quality_returns_combined_frame() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_wine_quality()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6_497  # red (1,599) + white (4,898)
    assert "quality" in df.columns
    assert "color" in df.columns
    assert set(df["color"].unique()) == {"red", "white"}


@pytest.mark.slow
def test_fetch_bank_marketing_has_interpretable_columns() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_bank_marketing()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 45_211
    # interpretable UCI names, not the generic OpenML V1..V16
    assert "age" in df.columns
    assert "job" in df.columns
    assert "y" in df.columns
    assert not any(str(c).startswith("V") and str(c)[1:].isdigit() for c in df.columns)


@pytest.mark.slow
def test_fetch_mushroom_is_fully_categorical() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_mushroom()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 8_124
    assert "class" in df.columns
    # every column is categorical / object (no numeric features)
    assert not any(pd.api.types.is_numeric_dtype(df[c]) for c in df.columns)


@pytest.mark.slow
def test_fetch_mushroom_works_with_catdap2() -> None:
    """End-to-end smoke: fully categorical dataset -> catdap2 search."""
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_mushroom()
    result = pycatdap.catdap2(df, response_name="class", nvar=2)
    assert result is not None
