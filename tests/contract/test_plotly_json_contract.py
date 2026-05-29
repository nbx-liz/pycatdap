"""Contract test for ``.to_plotly_json()`` across every public result type.

This suite codifies the data contract that downstream consumers (LizyStudio's
FastAPI + react-plotly.js front end, see Issue #21) depend on.  The contract has
two shapes:

* **FLAT** -- a single Plotly figure spec ``{"data": [...], "layout": {...}}``
  consumable directly by ``react-plotly.js`` / ``plotly.graph_objects.Figure``.
* **SECTIONED** -- a mapping ``{<section_name>: <figure-spec-or-mapping>}`` whose
  section keys are *stable*: a documented set of always-present keys plus
  conditional keys that appear only under a stated trigger.  Every section value
  is itself a FLAT spec, or a mapping of names to FLAT specs.

The hard requirement is JSON-safety: a spec must serialise with
``json.dumps(..., allow_nan=False)`` (NaN / Infinity are not valid JSON and
break ``JSON.parse`` in the browser).

See HISTORY.md H-0015 §A and BLUEPRINT.md §5.7 (DP-4).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap.suite import AICIndependenceSuite

# --------------------------------------------------------------------------- #
# Contract assertions
# --------------------------------------------------------------------------- #


def _is_flat(spec: Any) -> bool:
    """A FLAT figure spec is exactly ``{"data": ..., "layout": ...}``."""
    return isinstance(spec, dict) and set(spec.keys()) == {"data", "layout"}


def assert_flat(spec: Any) -> None:
    """Assert ``spec`` is a well-formed FLAT Plotly figure spec."""
    assert _is_flat(spec), f"expected FLAT {{data, layout}}, got keys {sorted(spec)}"
    assert isinstance(spec["data"], list), "FLAT 'data' must be a list of traces"
    for trace in spec["data"]:
        assert isinstance(trace, dict), "each trace must be a dict"
        assert "type" in trace, "each trace must declare a 'type'"
    assert isinstance(spec["layout"], dict), "FLAT 'layout' must be a dict"


def assert_section_value(value: Any) -> None:
    """A SECTIONED value is either a FLAT spec or a mapping of name -> FLAT spec."""
    if _is_flat(value):
        assert_flat(value)
        return
    assert isinstance(value, dict), (
        "a section value must be a FLAT spec or a mapping of name -> FLAT spec, "
        f"got {type(value).__name__}"
    )
    # Mapping of name -> FLAT spec (e.g. top_summaries: dict[col -> figure]).
    for name, child in value.items():
        assert _is_flat(child), f"nested section '{name}' must be a FLAT spec"
        assert_flat(child)


def assert_json_safe(spec: Any) -> None:
    """Assert the spec round-trips through strict JSON (no NaN / Infinity)."""
    # allow_nan=False raises ValueError on NaN/Inf -- the browser cannot parse them.
    text = json.dumps(spec, allow_nan=False)
    # Round-trip back to confirm structural integrity.
    assert json.loads(text) is not None


def assert_flat_contract(spec: Any) -> None:
    assert_flat(spec)
    assert_json_safe(spec)


def assert_sectioned_contract(
    spec: Any, *, always: set[str], allowed: set[str]
) -> None:
    assert isinstance(spec, dict), "SECTIONED spec must be a dict"
    assert not _is_flat(spec), "SECTIONED spec must not be a bare FLAT figure"
    keys = set(spec.keys())
    missing = always - keys
    assert not missing, f"missing always-present section keys: {sorted(missing)}"
    extra = keys - allowed
    assert not extra, f"unexpected section keys (not in contract): {sorted(extra)}"
    for value in spec.values():
        assert_section_value(value)
    assert_json_safe(spec)


# --------------------------------------------------------------------------- #
# Result builders (minimal synthetic inputs via the public API)
# --------------------------------------------------------------------------- #


def _classification_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Y": ["a"] * 30 + ["b"] * 20,
            "X1": ["p"] * 20 + ["q"] * 10 + ["p"] * 5 + ["q"] * 15,
            "X2": ["m"] * 25 + ["n"] * 25,
        }
    )


def build_catdap1() -> Any:
    return pycatdap.catdap1(_classification_frame(), response_names=["Y"])


def build_catdap2() -> Any:
    return pycatdap.catdap2(_classification_frame(), pool=[2, 2, 2], response_name="Y")


def build_describe() -> Any:
    df = pd.DataFrame(
        {
            "x_cont": [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5],
            "x_cat": ["a", "b", "a", "c", "a", "b", "c", "a", "b", "c"],
        }
    )
    return pycatdap.describe(df)


def _profile_frame() -> pd.DataFrame:
    rng = np.random.default_rng(seed=11)
    n = 120
    cat = rng.choice(["a", "b", "c"], size=n)
    return pd.DataFrame(
        {
            "target": rng.choice(["yes", "no"], size=n),
            "cat": cat,
            "cont": np.where(cat == "a", 0.0, 5.0) + rng.normal(0.0, 1.0, size=n),
        }
    )


def build_profile_no_response() -> Any:
    return pycatdap.profile(_profile_frame())


def build_profile_with_response() -> Any:
    return pycatdap.profile(_profile_frame(), response="target", top_k_subsets=2)


def build_quality_report() -> Any:
    n = 200
    df = pd.DataFrame(
        {
            "almost_all_nan": [np.nan] * 110 + list(range(90)),
            "constant_col": ["x"] * n,
            "id_like": [f"id-{i}" for i in range(n)],
            "high_card": [f"v-{i % 150}" for i in range(n)],
            "ok": np.arange(n, dtype=float),
        }
    )
    return pycatdap.quality_report(df)


def build_suite() -> Any:
    n = 200
    rng = np.random.default_rng(seed=23)
    df = pd.DataFrame(
        {
            "y": rng.choice(["yes", "no"], size=n),
            "constant": ["x"] * n,
            "high_card_str": [f"v-{i % 150}" for i in range(n)],
            "informative": np.where(rng.choice([0, 1], size=n) == 0, "yes", "no"),
            "noise": rng.choice(["a", "b"], size=n),
        }
    )
    return AICIndependenceSuite(df, response="y").run()


def _target_frame_classification() -> pd.DataFrame:
    rng = np.random.default_rng(seed=23)
    n = 200
    sex = rng.choice(["m", "f"], size=n)
    target = np.where(sex == "m", "yes", "no")
    flip = rng.random(n) < 0.1
    target = np.where(flip, np.where(target == "yes", "no", "yes"), target)
    return pd.DataFrame(
        {
            "target": target,
            "informative_cat": sex,
            "noisy_cat": rng.choice(["a", "b", "c"], size=n),
            "noisy_num": rng.normal(0, 1, size=n),
        }
    )


def build_target_analysis_classification() -> Any:
    return pycatdap.target_analysis(
        _target_frame_classification(), response="target", top_k=2
    )


def build_target_analysis_regression() -> Any:
    rng = np.random.default_rng(seed=31)
    n = 200
    x = rng.normal(0, 1, size=n)
    df = pd.DataFrame(
        {
            "y_cont": x * 3.0 + rng.normal(0, 0.5, size=n),
            "informative_num": x,
            "noisy_cat": rng.choice(["a", "b"], size=n),
        }
    )
    return pycatdap.target_analysis(df, response="y_cont", top_k=1)


def _error_frame() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n = 60
    age = rng.choice(["young", "old"], size=n)
    y_true = np.where(age == "old", 1, 0)
    y_pred = np.where(rng.random(n) < 0.2, 1 - y_true, y_true)
    return pd.DataFrame(
        {
            "age": age,
            "y_true": y_true.astype(int),
            "y_pred": y_pred.astype(int),
        }
    )


def build_error_analysis() -> Any:
    return pycatdap.error_analysis(_error_frame(), "y_true", "y_pred", top_k=1)


def build_error_analysis_regression() -> Any:
    """Regression task: the ``confusion`` section must be suppressed."""
    rng = np.random.default_rng(3)
    n = 90
    x = rng.normal(0.0, 1.0, size=n)
    y_true = 2.0 * x + rng.normal(0.0, 0.3, size=n)
    y_pred = y_true + rng.normal(0.0, 0.6, size=n)
    df = pd.DataFrame(
        {
            "grp": rng.choice(["a", "b", "c"], size=n),
            "y_true": y_true,
            "y_pred": y_pred,
        }
    )
    return pycatdap.error_analysis(df, "y_true", "y_pred", top_k=1)


# --------------------------------------------------------------------------- #
# FLAT cases
# --------------------------------------------------------------------------- #

FLAT_BUILDERS: dict[str, Callable[[], Any]] = {
    "Catdap1Result": build_catdap1,
    "Catdap2Result": build_catdap2,
    "DescribeResult": build_describe,
}


@pytest.mark.parametrize("name", sorted(FLAT_BUILDERS))
def test_flat_results_satisfy_contract(name: str) -> None:
    result = FLAT_BUILDERS[name]()
    assert_flat_contract(result.to_plotly_json())


# --------------------------------------------------------------------------- #
# SECTIONED cases: (builder, always-present keys, full allowed key set)
# --------------------------------------------------------------------------- #

SECTIONED_CASES: dict[str, tuple[Callable[[], Any], set[str], set[str]]] = {
    "ProfileResult (no response)": (
        build_profile_no_response,
        {"association_heatmap"},
        {"association_heatmap"},
    ),
    "ProfileResult (with response)": (
        build_profile_with_response,
        {"association_heatmap", "top_subsets"},
        {"association_heatmap", "top_subsets"},
    ),
    "QualityReport": (
        build_quality_report,
        {"warnings_table"},
        {"warnings_table"},
    ),
    "SuiteResult": (
        build_suite,
        {"checks_table"},
        {"checks_table"},
    ),
    "TargetAnalysisResult (classification)": (
        build_target_analysis_classification,
        {"ranking", "top_summaries"},
        {"ranking", "top_summaries"},
    ),
    "TargetAnalysisResult (regression)": (
        build_target_analysis_regression,
        {"ranking", "top_summaries"},
        {"ranking", "top_summaries"},
    ),
    "ErrorAnalysisResult (classification)": (
        build_error_analysis,
        {"feature_ranking", "top_summaries"},
        {"feature_ranking", "top_summaries", "confusion"},
    ),
    "ErrorAnalysisResult (regression)": (
        build_error_analysis_regression,
        {"feature_ranking", "top_summaries"},
        {"feature_ranking", "top_summaries"},  # confusion suppressed for regression
    ),
}


@pytest.mark.parametrize("name", sorted(SECTIONED_CASES))
def test_sectioned_results_satisfy_contract(name: str) -> None:
    builder, always, allowed = SECTIONED_CASES[name]
    result = builder()
    assert_sectioned_contract(result.to_plotly_json(), always=always, allowed=allowed)


def test_profile_top_subsets_is_conditional_on_response() -> None:
    """``top_subsets`` appears only when a response is supplied."""
    without = build_profile_no_response().to_plotly_json()
    with_response = build_profile_with_response().to_plotly_json()
    assert "top_subsets" not in without
    assert "top_subsets" in with_response


def test_error_confusion_is_conditional_on_classification() -> None:
    """``confusion`` is present for classification and absent for regression."""
    clf = build_error_analysis().to_plotly_json()
    assert "confusion" in clf, "classification error analysis must expose confusion"
    assert_flat(clf["confusion"])
    reg = build_error_analysis_regression().to_plotly_json()
    assert "confusion" not in reg, "regression error analysis must omit confusion"


# --------------------------------------------------------------------------- #
# react-plotly.js compatibility: every FLAT spec must build a real Figure
# --------------------------------------------------------------------------- #

_ALL_FLAT_SPEC_PROVIDERS: dict[str, Callable[[], Any]] = {
    "Catdap1Result": build_catdap1,
    "Catdap2Result": build_catdap2,
    "DescribeResult": build_describe,
    "ProfileResult": build_profile_with_response,
    "QualityReport": build_quality_report,
    "SuiteResult": build_suite,
    "TargetAnalysisResult": build_target_analysis_classification,
    "ErrorAnalysisResult": build_error_analysis,
}


def _iter_flat_specs(spec: Any) -> list[dict[str, Any]]:
    """Yield every FLAT figure spec reachable inside ``spec``."""
    flats: list[dict[str, Any]] = []
    if _is_flat(spec):
        flats.append(spec)
        return flats
    if isinstance(spec, dict):
        for value in spec.values():
            flats.extend(_iter_flat_specs(value))
    return flats


@pytest.mark.parametrize("name", sorted(_ALL_FLAT_SPEC_PROVIDERS))
def test_specs_build_real_plotly_figures(name: str) -> None:
    """Each FLAT spec must instantiate a ``plotly.graph_objects.Figure``."""
    go = pytest.importorskip("plotly.graph_objects")
    result = _ALL_FLAT_SPEC_PROVIDERS[name]()
    specs = _iter_flat_specs(result.to_plotly_json())
    assert specs, f"{name} produced no FLAT figure spec"
    for spec in specs:
        go.Figure(spec)
