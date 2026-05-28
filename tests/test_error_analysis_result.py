"""Tests for :class:`pycatdap.error.Slice` and
:class:`pycatdap.error.ErrorAnalysisResult` (H-0011 PR-G1).

These dataclasses are the result containers for the Phase H
``error_analysis()`` one-call wrapper (H-0011 §B). They follow the
v0.6.1 H-0009 immutable pattern:

- ``frozen=True`` blocks attribute reassignment
- ``feature_ranking`` / ``confusion`` numpy buffers frozen via
  ``__post_init__``
- ``top_slices`` is a ``tuple`` (no ``list``)
- ``top_summaries`` is wrapped in ``MappingProxyType`` (no ``dict``)
- ``residual_pooling`` is wrapped in ``MappingProxyType``

PR-G1 covers the dataclass contract only. The actual
``error_analysis()`` wrapper that constructs these results lands in
PR-G2.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest

from pycatdap._target_pair import TargetSummary, target_summary
from pycatdap.error import ErrorAnalysisResult, Slice

# ---------- Slice ----------


def test_slice_basic_construction() -> None:
    s = Slice(
        variable="age",
        category="young",
        error_category="incorrect",
        n_in_slice=30,
        n_error_in_slice=18,
        error_rate=0.6,
        pearson_residual=3.2,
        delta_aic=-12.5,
    )
    assert s.variable == "age"
    assert s.category == "young"
    assert s.error_category == "incorrect"
    assert s.n_in_slice == 30
    assert s.n_error_in_slice == 18
    assert s.error_rate == pytest.approx(0.6)
    assert s.pearson_residual == pytest.approx(3.2)
    assert s.delta_aic == pytest.approx(-12.5)


def test_slice_is_frozen() -> None:
    s = Slice(
        variable="age",
        category="young",
        error_category="incorrect",
        n_in_slice=10,
        n_error_in_slice=5,
        error_rate=0.5,
        pearson_residual=2.1,
        delta_aic=-3.0,
    )
    with pytest.raises(FrozenInstanceError):
        s.variable = "sex"  # type: ignore[misc]


def test_slice_repr_includes_variable_and_residual() -> None:
    s = Slice(
        variable="cholesterol",
        category="high",
        error_category="FP",
        n_in_slice=12,
        n_error_in_slice=9,
        error_rate=0.75,
        pearson_residual=2.8,
        delta_aic=-5.5,
    )
    r = repr(s)
    assert "cholesterol" in r
    assert "high" in r
    assert "FP" in r


# ---------- ErrorAnalysisResult: shared fixtures ----------


@pytest.fixture
def classification_ranking() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "variable": "age",
                "delta_aic": -12.5,
                "kind": "categorical",
                "n_obs": 100,
            },
            {"variable": "sex", "delta_aic": -4.0, "kind": "categorical", "n_obs": 100},
        ],
        columns=["variable", "delta_aic", "kind", "n_obs"],
    )


@pytest.fixture
def classification_confusion() -> pd.DataFrame:
    return pd.DataFrame(
        [[40, 5], [10, 45]],
        index=pd.Index(["TP", "FP"], name="confusion"),
        columns=pd.Index(["young", "old"], name="age"),
    )


@pytest.fixture
def regression_ranking() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"variable": "x1", "delta_aic": -25.0, "kind": "numeric", "n_obs": 200},
        ],
        columns=["variable", "delta_aic", "kind", "n_obs"],
    )


@pytest.fixture
def sample_target_summary() -> TargetSummary:
    df = pd.DataFrame(
        {
            "label": ["correct"] * 30 + ["incorrect"] * 20,
            "age": ["young"] * 15 + ["old"] * 15 + ["young"] * 12 + ["old"] * 8,
        }
    )
    return target_summary(df, target="label", explanatory="age")


@pytest.fixture
def sample_slice() -> Slice:
    return Slice(
        variable="age",
        category="young",
        error_category="incorrect",
        n_in_slice=27,
        n_error_in_slice=12,
        error_rate=12 / 27,
        pearson_residual=2.5,
        delta_aic=-7.0,
    )


# ---------- ErrorAnalysisResult: classification path ----------


def test_classification_result_basic_construction(
    classification_ranking: pd.DataFrame,
    classification_confusion: pd.DataFrame,
    sample_target_summary: TargetSummary,
    sample_slice: Slice,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="confusion_label",
        response_name="__pycatdap_confusion_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(sample_slice,),
        confusion=classification_confusion,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    assert result.task == "classification"
    assert result.label_kind == "confusion_label"
    assert result.n_correct == 85
    assert result.n_incorrect == 15
    assert result.mae is None
    assert result.rmse is None


def test_result_is_frozen(
    classification_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    with pytest.raises(FrozenInstanceError):
        result.task = "regression"  # type: ignore[misc]


def test_feature_ranking_numpy_buffer_is_frozen(
    classification_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    for col in result.feature_ranking.columns:
        values = result.feature_ranking[col].values
        if isinstance(values, np.ndarray):
            with pytest.raises(ValueError, match="read-only|assignment"):
                values[0] = values[0]


def test_confusion_numpy_buffer_is_frozen_when_present(
    classification_ranking: pd.DataFrame,
    classification_confusion: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="confusion_label",
        response_name="__pycatdap_confusion_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(),
        confusion=classification_confusion,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    assert result.confusion is not None
    for col in result.confusion.columns:
        values = result.confusion[col].values
        if isinstance(values, np.ndarray):
            with pytest.raises(ValueError, match="read-only|assignment"):
                values[0] = values[0]


def test_top_slices_must_be_tuple(
    classification_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
    sample_slice: Slice,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(sample_slice,),
        confusion=None,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    assert isinstance(result.top_slices, tuple)
    with pytest.raises(AttributeError):
        result.top_slices.append(sample_slice)  # type: ignore[attr-defined]


def test_top_summaries_is_mapping_proxy(
    classification_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="error_label",
        response_name="__pycatdap_error_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    with pytest.raises(TypeError):
        result.top_summaries["sex"] = sample_target_summary  # type: ignore[index]


# ---------- ErrorAnalysisResult: regression path ----------


def test_regression_result_basic_construction(
    regression_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    pooling_dict = {"bin_0": (-3.0, -1.0), "bin_1": (-1.0, 1.0), "bin_2": (1.0, 3.0)}
    result = ErrorAnalysisResult(
        task="regression",
        label_kind="residual_label",
        response_name="__pycatdap_residual_label__",
        feature_ranking=regression_ranking,
        top_summaries=MappingProxyType({"x1": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling=pooling_dict,
        n_rows=200,
        n_correct=None,
        n_incorrect=None,
        mae=0.85,
        rmse=1.12,
    )
    assert result.task == "regression"
    assert result.label_kind == "residual_label"
    assert result.confusion is None
    assert result.mae == pytest.approx(0.85)
    assert result.rmse == pytest.approx(1.12)


def test_residual_pooling_is_wrapped_in_mapping_proxy(
    regression_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    pooling_dict = {"bin_0": (-3.0, 0.0), "bin_1": (0.0, 3.0)}
    result = ErrorAnalysisResult(
        task="regression",
        label_kind="residual_label",
        response_name="__pycatdap_residual_label__",
        feature_ranking=regression_ranking,
        top_summaries=MappingProxyType({"x1": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling=pooling_dict,
        n_rows=200,
        n_correct=None,
        n_incorrect=None,
        mae=0.85,
        rmse=1.12,
    )
    assert isinstance(result.residual_pooling, MappingProxyType)
    with pytest.raises(TypeError):
        result.residual_pooling["bin_2"] = (3.0, 5.0)  # type: ignore[index]


# ---------- show() smoke test ----------


def test_show_classification_does_not_crash(
    classification_ranking: pd.DataFrame,
    classification_confusion: pd.DataFrame,
    sample_target_summary: TargetSummary,
    sample_slice: Slice,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = ErrorAnalysisResult(
        task="classification",
        label_kind="confusion_label",
        response_name="__pycatdap_confusion_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(sample_slice,),
        confusion=classification_confusion,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    result.show()
    captured = capsys.readouterr()
    # Header content should reach stdout regardless of IPython presence.
    assert "ErrorAnalysisResult" in captured.out or "task" in captured.out.lower()


def test_show_regression_does_not_crash(
    regression_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = ErrorAnalysisResult(
        task="regression",
        label_kind="residual_label",
        response_name="__pycatdap_residual_label__",
        feature_ranking=regression_ranking,
        top_summaries=MappingProxyType({"x1": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling={"bin_0": (-1.0, 1.0)},
        n_rows=200,
        n_correct=None,
        n_incorrect=None,
        mae=0.5,
        rmse=0.7,
    )
    result.show()
    captured = capsys.readouterr()
    assert "ErrorAnalysisResult" in captured.out or "task" in captured.out.lower()


# ---------- to_dict smoke test ----------


def test_to_dict_classification_is_json_safe(
    classification_ranking: pd.DataFrame,
    classification_confusion: pd.DataFrame,
    sample_target_summary: TargetSummary,
    sample_slice: Slice,
) -> None:
    import json

    result = ErrorAnalysisResult(
        task="classification",
        label_kind="confusion_label",
        response_name="__pycatdap_confusion_label__",
        feature_ranking=classification_ranking,
        top_summaries=MappingProxyType({"age": sample_target_summary}),
        top_slices=(sample_slice,),
        confusion=classification_confusion,
        residual_pooling=None,
        n_rows=100,
        n_correct=85,
        n_incorrect=15,
        mae=None,
        rmse=None,
    )
    d = result.to_dict()
    json_str = json.dumps(d)  # must serialise without TypeError
    assert "classification" in json_str
    assert "confusion_label" in json_str
    assert "feature_ranking" in d
    assert "top_slices" in d


def test_to_dict_regression_is_json_safe(
    regression_ranking: pd.DataFrame,
    sample_target_summary: TargetSummary,
) -> None:
    import json

    result = ErrorAnalysisResult(
        task="regression",
        label_kind="residual_label",
        response_name="__pycatdap_residual_label__",
        feature_ranking=regression_ranking,
        top_summaries=MappingProxyType({"x1": sample_target_summary}),
        top_slices=(),
        confusion=None,
        residual_pooling={"bin_0": [-1.0, 1.0]},
        n_rows=200,
        n_correct=None,
        n_incorrect=None,
        mae=0.5,
        rmse=0.7,
    )
    d = result.to_dict()
    json.dumps(d)
    assert d["task"] == "regression"
    assert d["mae"] == pytest.approx(0.5)
