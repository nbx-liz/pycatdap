"""Tests for the pysubgroup interop measure ``AICMeasure`` (H-0018, #31).

``AICMeasure`` bridges pycatdap's ΔAIC to pysubgroup's binary-target
``QualityFunction`` interface so AIC can be used as the interestingness
measure for pysubgroup's ``BeamSearch`` / ``SimpleDFS``.

pysubgroup is an **optional** dependency:

- the cross-tests use ``pytest.importorskip("pysubgroup")``;
- the ImportError-fallback test runs in any environment by masking
  ``pysubgroup`` in ``sys.modules`` and forcing the bridge module to
  re-import.
"""

from __future__ import annotations

import sys
import warnings
from unittest import mock

import numpy as np
import pandas as pd
import pytest

import pycatdap
import pycatdap.measures

# ---------- lazy import contract (runs without pysubgroup) ----------


def test_measures_import_does_not_require_pysubgroup() -> None:
    """Importing ``pycatdap.measures`` must not eagerly import pysubgroup;
    the standard table measures stay available regardless."""
    assert callable(pycatdap.measures.aic)
    assert "aic" in pycatdap.measures.list_measures()


def test_measures_getattr_raises_attributeerror_for_unknown() -> None:
    """PEP 562 ``__getattr__`` must reject unknown names (not return None)."""
    with pytest.raises(AttributeError):
        _ = pycatdap.measures.does_not_exist  # type: ignore[attr-defined]


def test_aicmeasure_raises_importerror_without_pysubgroup() -> None:
    """When pysubgroup is unimportable, accessing ``AICMeasure`` must
    surface a clear ImportError telling the user to ``pip install
    pysubgroup``. We mask pysubgroup and drop the cached bridge module so
    its top-level import re-runs."""
    with mock.patch.dict(sys.modules):
        sys.modules["pysubgroup"] = None  # type: ignore[assignment]
        sys.modules.pop("pycatdap.measures._pysubgroup", None)
        with pytest.raises(ImportError, match=r"pip install pysubgroup"):
            _ = pycatdap.measures.AICMeasure


# ---------- AICMeasure behaviour (needs pysubgroup) ----------


def _binary_frame(separating: bool) -> pd.DataFrame:
    """Build a frame where column ``a`` either separates ``target``
    strongly (``separating=True``) or is independent of it."""
    rng = np.random.RandomState(0)
    n = 400
    a = rng.choice(["x", "y"], n)
    if separating:
        target = ((a == "x") & (rng.rand(n) < 0.85)) | (
            (a == "y") & (rng.rand(n) < 0.15)
        )
    else:
        target = rng.rand(n) < 0.5
    return pd.DataFrame({"a": a, "target": target})


def test_aicmeasure_accessible_via_measures_namespace() -> None:
    ps = pytest.importorskip("pysubgroup")
    qf = pycatdap.measures.AICMeasure()
    assert isinstance(qf, ps.AbstractInterestingnessMeasure)


def test_aicmeasure_quality_positive_for_informative_selector() -> None:
    """An informative selector (ΔAIC < 0) maps to positive quality
    (pysubgroup maximises; quality = -ΔAIC)."""
    ps = pytest.importorskip("pysubgroup")
    df = _binary_frame(separating=True)
    target = ps.BinaryTarget("target", True)
    qf = pycatdap.measures.AICMeasure()
    qf.calculate_constant_statistics(df, target)
    quality = qf.evaluate(ps.EqualitySelector("a", "x"), target, df)
    assert quality > 0


def test_aicmeasure_quality_not_positive_for_noise_selector() -> None:
    """A noise selector (independent of target, ΔAIC > 0) must not map to
    positive quality."""
    ps = pytest.importorskip("pysubgroup")
    df = _binary_frame(separating=False)
    target = ps.BinaryTarget("target", True)
    qf = pycatdap.measures.AICMeasure()
    qf.calculate_constant_statistics(df, target)
    quality = qf.evaluate(ps.EqualitySelector("a", "x"), target, df)
    assert quality <= 0


def test_aicmeasure_empty_subgroup_is_nan() -> None:
    """A selector covering zero rows yields NaN (StandardQF convention)."""
    ps = pytest.importorskip("pysubgroup")
    df = _binary_frame(separating=True)
    target = ps.BinaryTarget("target", True)
    qf = pycatdap.measures.AICMeasure()
    qf.calculate_constant_statistics(df, target)
    quality = qf.evaluate(ps.EqualitySelector("a", "no_such_value"), target, df)
    assert np.isnan(quality)


def test_aicmeasure_evaluate_emits_no_runtime_warning() -> None:
    """Degenerate contingency tables must not leak numpy RuntimeWarnings."""
    ps = pytest.importorskip("pysubgroup")
    # ``a`` is constant, so a selector on it covers ALL rows -> the
    # out-subgroup column is all-zero (the degenerate path that triggers
    # numpy's divide warning unless suppressed in evaluate()).
    df = pd.DataFrame({"a": ["x"] * 100, "target": [True] * 30 + [False] * 70})
    target = ps.BinaryTarget("target", True)
    qf = pycatdap.measures.AICMeasure()
    qf.calculate_constant_statistics(df, target)
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        # raises if evaluate() leaks a RuntimeWarning on the all-zero column
        quality = qf.evaluate(ps.EqualitySelector("a", "x"), target, df)
    assert isinstance(quality, float)


# ---------- cross-test vs native discover_error_slices (#31 AC) ----------


def test_aicmeasure_beamsearch_ranks_informative_variable_top() -> None:
    """``pysubgroup.BeamSearch().execute(task, qf=AICMeasure())`` must run
    and rank the informative variable above the noise variable."""
    ps = pytest.importorskip("pysubgroup")
    rng = np.random.RandomState(1)
    n = 600
    a = rng.choice(["x", "y"], n)  # informative
    b = rng.choice(["p", "q"], n)  # noise
    target = ((a == "x") & (rng.rand(n) < 0.85)) | ((a == "y") & (rng.rand(n) < 0.15))
    df = pd.DataFrame({"a": a, "b": b, "target": target})
    tgt = ps.BinaryTarget("target", True)
    search_space = ps.create_selectors(df, ignore=["target"])
    task = ps.SubgroupDiscoveryTask(
        df,
        tgt,
        search_space,
        result_set_size=4,
        depth=1,
        qf=pycatdap.measures.AICMeasure(),
    )
    result = ps.BeamSearch().execute(task)
    descriptions = result.to_descriptions()
    # top single-selector subgroup must reference the informative column 'a'
    top_quality, top_sg = descriptions[0]
    assert "a=" in str(top_sg)
    assert top_quality > 0


def test_aicmeasure_consistent_with_native_discover_error_slices() -> None:
    """The variable AICMeasure+BeamSearch ranks highest must match the
    variable pycatdap's native slice discovery surfaces as most
    informative — both are driven by the same ΔAIC."""
    ps = pytest.importorskip("pysubgroup")
    rng = np.random.RandomState(2)
    n = 600
    a = rng.choice(["x", "y"], n)  # informative
    b = rng.choice(["p", "q"], n)  # noise
    y_true = ((a == "x") & (rng.rand(n) < 0.85)) | ((a == "y") & (rng.rand(n) < 0.15))
    y_pred = np.zeros(n, dtype=bool)  # constant predictor -> error == y_true
    df = pd.DataFrame({"a": a, "b": b})

    # native: which column dominates the top slice?
    native = pycatdap.error.discover_error_slices(
        df, y_true.astype(int), y_pred.astype(int), max_vars=1, top_k=3
    )
    native_cols = {cond[0] for s in native.slices for cond in s.conditions}
    assert "a" in native_cols

    # pysubgroup path: top subgroup references the same column 'a'
    tgt = ps.BinaryTarget("target", True)
    df2 = df.assign(target=y_true)
    search_space = ps.create_selectors(df2, ignore=["target"])
    task = ps.SubgroupDiscoveryTask(
        df2,
        tgt,
        search_space,
        result_set_size=3,
        depth=1,
        qf=pycatdap.measures.AICMeasure(),
    )
    result = ps.BeamSearch().execute(task)
    _, top_sg = result.to_descriptions()[0]
    assert "a=" in str(top_sg)
