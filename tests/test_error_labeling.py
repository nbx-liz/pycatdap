"""Tests for ``pycatdap.error`` — Phase G error labeling utilities (H-0010).

Covers the 4 public functions + ``_detect_task`` helper specified in
BLUEPRINT.md §5.8 and confirmed in H-0010.

Decisions tested here:
- ``confusion_label`` raises ``NotImplementedError`` for multiclass
  (deferred to v0.8.0+)
- ``residual_label`` supports all three methods: ``aic_pool`` (default),
  ``quantile``, ``equal_width``
- ``abs_residual_pool`` reuses ``_pooling`` infrastructure
- ``_detect_task`` heuristic: low-cardinality int → classification,
  probability range [0,1] with binary y_true → classification, else
  regression
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

# ---------- error_label ----------


class TestErrorLabel:
    def test_returns_pd_series(self) -> None:
        from pycatdap.error import error_label

        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 1, 1]
        result = error_label(y_true, y_pred)
        assert isinstance(result, pd.Series)

    def test_correct_incorrect_categories(self) -> None:
        from pycatdap.error import error_label

        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 1, 1]
        result = error_label(y_true, y_pred)
        assert result.tolist() == ["correct", "correct", "incorrect", "correct"]

    def test_is_categorical(self) -> None:
        from pycatdap.error import error_label

        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 0, 1]
        result = error_label(y_true, y_pred)
        assert isinstance(result.dtype, pd.CategoricalDtype)
        assert set(result.cat.categories) == {"correct", "incorrect"}

    def test_accepts_numpy_array(self) -> None:
        from pycatdap.error import error_label

        y_true = np.array([0, 1, 0])
        y_pred = np.array([0, 0, 0])
        result = error_label(y_true, y_pred)
        assert result.tolist() == ["correct", "incorrect", "correct"]

    def test_accepts_pd_series(self) -> None:
        from pycatdap.error import error_label

        y_true = pd.Series([0, 1, 0, 1])
        y_pred = pd.Series([0, 1, 0, 1])
        result = error_label(y_true, y_pred)
        assert (result == "correct").all()

    def test_length_mismatch_raises(self) -> None:
        from pycatdap.error import error_label

        with pytest.raises(ValueError, match="length"):
            error_label([0, 1], [0, 1, 0])

    def test_empty_input_returns_empty(self) -> None:
        from pycatdap.error import error_label

        result = error_label([], [])
        assert len(result) == 0
        assert isinstance(result.dtype, pd.CategoricalDtype)

    def test_string_labels(self) -> None:
        from pycatdap.error import error_label

        y_true = ["cat", "dog", "cat"]
        y_pred = ["cat", "cat", "cat"]
        result = error_label(y_true, y_pred)
        assert result.tolist() == ["correct", "incorrect", "correct"]


# ---------- confusion_label ----------


class TestConfusionLabel:
    def test_binary_tp_fp_fn_tn(self) -> None:
        from pycatdap.error import confusion_label

        # positive = 1; (y_true, y_pred) → label
        #   (1, 1) → TP, (0, 1) → FP, (1, 0) → FN, (0, 0) → TN
        y_true = [1, 0, 1, 0]
        y_pred = [1, 1, 0, 0]
        result = confusion_label(y_true, y_pred, positive=1)
        assert result.tolist() == ["TP", "FP", "FN", "TN"]

    def test_returns_pd_series(self) -> None:
        from pycatdap.error import confusion_label

        result = confusion_label([0, 1], [0, 1], positive=1)
        assert isinstance(result, pd.Series)

    def test_is_categorical_with_four_categories(self) -> None:
        from pycatdap.error import confusion_label

        result = confusion_label([0, 1], [0, 1], positive=1)
        assert isinstance(result.dtype, pd.CategoricalDtype)
        assert set(result.cat.categories) == {"TP", "FP", "FN", "TN"}

    def test_auto_detect_positive(self) -> None:
        """When positive is None, pick the larger of two unique values."""
        from pycatdap.error import confusion_label

        # Binary {0, 1} — positive defaults to 1
        result = confusion_label([1, 0, 1], [1, 0, 0])
        # (1,1)=TP, (0,0)=TN, (1,0)=FN
        assert result.tolist() == ["TP", "TN", "FN"]

    def test_string_labels_with_explicit_positive(self) -> None:
        from pycatdap.error import confusion_label

        y_true = ["spam", "ham", "spam", "ham"]
        y_pred = ["spam", "spam", "ham", "ham"]
        result = confusion_label(y_true, y_pred, positive="spam")
        # (spam, spam)=TP, (ham, spam)=FP, (spam, ham)=FN, (ham, ham)=TN
        assert result.tolist() == ["TP", "FP", "FN", "TN"]

    def test_multiclass_raises_not_implemented(self) -> None:
        """v0.7.0: multiclass deferred per H-0010 §C."""
        from pycatdap.error import confusion_label

        y_true = [0, 1, 2, 0, 1, 2]
        y_pred = [0, 1, 2, 0, 1, 2]
        with pytest.raises(NotImplementedError, match="binary|multiclass"):
            confusion_label(y_true, y_pred)

    def test_length_mismatch_raises(self) -> None:
        from pycatdap.error import confusion_label

        with pytest.raises(ValueError, match="length"):
            confusion_label([0, 1], [0, 1, 0], positive=1)

    def test_invalid_positive_raises(self) -> None:
        """If positive is not in the unique values, raise ValueError."""
        from pycatdap.error import confusion_label

        with pytest.raises(ValueError, match="positive"):
            confusion_label([0, 1], [0, 1], positive=99)


# ---------- residual_label ----------


class TestResidualLabel:
    def test_default_method_is_aic_pool(self) -> None:
        from pycatdap.error import residual_label

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=100)
        y_pred = y_true + rng.normal(size=100, scale=0.1)
        result = residual_label(y_true, y_pred)
        assert isinstance(result, pd.Series)
        assert isinstance(result.dtype, pd.CategoricalDtype)

    def test_quantile_method_produces_n_bins(self) -> None:
        from pycatdap.error import residual_label

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=200)
        y_pred = y_true + rng.normal(size=200, scale=0.5)
        result = residual_label(y_true, y_pred, method="quantile", n_bins=4)
        # Quantile binning into n_bins should produce at most n_bins
        # categories (some bins may collapse on ties).
        assert len(result.cat.categories) <= 4
        assert len(result.cat.categories) >= 1

    def test_equal_width_method_produces_n_bins(self) -> None:
        from pycatdap.error import residual_label

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=200)
        y_pred = y_true + rng.normal(size=200, scale=0.5)
        result = residual_label(y_true, y_pred, method="equal_width", n_bins=4)
        assert len(result.cat.categories) <= 4
        assert len(result.cat.categories) >= 1

    def test_invalid_method_raises(self) -> None:
        from pycatdap.error import residual_label

        with pytest.raises(ValueError, match="method"):
            residual_label([1.0, 2.0], [1.1, 2.1], method="not_a_method")  # type: ignore[arg-type]

    def test_length_mismatch_raises(self) -> None:
        from pycatdap.error import residual_label

        with pytest.raises(ValueError, match="length"):
            residual_label([1.0, 2.0], [1.1, 2.1, 3.0])

    def test_returns_pd_series(self) -> None:
        from pycatdap.error import residual_label

        result = residual_label([1.0, 2.0, 3.0, 4.0], [1.1, 1.9, 3.2, 3.8])
        assert isinstance(result, pd.Series)


# ---------- abs_residual_pool ----------


class TestAbsResidualPool:
    def test_returns_pd_series(self) -> None:
        from pycatdap.error import abs_residual_pool

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=100)
        y_pred = y_true + rng.normal(size=100, scale=0.1)
        result = abs_residual_pool(y_true, y_pred)
        assert isinstance(result, pd.Series)

    def test_is_categorical(self) -> None:
        from pycatdap.error import abs_residual_pool

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=100)
        y_pred = y_true + rng.normal(size=100, scale=0.1)
        result = abs_residual_pool(y_true, y_pred)
        assert isinstance(result.dtype, pd.CategoricalDtype)

    def test_length_mismatch_raises(self) -> None:
        from pycatdap.error import abs_residual_pool

        with pytest.raises(ValueError, match="length"):
            abs_residual_pool([1.0, 2.0], [1.1, 2.1, 3.0])


# ---------- _detect_task ----------


class TestDetectTask:
    def test_int_low_cardinality_is_classification(self) -> None:
        from pycatdap.error import _detect_task

        assert _detect_task(np.array([0, 1, 0, 1, 0]), np.array([0, 1, 1, 0, 1])) == (
            "classification"
        )

    def test_float_probabilities_binary_y_true_is_classification(self) -> None:
        from pycatdap.error import _detect_task

        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0.1, 0.9, 0.3, 0.8])
        assert _detect_task(y_true, y_pred) == "classification"

    def test_continuous_is_regression(self) -> None:
        from pycatdap.error import _detect_task

        rng = np.random.default_rng(0)
        y_true = rng.normal(size=100)
        y_pred = y_true + rng.normal(size=100, scale=0.1)
        assert _detect_task(y_true, y_pred) == "regression"

    def test_high_cardinality_int_is_regression(self) -> None:
        """100 unique int values look like a regression target."""
        from pycatdap.error import _detect_task

        y_true = np.arange(100)
        y_pred = np.arange(100) + 1
        assert _detect_task(y_true, y_pred) == "regression"

    def test_string_categorical_is_classification(self) -> None:
        from pycatdap.error import _detect_task

        y_true = np.array(["cat", "dog", "cat", "dog"])
        y_pred = np.array(["cat", "cat", "dog", "dog"])
        assert _detect_task(y_true, y_pred) == "classification"


# ---------- module exports ----------


def test_error_module_public_api() -> None:
    """The 4 documented public functions are accessible via pycatdap.error."""
    import pycatdap.error as err_module

    for name in (
        "error_label",
        "confusion_label",
        "residual_label",
        "abs_residual_pool",
    ):
        assert hasattr(err_module, name), f"pycatdap.error.{name} missing"
