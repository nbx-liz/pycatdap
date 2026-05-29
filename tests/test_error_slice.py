"""Tests for the multivariable error-slice containers (H-0014 PR-L2).

Covers the description grammar (``_describe``), the ``ErrorSlice`` /
``SliceDiscoveryResult`` contracts, serialization, and immutability.
The discovery engine that *produces* these is PR-L3.
"""

from __future__ import annotations

import dataclasses

import pytest

from pycatdap.error import ErrorSlice, SliceDiscoveryResult
from pycatdap.error._describe import (
    build_description,
    fmt_number,
    format_condition,
    interval_label,
)

# ---------------------------------------------------------------------------
# _describe grammar
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (45.0, "45"),
        (60.0, "60"),
        (45.5, "45.5"),
        (0.1, "0.1"),
        (-3.0, "-3"),
        (float("inf"), "inf"),
        (float("-inf"), "-inf"),
        (float("nan"), "nan"),
        (60.708540000000006, "60.7085"),  # float-noise rounding
    ],
)
def test_fmt_number(value: float, expected: str) -> None:
    assert fmt_number(value) == expected


def test_interval_label_middle_bin() -> None:
    # boundaries = [45, 60, 80] -> code 1 spans [45, 60]
    assert interval_label(1, [45.0, 60.0, 80.0]) == "[45, 60]"


def test_interval_label_edges() -> None:
    bnds = [45.0, 60.0]
    assert interval_label(0, bnds) == "< 45"
    assert interval_label(2, bnds) == ">= 60"


def test_interval_label_single_bin() -> None:
    assert interval_label(0, []) == "(all)"


def test_format_condition_categorical() -> None:
    assert format_condition("marital_status", "Never-married") == (
        "marital_status = Never-married"
    )


def test_format_condition_interval() -> None:
    assert format_condition("age", "[45, 60]") == "age ∈ [45, 60]"


def test_format_condition_one_sided() -> None:
    # one-sided bounds absorb the operator (no ∈)
    assert format_condition("age", "< 45") == "age < 45"
    assert format_condition("age", ">= 60") == "age >= 60"


def test_format_condition_bracketed_categorical_not_interval() -> None:
    # categorical values that merely look bracketed must NOT use ∈
    assert format_condition("flag", "[High]") == "flag = [High]"
    assert format_condition("grp", "(Other)") == "grp = (Other)"


def test_interval_label_out_of_range_raises() -> None:
    with pytest.raises(ValueError, match="out of range"):
        interval_label(-1, [10.0, 20.0])
    with pytest.raises(ValueError, match="out of range"):
        interval_label(5, [10.0, 20.0])


def test_build_description_acceptance_string() -> None:
    """Issue #20 acceptance criterion: descriptions are parseable verbatim."""
    conditions = (("age", "[45, 60]"), ("marital_status", "Never-married"))
    assert build_description(conditions) == (
        "age ∈ [45, 60] × marital_status = Never-married"
    )


def test_build_description_empty() -> None:
    assert build_description(()) == ""


# ---------------------------------------------------------------------------
# ErrorSlice
# ---------------------------------------------------------------------------


def _make_slice() -> ErrorSlice:
    return ErrorSlice.from_conditions(
        (("age", "[45, 60]"), ("marital_status", "Never-married")),
        size=120,
        error_metric=0.42,
        delta_aic=-18.5,
        measure_value=18.5,
        n_error_in_slice=50,
    )


def test_errorslice_from_conditions_derives_description() -> None:
    s = _make_slice()
    assert s.description == "age ∈ [45, 60] × marital_status = Never-married"
    assert s.conditions == (("age", "[45, 60]"), ("marital_status", "Never-married"))
    assert s.size == 120
    assert s.n_error_in_slice == 50


def test_errorslice_is_frozen() -> None:
    s = _make_slice()
    with pytest.raises(dataclasses.FrozenInstanceError):
        s.size = 1  # type: ignore[misc]


def test_errorslice_is_hashable() -> None:
    # tuple-of-tuples conditions keep the dataclass hashable
    assert len({_make_slice(), _make_slice()}) == 1


# ---------------------------------------------------------------------------
# SliceDiscoveryResult
# ---------------------------------------------------------------------------


def _make_result(n: int = 2) -> SliceDiscoveryResult:
    slices = tuple(
        ErrorSlice.from_conditions(
            (("age", "[45, 60]"),),
            size=100 - i,
            error_metric=0.4 - 0.01 * i,
            delta_aic=-10.0 + i,
            measure_value=10.0 - i,
            n_error_in_slice=40 - i,
        )
        for i in range(n)
    )
    return SliceDiscoveryResult(
        slices=slices,
        measure="aic",
        max_vars=3,
        base_aic=200.0,
        n_evaluated=120,
        n_pruned=380,
        label_kind="error_label",
    )


def test_result_is_frozen() -> None:
    r = _make_result()
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.measure = "x"  # type: ignore[misc]


def test_to_divexplorer_format_shape() -> None:
    r = _make_result(n=3)
    df = r.to_divexplorer_format()
    assert list(df.columns) == [
        "description",
        "size",
        "error_rate",
        "delta_aic",
        "measure_value",
        "n_error_in_slice",
    ]
    assert len(df) == 3
    assert df["description"].iloc[0] == "age ∈ [45, 60]"


def test_to_divexplorer_format_empty() -> None:
    r = SliceDiscoveryResult(
        slices=(),
        measure="aic",
        max_vars=2,
        base_aic=1.0,
        n_evaluated=0,
        n_pruned=0,
    )
    df = r.to_divexplorer_format()
    assert len(df) == 0
    assert list(df.columns) == [
        "description",
        "size",
        "error_rate",
        "delta_aic",
        "measure_value",
        "n_error_in_slice",
    ]


def test_to_dict_structure() -> None:
    r = _make_result(n=2)
    d = r.to_dict()
    assert d["measure"] == "aic"
    assert d["max_vars"] == 3
    assert d["n_evaluated"] == 120
    assert d["n_pruned"] == 380
    assert d["label_kind"] == "error_label"
    assert len(d["slices"]) == 2
    first = d["slices"][0]
    assert first["conditions"] == [["age", "[45, 60]"]]
    assert first["description"] == "age ∈ [45, 60]"
    assert set(first) == {
        "conditions",
        "description",
        "size",
        "error_rate",
        "delta_aic",
        "measure_value",
        "n_error_in_slice",
    }


def test_pruning_ratio_measurable() -> None:
    """n_pruned / (n_evaluated + n_pruned) is the >50% acceptance metric."""
    r = _make_result()
    ratio = r.n_pruned / (r.n_evaluated + r.n_pruned)
    assert ratio == pytest.approx(380 / 500)
    assert ratio > 0.5
