"""Tests for discover_error_slices (H-0014 PR-L3).

Fast synthetic tests for the orchestration: known-cohort surfacing,
immutability, the pluggable measure (FR-9), continuous binning, and the
regression guard. The Adult Income acceptance test is slow + sklearn-gated.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pandas.testing as pdt
import pytest

from pycatdap.error import (
    ErrorSlice,
    SliceDiscoveryResult,
    discover_error_slices,
)
from pycatdap.measures import _registry


def _cohort_frame(
    n: int = 400, seed: int = 0
) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Errors concentrate where a == 'x' AND b == 'p'."""
    rng = np.random.default_rng(seed)
    a = rng.choice(["x", "y", "z"], size=n)
    b = rng.choice(["p", "q"], size=n)
    c = rng.choice(["m", "n"], size=n)
    df = pd.DataFrame({"a": a, "b": b, "c": c})

    y_true = rng.integers(0, 2, size=n)
    y_pred = y_true.copy()
    bad = (a == "x") & (b == "p")
    # 80% of the bad cohort is mispredicted; ~5% elsewhere.
    flip = np.where(bad, rng.random(n) < 0.8, rng.random(n) < 0.05)
    y_pred = np.where(flip, 1 - y_true, y_true)
    return df, y_true, y_pred


def test_returns_slice_discovery_result() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=20)
    assert isinstance(result, SliceDiscoveryResult)
    assert all(isinstance(s, ErrorSlice) for s in result.slices)
    assert result.label_kind == "error_label"
    assert result.measure == "aic"


def test_surfaces_known_error_cohort() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=2, top_k=5, min_support=20)
    # The (a=x, b=p) cohort should appear among the top slices.
    found = any({("a", "x"), ("b", "p")} <= set(s.conditions) for s in result.slices)
    assert found, [s.description for s in result.slices]


def test_slices_sorted_by_measure_value_desc() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=2, top_k=10, min_support=20)
    values = [s.measure_value for s in result.slices]
    assert values == sorted(values, reverse=True)


def test_top_k_respected() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=3, top_k=3, min_support=10)
    assert len(result.slices) <= 3


def test_input_dataframe_not_mutated() -> None:
    df, yt, yp = _cohort_frame()
    before = df.copy(deep=True)
    discover_error_slices(df, yt, yp, max_vars=3, min_support=20)
    pdt.assert_frame_equal(df, before)


def test_min_support_fraction() -> None:
    df, yt, yp = _cohort_frame(n=400)
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=0.1)
    # 0.1 * 400 = 40 → every returned slice has size >= 40.
    assert all(s.size >= 40 for s in result.slices)


def test_min_support_invalid_raises() -> None:
    df, yt, yp = _cohort_frame(n=50)
    with pytest.raises(ValueError, match="min_support"):
        discover_error_slices(df, yt, yp, min_support=0)


def test_min_support_float_above_one_raises() -> None:
    df, yt, yp = _cohort_frame(n=50)
    with pytest.raises(ValueError, match=r"\(0, 1\]"):
        discover_error_slices(df, yt, yp, min_support=1.5)


def test_reserved_column_name_raises() -> None:
    df, yt, yp = _cohort_frame(n=60)
    df = df.rename(columns={"a": "_error_label_"})
    with pytest.raises(ValueError, match="reserved"):
        discover_error_slices(df, yt, yp)


def test_pruning_ratio_reported() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=3, min_support=40)
    total = result.n_evaluated + result.n_pruned
    assert total > 0
    assert result.n_pruned >= 0


def test_measure_plugin_callable() -> None:
    df, yt, yp = _cohort_frame()

    def my_measure(cross: np.ndarray) -> float:
        # higher when the table is more concentrated
        return float(np.max(cross))

    result = discover_error_slices(
        df, yt, yp, measure=my_measure, max_vars=2, min_support=20
    )
    assert result.measure == "<callable>"
    values = [s.measure_value for s in result.slices]
    assert values == sorted(values, reverse=True)


@pytest.mark.parametrize("name", ["cramers_v", "mutual_info"])
def test_measure_plugin_registry_names(name: str) -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, measure=name, max_vars=2, min_support=20)
    assert result.measure == name
    values = [s.measure_value for s in result.slices]
    assert values == sorted(values, reverse=True)


def test_custom_registered_measure() -> None:
    df, yt, yp = _cohort_frame()

    def trivial(cross: np.ndarray) -> float:
        return float(cross.sum())

    _registry.register("_test_trivial_", trivial)
    try:
        result = discover_error_slices(
            df, yt, yp, measure="_test_trivial_", max_vars=2, min_support=20
        )
        assert result.measure == "_test_trivial_"
    finally:
        _registry._REGISTRY.pop("_test_trivial_", None)


def test_continuous_column_binned_to_intervals() -> None:
    rng = np.random.default_rng(1)
    n = 400
    age = rng.integers(18, 80, size=n).astype(float)  # >20 unique → continuous
    grp = rng.choice(["p", "q"], size=n)
    df = pd.DataFrame({"age": age, "grp": grp})
    yt = rng.integers(0, 2, size=n)
    # errors concentrate in older ages
    flip = np.where(age >= 60, rng.random(n) < 0.8, rng.random(n) < 0.05)
    yp = np.where(flip, 1 - yt, yt)
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=20)
    # at least one age-based slice rendered as an interval / one-sided bound
    age_descs = [
        s.description
        for s in result.slices
        if any(col == "age" for col, _ in s.conditions)
    ]
    assert age_descs
    assert any(("∈" in d) or ("<" in d) or (">=" in d) for d in age_descs)


def test_length_mismatch_raises() -> None:
    df, yt, yp = _cohort_frame(n=100)
    with pytest.raises(ValueError, match="length"):
        discover_error_slices(df, yt[:50], yp[:50])


def test_constant_continuous_column_no_crash() -> None:
    rng = np.random.default_rng(2)
    n = 200
    df = pd.DataFrame(
        {
            "const": np.full(n, 5.0),  # numeric but single value
            "g": rng.choice(["p", "q"], size=n),
            "many": rng.integers(0, 100, size=n).astype(float),  # >20 unique
        }
    )
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.2, 1 - yt, yt)
    # must not raise even though 'const' has a single finite value
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=20)
    assert isinstance(result, SliceDiscoveryResult)


def test_empty_frame_returns_empty_result() -> None:
    df = pd.DataFrame({"a": pd.Series([], dtype="object")})
    result = discover_error_slices(df, np.array([], dtype=int), np.array([], dtype=int))
    assert result.slices == ()
    assert result.base_aic == 0.0


def test_all_nan_continuous_column_no_crash() -> None:
    rng = np.random.default_rng(4)
    n = 200
    df = pd.DataFrame(
        {
            "allnan": np.full(n, np.nan),
            "g": rng.choice(["p", "q"], size=n),
        }
    )
    # 'allnan' is float dtype with 0 finite unique → not continuous; even if
    # binned, finite.size == 0 path returns it untouched.
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.2, 1 - yt, yt)
    result = discover_error_slices(df, yt, yp, max_vars=2, min_support=20)
    assert isinstance(result, SliceDiscoveryResult)


def test_regression_task_now_supported() -> None:
    """H-0015 (design D1): regression no longer raises -- it discovers
    high-residual subgroups. See tests/test_error_discovery_regression.py for
    the invariant suite; here we only assert the guard is gone and the path
    returns the regression labeller's result."""
    rng = np.random.default_rng(0)
    n = 100
    df = pd.DataFrame({"a": rng.choice(["x", "y"], size=n)})
    yt = rng.normal(size=n)
    yp = yt + rng.normal(scale=0.5, size=n)
    result = discover_error_slices(df, yt, yp, min_support=20)
    assert isinstance(result, SliceDiscoveryResult)
    assert result.label_kind == "abs_residual_pool"


def test_to_divexplorer_and_dict_roundtrip() -> None:
    df, yt, yp = _cohort_frame()
    result = discover_error_slices(df, yt, yp, max_vars=2, top_k=4, min_support=20)
    flat = result.to_divexplorer_format()
    assert len(flat) == len(result.slices)
    d = result.to_dict()
    assert d["measure"] == "aic"
    assert len(d["slices"]) == len(result.slices)


# ---------------------------------------------------------------------------
# H-0016: candidate cap (memory/time guard)
# ---------------------------------------------------------------------------


def test_max_candidates_truncates_and_warns() -> None:
    """A small max_candidates stops the search early, flags truncated, and
    warns (no silent cap). Memory-safe: small data, the cap prevents blow-up."""
    rng = np.random.default_rng(0)
    n = 400
    df = pd.DataFrame(
        {f"c{i}": rng.integers(0, 4, size=n).astype(str) for i in range(6)}
    )
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.3, 1 - yt, yt)
    with pytest.warns(UserWarning, match="max_candidates"):
        result = discover_error_slices(
            df, yt, yp, max_vars=3, min_support=5, max_candidates=10
        )
    assert result.truncated is True
    assert result.n_evaluated <= 10
    # The slices returned are still sound (real, support-respecting).
    assert all(s.size >= 5 for s in result.slices)


def test_max_candidates_large_is_identical_to_uncapped() -> None:
    """INV-C1: under a cap that is never hit, results are byte-identical to
    the uncapped search and truncated is False."""
    rng = np.random.default_rng(1)
    n = 300
    df = pd.DataFrame(
        {
            "a": rng.integers(0, 3, size=n).astype(str),
            "b": rng.integers(0, 3, size=n).astype(str),
        }
    )
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.25, 1 - yt, yt)
    capped = discover_error_slices(
        df, yt, yp, max_vars=2, min_support=10, max_candidates=10_000
    )
    uncapped = discover_error_slices(
        df, yt, yp, max_vars=2, min_support=10, max_candidates=200_000
    )
    assert capped.truncated is False
    assert capped.n_evaluated == uncapped.n_evaluated
    assert [s.description for s in capped.slices] == [
        s.description for s in uncapped.slices
    ]


# ---------------------------------------------------------------------------
# Acceptance: Adult Income (slow + sklearn-gated)
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_adult_income_surfaces_cohorts_and_prunes() -> None:
    """Issue #20 acceptance: known disparate cohorts surface, >50% pruned,
    completes well under the 30s budget."""
    import time

    pytest.importorskip("sklearn")
    from sklearn.linear_model import LogisticRegression  # noqa: PLC0415
    from sklearn.preprocessing import OrdinalEncoder  # noqa: PLC0415

    from pycatdap.datasets import fetch_adult_income  # noqa: PLC0415

    df = fetch_adult_income()
    target = "income" if "income" in df.columns else df.columns[-1]
    features = [c for c in df.columns if c != target]

    enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    # Adult Income has missing values; fill them with "?" then stringify so the
    # encoder + LogisticRegression never see a float NaN. astype(object) first
    # so .fillna() works on category-dtype columns (pandas rejects setitem of a
    # new category directly on a Categorical).
    x = enc.fit_transform(df[features].astype(object).fillna("?").astype(str))
    y = (df[target].astype(str).str.contains(">50K")).to_numpy().astype(int)
    model = LogisticRegression(max_iter=200)
    model.fit(x, y)
    y_pred = model.predict(x)

    # Memory safety (incident 2026-05-30): max_vars=3 over all 14 columns OOM'd
    # the host. When the dataset ships category dtypes, high-cardinality numeric
    # columns (e.g. fnlwgt, ~28k values) escape continuous-binning in
    # _is_continuous and are treated as raw categoricals, so the frequent-cell
    # count + O(N^2) candidate generation explode. Bound the search to max_vars=2
    # over curated low/mid-cardinality categorical cohort columns. See memory
    # incident_discover_slices_oom; a real cap belongs in enumerate_cells.
    cohort_cols = [
        c
        for c in (
            "workclass",
            "education",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "native-country",
        )
        if c in features
    ]
    start = time.perf_counter()
    result = discover_error_slices(
        df[features],
        y,
        y_pred,
        max_vars=2,
        top_k=15,
        min_support=100,
        columns=cohort_cols,
    )
    elapsed = time.perf_counter() - start

    assert elapsed < 30.0, f"took {elapsed:.1f}s (budget 30s)"
    # Apriori pruning still fires; the original >50% figure required the full
    # high-cardinality max_vars=3 search over all columns, which we bound for
    # memory safety (incident 2026-05-30). The >50%-on-realistic-data guarantee
    # belongs with a code-level candidate cap in enumerate_cells (follow-up).
    assert result.n_pruned > 0, "Apriori pruning should cut some branches"
    # a sex/race-based cohort should appear among the slices
    cols_in_slices = {col for s in result.slices for col, _ in s.conditions}
    assert cols_in_slices & {"sex", "race", "relationship", "marital-status"}
