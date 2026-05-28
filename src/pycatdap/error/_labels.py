"""Error labeling utilities (H-0010, Phase G).

All public functions return a ``pd.Series`` with categorical dtype.
No result dataclass is introduced (Phase H introduces those).

Numerical conventions:
- AIC pooling reuses :mod:`pycatdap._pooling`
- Quantile / equal_width binning uses :func:`pandas.qcut` / :func:`pandas.cut`
- The "correct" / "incorrect" comparison uses element-wise equality
  on the underlying numpy array, so it works for any dtype
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd


def _as_arrays(y_true: Any, y_pred: Any) -> tuple[npt.NDArray[Any], npt.NDArray[Any]]:
    """Convert pd.Series / np.ndarray / list to (np.ndarray, np.ndarray).

    Validates equal length. Raises ``ValueError`` on mismatch.
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    if y_true_arr.shape[0] != y_pred_arr.shape[0]:
        msg = (
            f"y_true and y_pred must have the same length "
            f"(got {y_true_arr.shape[0]} and {y_pred_arr.shape[0]})"
        )
        raise ValueError(msg)
    return y_true_arr, y_pred_arr


def _detect_task(
    y_true: npt.NDArray[Any] | pd.Series,
    y_pred: npt.NDArray[Any] | pd.Series,
) -> Literal["classification", "regression"]:
    """Heuristic task detection (H-0010 §D).

    Rules
    -----
    1. Non-numeric (object / string) inputs → ``classification``.
    2. Both arrays integer dtype AND both have <= 20 unique values
       → ``classification``.
    3. ``y_pred`` is float in ``[0, 1]`` AND ``y_true`` has exactly
       2 unique integer-like values → ``classification`` (probability
       prediction against binary truth).
    4. Otherwise → ``regression``.
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)

    # Rule 1: non-numeric → classification
    if y_true_arr.dtype.kind in ("O", "U", "S"):
        return "classification"

    # Rule 2: both integer with low cardinality → classification
    if y_true_arr.dtype.kind in ("i", "u") and y_pred_arr.dtype.kind in ("i", "u"):
        n_unique_true = len(np.unique(y_true_arr))
        n_unique_pred = len(np.unique(y_pred_arr))
        if n_unique_true <= 20 and n_unique_pred <= 20:
            return "classification"

    # Rule 3: probability prediction against binary truth
    if y_pred_arr.dtype.kind == "f":
        finite = y_pred_arr[np.isfinite(y_pred_arr)]
        if len(finite) > 0 and finite.min() >= 0.0 and finite.max() <= 1.0:
            n_unique_true = len(np.unique(y_true_arr))
            if n_unique_true == 2:
                return "classification"

    return "regression"


def error_label(
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
) -> pd.Series:
    """Categorize each prediction as ``"correct"`` or ``"incorrect"``.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted labels. Same length.

    Returns
    -------
    pd.Series
        Categorical Series with categories ``{"correct", "incorrect"}``.
        Even for empty input the categorical dtype is preserved.

    Examples
    --------
    >>> labels = error_label([0, 1, 0, 1], [0, 1, 1, 1])
    >>> labels.tolist()
    ['correct', 'correct', 'incorrect', 'correct']
    """
    y_true_arr, y_pred_arr = _as_arrays(y_true, y_pred)
    correct = y_true_arr == y_pred_arr
    labels = np.where(correct, "correct", "incorrect")
    return pd.Series(
        pd.Categorical(labels, categories=["correct", "incorrect"]),
        name="error_label",
    )


def confusion_label(
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
    *,
    positive: Any = None,
) -> pd.Series:
    """Label each prediction as ``"TP" | "FP" | "FN" | "TN"``.

    Binary classification only in v0.7.0. Multiclass support is
    deferred per H-0010 §C (see ``NotImplementedError`` message for the
    follow-up issue reference).

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted labels.
    positive : any, optional
        The label treated as the positive class. When ``None``, the
        function picks the larger of the two unique values (so
        ``{0, 1}`` defaults to ``positive=1`` and string ``{"ham",
        "spam"}`` defaults to ``positive="spam"``).

    Returns
    -------
    pd.Series
        Categorical Series with categories ``{"TP", "FP", "FN", "TN"}``.

    Raises
    ------
    NotImplementedError
        When ``y_true ∪ y_pred`` has more than 2 unique values.
    ValueError
        When ``positive`` is explicitly given but is not one of the
        unique values, or when the inputs have different lengths.
    """
    y_true_arr, y_pred_arr = _as_arrays(y_true, y_pred)

    # Determine the universe of unique values (across both).
    combined = np.concatenate([y_true_arr, y_pred_arr])
    unique_values = np.unique(combined)

    if len(unique_values) > 2:
        msg = (
            f"confusion_label only supports binary classification in v0.7.0 "
            f"(got {len(unique_values)} unique values). Multiclass "
            f"(one-vs-rest) is deferred to a v0.8.0+ follow-up to Issue #16."
        )
        raise NotImplementedError(msg)

    if positive is None:
        # Pick the larger of the unique values as positive.
        # For {0, 1} → 1; for {"ham", "spam"} → "spam" (lexicographic).
        # When only one unique value exists, take it.
        positive = unique_values[-1] if len(unique_values) >= 1 else None

    if positive not in unique_values.tolist():
        msg = (
            f"positive={positive!r} is not present in y_true or y_pred "
            f"(unique values: {unique_values.tolist()})"
        )
        raise ValueError(msg)

    is_true_pos = y_true_arr == positive
    is_pred_pos = y_pred_arr == positive

    labels = np.empty(len(y_true_arr), dtype=object)
    labels[is_true_pos & is_pred_pos] = "TP"
    labels[~is_true_pos & is_pred_pos] = "FP"
    labels[is_true_pos & ~is_pred_pos] = "FN"
    labels[~is_true_pos & ~is_pred_pos] = "TN"

    return pd.Series(
        pd.Categorical(labels, categories=["TP", "FP", "FN", "TN"]),
        name="confusion_label",
    )


def residual_label(
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
    *,
    method: Literal["aic_pool", "quantile", "equal_width"] = "aic_pool",
    n_bins: int = 4,
) -> pd.Series:
    """Bin regression residuals into categorical labels.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted values (numeric).
    method : {"aic_pool", "quantile", "equal_width"}, default "aic_pool"
        - ``"aic_pool"``: reuse the CATDAP-01 AIC-optimal pooling (see
          :mod:`pycatdap._pooling`). ``n_bins`` is the initial bin count;
          the AIC merge step may collapse it further.
        - ``"quantile"``: ``n_bins`` equal-frequency bins via
          :func:`pandas.qcut`.
        - ``"equal_width"``: ``n_bins`` equal-width bins via
          :func:`pandas.cut`.
    n_bins : int, default 4
        Target number of bins. For ``"aic_pool"`` this is the *initial*
        bin count before AIC-driven merging.

    Returns
    -------
    pd.Series
        Categorical Series whose categories are the bin labels.

    Raises
    ------
    ValueError
        On unknown ``method`` or length mismatch.
    """
    y_true_arr, y_pred_arr = _as_arrays(y_true, y_pred)
    residuals = y_true_arr.astype(np.float64) - y_pred_arr.astype(np.float64)

    if method == "aic_pool":
        return _residual_label_aic_pool(residuals, n_bins=n_bins)
    if method == "quantile":
        labels = pd.qcut(residuals, q=n_bins, duplicates="drop")
        return pd.Series(labels, name="residual_label").astype("category")
    if method == "equal_width":
        labels = pd.cut(residuals, bins=n_bins, duplicates="drop")
        return pd.Series(labels, name="residual_label").astype("category")

    msg = (
        f"unknown method={method!r}; expected one of "
        f"'aic_pool', 'quantile', 'equal_width'"
    )
    raise ValueError(msg)


def _residual_label_aic_pool(
    residuals: npt.NDArray[np.float64],
    *,
    n_bins: int,
) -> pd.Series:
    """AIC-driven binning of residuals.

    Strategy: quantile-bin into ``n_bins`` initial categories, then use
    those categories as the "response" for AIC pooling on the residual
    values themselves. The final categorical labels are the resulting
    bin labels.

    For small inputs where qcut would degenerate, fall back to a single
    bin.
    """
    if len(residuals) == 0:
        return pd.Series(pd.Categorical([]), name="residual_label")

    # Quantile bin labels as the "response".
    try:
        initial = pd.qcut(residuals, q=n_bins, duplicates="drop")
    except ValueError:
        return pd.Series(
            pd.Categorical(["all"] * len(residuals), categories=["all"]),
            name="residual_label",
        )

    from pycatdap._pooling import equal_pooling

    response = np.asarray(initial.astype(str))
    accuracy = (
        float(np.diff(np.sort(np.unique(residuals))).min())
        if len(np.unique(residuals)) > 1
        else 1.0
    )
    accuracy = max(accuracy, 1e-9)
    result = equal_pooling(residuals, response, accuracy=accuracy)

    # Build labels from the pooled bin codes.
    n_codes = int(result.codes.max()) + 1 if len(result.codes) > 0 else 0
    categories = [f"bin_{i}" for i in range(n_codes)]
    labels = np.array([f"bin_{c}" for c in result.codes], dtype=object)
    return pd.Series(
        pd.Categorical(labels, categories=categories),
        name="residual_label",
    )


def abs_residual_pool(
    y_true: pd.Series | npt.NDArray[Any] | list[Any],
    y_pred: pd.Series | npt.NDArray[Any] | list[Any],
    *,
    n_bins: int = 4,
) -> pd.Series:
    """Bin absolute residuals ``|y_true - y_pred|`` via AIC pooling.

    Parameters
    ----------
    y_true, y_pred : array-like
        Aligned ground-truth and predicted numeric values.
    n_bins : int, default 4
        Initial quantile bin count used to seed the AIC pooling.

    Returns
    -------
    pd.Series
        Categorical Series whose labels reflect the AIC-pooled
        absolute-residual bins.
    """
    y_true_arr, y_pred_arr = _as_arrays(y_true, y_pred)
    abs_resid = np.abs(y_true_arr.astype(np.float64) - y_pred_arr.astype(np.float64))
    return _residual_label_aic_pool(abs_resid, n_bins=n_bins)
