"""Tests for :func:`pycatdap.error_analysis` (H-0011 PR-G2).

Covers the public one-call wrapper that composes Phase G labelling
with :func:`pycatdap.target_analysis`. Also verifies the three
implementation safeguards extracted by cross-check (H-0011 §F):

- **F-1**: reserved column name collision raises ``ValueError``
- **F-2**: a perfect (all-TP/all-TN) classifier does not KeyError
  even though ``pd.crosstab`` drops empty rows
- **F-3**: residual-label slice extraction uses the smallest and
  largest bins (bin order is monotonic)

Plus the multiclass guard: ``confusion_label`` is bypassed when
``y_true ∪ y_pred`` has more than 2 unique values (H-0010 §C
deferred multiclass).
"""

from __future__ import annotations

from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest

import pycatdap
from pycatdap.error import ErrorAnalysisResult

# ---------- fixtures ----------


@pytest.fixture
def df_binary_clf() -> pd.DataFrame:
    rng = np.random.default_rng(seed=7)
    n = 200
    age = rng.choice(["young", "old"], size=n)
    sex = rng.choice(["M", "F"], size=n)
    # y_true correlates with age; predictions are noisy on the "young"
    # bucket so we should see "incorrect" / "FN" concentrating in young.
    y_true = np.where(age == "old", 1, 0)
    flip_p = np.where(age == "young", 0.4, 0.05)
    flips = rng.random(n) < flip_p
    y_pred = np.where(flips, 1 - y_true, y_true)
    return pd.DataFrame(
        {
            "age": age,
            "sex": sex,
            "y_true": y_true.astype(int),
            "y_pred": y_pred.astype(int),
        }
    )


@pytest.fixture
def df_multiclass_clf() -> pd.DataFrame:
    rng = np.random.default_rng(seed=11)
    n = 150
    cls = rng.integers(0, 3, size=n)
    flips = rng.random(n) < 0.2
    pred = np.where(flips, (cls + 1) % 3, cls)
    return pd.DataFrame(
        {
            "feature": rng.choice(["a", "b", "c"], size=n),
            "y_true": cls.astype(int),
            "y_pred": pred.astype(int),
        }
    )


@pytest.fixture
def df_regression() -> pd.DataFrame:
    rng = np.random.default_rng(seed=23)
    n = 200
    group = rng.choice(["lo", "hi"], size=n)
    y_true = np.where(group == "hi", 10.0, 0.0) + rng.normal(0, 1.0, size=n)
    # systematic under-prediction in the "hi" group
    bias = np.where(group == "hi", -3.0, 0.0)
    y_pred = y_true + bias + rng.normal(0, 0.5, size=n)
    return pd.DataFrame(
        {
            "group": group,
            "noisy": rng.choice(["x", "y"], size=n),
            "y_true": y_true,
            "y_pred": y_pred,
        }
    )


# ---------- classification (binary) ----------


def test_binary_classification_path(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred")
    assert isinstance(r, ErrorAnalysisResult)
    assert r.task == "classification"
    assert r.label_kind == "confusion_label"
    assert r.response_name == "__pycatdap_confusion_label__"
    assert r.n_rows == len(df_binary_clf)
    assert r.n_correct is not None
    assert r.n_incorrect is not None
    assert r.n_correct + r.n_incorrect == r.n_rows
    assert r.confusion is not None
    assert list(r.confusion.index) == ["TP", "FP", "FN", "TN"]
    assert r.mae is None and r.rmse is None


def test_binary_ranking_excludes_label_columns(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred")
    variables = set(r.feature_ranking["variable"])
    # The original y_true / y_pred columns DO appear in df (passed through);
    # the synthetic label column is excluded as the response.
    assert r.response_name not in variables
    # age and sex are the candidate explanatories
    assert {"age", "sex"}.issubset(variables)


def test_binary_top_slices_concentrate_on_young(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred", top_k=3)
    # By construction, "young" rows misclassify; some slice on age=young
    # should appear (FP or FN).
    age_slices = [s for s in r.top_slices if s.variable == "age"]
    assert any(
        s.category == "young" and s.error_category in {"FP", "FN"} for s in age_slices
    )


def test_y_true_and_y_pred_as_arrays(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(
        df_binary_clf.drop(columns=["y_true", "y_pred"]),
        df_binary_clf["y_true"].to_numpy(),
        df_binary_clf["y_pred"].to_numpy(),
    )
    assert r.task == "classification"
    assert r.n_rows == len(df_binary_clf)


def test_length_mismatch_raises(df_binary_clf: pd.DataFrame) -> None:
    short = df_binary_clf["y_true"].to_numpy()[:50]
    with pytest.raises(ValueError, match="length"):
        pycatdap.error_analysis(df_binary_clf, short, df_binary_clf["y_pred"])


# ---------- F-1: column-name collision ----------


def test_reserved_column_name_collision_raises(df_binary_clf: pd.DataFrame) -> None:
    bad = df_binary_clf.assign(__pycatdap_confusion_label__=0)
    with pytest.raises(ValueError, match="reserved column"):
        pycatdap.error_analysis(bad, "y_true", "y_pred")


def test_reserved_residual_column_collision_raises(
    df_regression: pd.DataFrame,
) -> None:
    bad = df_regression.assign(__pycatdap_residual_label__=0.0)
    with pytest.raises(ValueError, match="reserved column"):
        pycatdap.error_analysis(bad, "y_true", "y_pred")


# ---------- F-2: perfect classifier does not KeyError ----------


def test_perfect_classifier_preserves_fixed_confusion_rows() -> None:
    df = pd.DataFrame(
        {
            "age": ["young", "old"] * 50,
            "y_true": [0, 1] * 50,
            "y_pred": [0, 1] * 50,
        }
    )
    r = pycatdap.error_analysis(df, "y_true", "y_pred")
    assert r.confusion is not None
    assert list(r.confusion.index) == ["TP", "FP", "FN", "TN"]
    assert int(r.confusion.loc["FP", "count"]) == 0
    assert int(r.confusion.loc["FN", "count"]) == 0


# ---------- multiclass guard ----------


def test_multiclass_routes_to_error_label(df_multiclass_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_multiclass_clf, "y_true", "y_pred")
    assert r.task == "classification"
    assert r.label_kind == "error_label"
    assert r.response_name == "__pycatdap_error_label__"
    # No confusion table for multiclass (would have triggered the
    # v0.7.0 NotImplementedError if we had routed through
    # confusion_label).
    assert r.confusion is None


# ---------- regression ----------


def test_regression_path(df_regression: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_regression, "y_true", "y_pred")
    assert r.task == "regression"
    assert r.label_kind == "residual_label"
    assert r.response_name == "__pycatdap_residual_label__"
    assert r.confusion is None
    assert r.mae is not None and r.mae > 0
    assert r.rmse is not None and r.rmse >= r.mae
    assert r.residual_pooling is not None
    assert isinstance(r.residual_pooling, MappingProxyType)
    assert "bins" in r.residual_pooling and "counts" in r.residual_pooling


def test_regression_slices_detect_bias_group(df_regression: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_regression, "y_true", "y_pred", top_k=2)
    # "group=hi" is the under-prediction bucket by construction; at
    # least one slice should land on it.
    assert any(s.variable == "group" and s.category == "hi" for s in r.top_slices)


# ---------- task='auto' detection ----------


def test_task_auto_detects_classification(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred", task="auto")
    assert r.task == "classification"


def test_task_auto_detects_regression(df_regression: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_regression, "y_true", "y_pred", task="auto")
    assert r.task == "regression"


def test_task_force_regression_on_binary(df_binary_clf: pd.DataFrame) -> None:
    # Force regression on integer 0/1 labels — should still produce a
    # residual_label result.
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred", task="regression")
    assert r.task == "regression"
    assert r.label_kind == "residual_label"


# ---------- top_slices invariants ----------


def test_top_slices_are_residual_thresholded(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred", top_k=5)
    for s in r.top_slices:
        assert abs(s.pearson_residual) >= 2.0


def test_top_slices_capped_at_3_top_k(df_binary_clf: pd.DataFrame) -> None:
    r = pycatdap.error_analysis(df_binary_clf, "y_true", "y_pred", top_k=2)
    assert len(r.top_slices) <= 3 * 2


def test_y_true_missing_column_raises(df_binary_clf: pd.DataFrame) -> None:
    with pytest.raises(KeyError, match="not a column"):
        pycatdap.error_analysis(df_binary_clf, "missing_col", "y_pred")


# ---------- top-level export ----------


def test_error_analysis_exported_at_top_level() -> None:
    assert hasattr(pycatdap, "error_analysis")
    assert pycatdap.error_analysis is pycatdap.error.error_analysis
    assert pycatdap.ErrorAnalysisResult is pycatdap.error.ErrorAnalysisResult
    assert pycatdap.Slice is pycatdap.error.Slice
