"""Tests for D4 fetch loaders (H-0011 PR-G4).

Three sklearn-backed fetchers added in v0.8.0:

- ``fetch_california_housing`` — regression demo (sklearn bundle)
- ``fetch_adult_income`` — fairness-relevant binary classification
- ``fetch_compas`` — ProPublica COMPAS recidivism (binary, demo only)

All fetchers raise :class:`ImportError` when ``scikit-learn`` is not
installed (the test for that runs in any environment). The
network-bound tests use ``pytest.importorskip("sklearn")`` and the
``@pytest.mark.slow`` marker so they are excluded from default CI.
"""

from __future__ import annotations

import sys
from unittest import mock

import numpy as np
import pandas as pd
import pytest

import pycatdap

# ---------- ImportError fallback (runs without sklearn) ----------


@pytest.mark.parametrize(
    "loader_name",
    ["fetch_california_housing", "fetch_adult_income", "fetch_compas"],
)
def test_fetchers_raise_importerror_without_sklearn(loader_name: str) -> None:
    """When scikit-learn is unimportable, the loader must surface a
    clear ImportError pointing at the ``pycatdap[data]`` extras.

    We simulate sklearn absence by inserting ``None`` into
    ``sys.modules`` so the ``from sklearn.datasets import ...`` line
    raises ImportError inside the loader.
    """
    loader = getattr(pycatdap.datasets, loader_name)
    with (
        mock.patch.dict(sys.modules, {"sklearn": None, "sklearn.datasets": None}),
        pytest.raises(ImportError, match=r"pycatdap\[data\]"),
    ):
        loader()


# ---------- exports ----------


def test_d4_loaders_exposed_on_datasets_module() -> None:
    assert hasattr(pycatdap.datasets, "fetch_california_housing")
    assert hasattr(pycatdap.datasets, "fetch_adult_income")
    assert hasattr(pycatdap.datasets, "fetch_compas")


# ---------- network-bound smoke tests (slow + sklearn) ----------


@pytest.mark.slow
def test_fetch_california_housing_returns_frame() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_california_housing()
    assert isinstance(df, pd.DataFrame)
    assert "MedHouseVal" in df.columns
    assert len(df) == 20_640


@pytest.mark.slow
def test_fetch_adult_income_returns_frame() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_adult_income()
    assert isinstance(df, pd.DataFrame)
    assert "class" in df.columns
    assert len(df) > 30_000  # OpenML "adult" v2 is ~48,842


@pytest.mark.slow
def test_fetch_compas_returns_frame() -> None:
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_compas()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 5_000


@pytest.mark.slow
def test_fetch_california_housing_works_with_error_analysis() -> None:
    """End-to-end smoke: fetch -> error_analysis pipeline."""
    pytest.importorskip("sklearn")
    df = pycatdap.datasets.fetch_california_housing()
    # synthetic predictions: mean as a baseline regressor
    y_true = df["MedHouseVal"].to_numpy()
    y_pred = np.full_like(y_true, fill_value=float(df["MedHouseVal"].mean()))
    r = pycatdap.error_analysis(
        df.drop(columns=["MedHouseVal"]),
        y_true,
        y_pred,
        top_k=3,
    )
    assert r.task == "regression"
    assert r.mae is not None and r.mae > 0
