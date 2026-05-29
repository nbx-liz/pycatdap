"""Multi-class one-vs-rest confusion labelling (H-0015 PR-M4, design A).

``multiclass_confusion_label`` returns a read-only mapping of class label to a
per-class TP/FP/FN/TN Series, reducing each class to a binary OvR problem and
reusing the existing binary :func:`confusion_label` core.

Invariants under test (see HISTORY.md H-0015 §Invariants):

* INV-1  binary confusion_label unchanged (still raises for >2 classes)
* INV-2  2-class OvR == binary confusion_label(positive=that class)
* INV-3  OvR self-consistency per class (TP/FP/FN/TN definitions)
* INV-4  per-class count conservation; sum_k TP_k == n_correct
* INV-6  read-only mapping; inputs never mutated
"""

from __future__ import annotations

from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest

from pycatdap.error import confusion_label, multiclass_confusion_label


def _mc_data(n: int = 300, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    y_true = rng.integers(0, 3, size=n)
    y_pred = np.where(rng.random(n) < 0.3, rng.integers(0, 3, size=n), y_true)
    return y_true, y_pred


def test_returns_readonly_mapping_per_class() -> None:
    yt, yp = _mc_data()
    result = multiclass_confusion_label(yt, yp)
    assert isinstance(result, MappingProxyType)
    assert sorted(result.keys()) == [0, 1, 2]
    for series in result.values():
        assert set(series.cat.categories) == {"TP", "FP", "FN", "TN"}
        assert len(series) == len(yt)


def test_ovr_self_consistency() -> None:
    """INV-3: per class k, exactly one of TP/FP/FN/TN, matching definitions."""
    yt, yp = _mc_data()
    result = multiclass_confusion_label(yt, yp)
    for k, series in result.items():
        labels = series.to_numpy()
        is_true = yt == k
        is_pred = yp == k
        np.testing.assert_array_equal(labels == "TP", is_true & is_pred)
        np.testing.assert_array_equal(labels == "FP", ~is_true & is_pred)
        np.testing.assert_array_equal(labels == "FN", is_true & ~is_pred)
        np.testing.assert_array_equal(labels == "TN", ~is_true & ~is_pred)


def test_count_conservation() -> None:
    """INV-4: TP+FP+FN+TN == n per class; sum_k TP_k == n_correct."""
    yt, yp = _mc_data()
    result = multiclass_confusion_label(yt, yp)
    n = len(yt)
    total_tp = 0
    for series in result.values():
        counts = series.value_counts()
        assert int(counts.sum()) == n
        total_tp += int(counts.get("TP", 0))
    assert total_tp == int((yt == yp).sum())


def test_two_class_ovr_equals_binary() -> None:
    """INV-2: on a 2-class problem the larger class's OvR == binary."""
    rng = np.random.default_rng(2)
    n = 200
    yt = rng.integers(0, 2, size=n)
    yp = np.where(rng.random(n) < 0.25, 1 - yt, yt)
    result = multiclass_confusion_label(yt, yp)
    binary = confusion_label(yt, yp, positive=1)
    pd.testing.assert_series_equal(
        result[1].reset_index(drop=True),
        binary.reset_index(drop=True),
        check_names=False,
    )


def test_inputs_not_mutated() -> None:
    """INV-6: input arrays untouched."""
    yt, yp = _mc_data(n=120)
    yt_before = yt.copy()
    yp_before = yp.copy()
    multiclass_confusion_label(yt, yp)
    np.testing.assert_array_equal(yt, yt_before)
    np.testing.assert_array_equal(yp, yp_before)


def test_explicit_classes_order() -> None:
    yt, yp = _mc_data()
    result = multiclass_confusion_label(yt, yp, classes=[2, 0, 1])
    assert list(result.keys()) == [2, 0, 1]


def test_string_labels() -> None:
    yt = np.array(["a", "b", "c", "a", "b", "c", "a", "b"])
    yp = np.array(["a", "b", "a", "a", "c", "c", "b", "b"])
    result = multiclass_confusion_label(yt, yp)
    assert sorted(result.keys()) == ["a", "b", "c"]
    # class "a": TP where both a
    a = result["a"].to_numpy()
    np.testing.assert_array_equal(a == "TP", (yt == "a") & (yp == "a"))


def test_binary_confusion_label_still_rejects_multiclass() -> None:
    """INV-1: the binary entry point is unchanged (still raises for >2)."""
    yt, yp = _mc_data(n=60)
    with pytest.raises(NotImplementedError):
        confusion_label(yt, yp)
