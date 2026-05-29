"""Phase H one-call wrapper :func:`error_analysis` (H-0011 PR-G2).

Composes Phase G labelling (H-0010) with :func:`pycatdap.target_analysis`
(H-0008) into a single ML-error-analysis entry point:

```
_detect_task → label_fn → target_analysis(label_col) → ErrorAnalysisResult
```

Single-variable slice extraction is performed locally; multivariable
subgroup discovery is reserved for Phase L (Issue #20).

Implementation safeguards from cross-check 2026-05-28
(H-0011 §F):

- **F-1 column collision**: the synthetic label column name
  (``__pycatdap_error_label__`` etc.) must not exist in the input frame
- **F-2 FP/FN row absence**: ``pd.crosstab`` drops empty rows, so a
  perfect model produces a confusion table without the ``"FP"`` / ``"FN"``
  rows; we ``reindex`` to a fixed 4-row order and ``fillna(0.0)``
- **F-3 bin ordering**: ``equal_pooling`` boundaries are sorted
  ascending so ``bin_0`` is the under-prediction bin and ``bin_{n-1}``
  the over-prediction bin
"""

from __future__ import annotations

from collections.abc import Sequence
from types import MappingProxyType
from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import pandas as pd

from pycatdap._target_pair import TargetSummary
from pycatdap.error._labels import (
    _detect_task,
    confusion_label,
    error_label,
    residual_label,
)
from pycatdap.error._result import ErrorAnalysisResult, Slice
from pycatdap.target_analysis import target_analysis

_RESERVED_LABEL_NAMES = (
    "__pycatdap_error_label__",
    "__pycatdap_confusion_label__",
    "__pycatdap_residual_label__",
)

_RESIDUAL_THRESHOLD = 2.0


def error_analysis(
    df: pd.DataFrame,
    y_true: str | pd.Series | npt.NDArray[Any] | Sequence[Any],
    y_pred: str | pd.Series | npt.NDArray[Any] | Sequence[Any],
    *,
    task: Literal["auto", "classification", "regression"] = "auto",
    top_k: int = 5,
    positive: Any = None,
    residual_method: Literal["aic_pool", "quantile", "equal_width"] = "aic_pool",
    n_bins: int = 4,
    bins: int | None = None,
    criterion: Literal["aic", "aicc", "bic"] = "bic",
    y_proba: str | pd.Series | npt.NDArray[Any] | Sequence[Any] | None = None,
) -> ErrorAnalysisResult:
    """ML error analysis one-call wrapper.

    Composes Phase G error labelling (:mod:`pycatdap.error`) with
    :func:`pycatdap.target_analysis` to rank explanatory variables by
    how strongly they associate with model error, plus surface single-
    variable slices where one error category concentrates.

    Parameters
    ----------
    df : DataFrame
        Source frame.  All columns except those referenced by string
        ``y_true``/``y_pred`` participate as candidate explanatories.
    y_true, y_pred : str | pd.Series | np.ndarray | Sequence
        Ground-truth and predicted labels.  Either a column name in
        ``df`` or an array of equal length.
    task : {"auto", "classification", "regression"}
        ``"auto"`` calls :func:`pycatdap.error._detect_task`.  Otherwise
        forces the labelling path.
    top_k : int, default 5
        Number of top-ranked variables to retain full
        :class:`TargetSummary` objects for.  Slice extraction also
        searches these top-K variables only.
    positive : any, optional
        Forwarded to :func:`pycatdap.error.confusion_label` (binary
        classification only).
    residual_method, n_bins : passthrough
        Forwarded to :func:`pycatdap.error.residual_label`.
    bins : int or None
        Binning for continuous explanatories, forwarded to
        :func:`pycatdap.target_analysis`.
    criterion : {"aic", "aicc", "bic"}
        Penalty family for the regression AIC path inside
        :func:`pycatdap.target_analysis`.
    y_proba : str | pd.Series | np.ndarray | Sequence | None, optional
        Positive-class probabilities for binary classification.  When
        supplied, retained on the result so
        :meth:`ErrorAnalysisResult.calibration_curve` works (H-0013 Phase
        K).  Either a column name in ``df`` or an array of equal length.

    Returns
    -------
    ErrorAnalysisResult

    Raises
    ------
    ValueError
        If ``df`` already contains a reserved label column name
        (``__pycatdap_error_label__`` etc.) or if array-form ``y_true`` /
        ``y_pred`` does not match ``len(df)``.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> from pycatdap.error import error_label
    >>> df["pred"] = df["Survived"]  # toy: perfect model
    >>> r = pycatdap.error_analysis(df, "Survived", "pred", task="classification")
    >>> r.task
    'classification'
    """
    y_true_arr, y_pred_arr = _resolve_label_arrays(df, y_true, y_pred)
    if len(y_true_arr) != len(df):
        msg = (
            f"y_true / y_pred length ({len(y_true_arr)}) does not match "
            f"len(df) ({len(df)})"
        )
        raise ValueError(msg)

    y_proba_arr: npt.NDArray[Any] | None = None
    if y_proba is not None:
        y_proba_arr = _resolve_one(df, y_proba, "y_proba")
        if len(y_proba_arr) != len(df):
            msg = (
                f"y_proba length ({len(y_proba_arr)}) does not match "
                f"len(df) ({len(df)})"
            )
            raise ValueError(msg)

    resolved_task = _detect_task(y_true_arr, y_pred_arr) if task == "auto" else task

    n_correct: int | None
    n_incorrect: int | None
    mae: float | None
    rmse: float | None
    confusion: pd.DataFrame | None
    residual_pooling: dict[str, Any] | None
    label_kind: Literal["error_label", "confusion_label", "residual_label"]
    response_name: str

    if resolved_task == "classification":
        n_unique = len(np.unique(np.concatenate([y_true_arr, y_pred_arr])))
        # F-2 guard: only call confusion_label for true binary; multiclass
        # is rerouted to error_label so we never trigger the v0.7.0
        # NotImplementedError.
        if n_unique <= 2:
            label_series = confusion_label(y_true_arr, y_pred_arr, positive=positive)
            response_name = "__pycatdap_confusion_label__"
            label_kind = "confusion_label"
        else:
            label_series = error_label(y_true_arr, y_pred_arr)
            response_name = "__pycatdap_error_label__"
            label_kind = "error_label"
        n_correct = int((y_true_arr == y_pred_arr).sum())
        n_incorrect = int(len(y_true_arr) - n_correct)
        mae = None
        rmse = None
    else:
        label_series = residual_label(
            y_true_arr, y_pred_arr, method=residual_method, n_bins=n_bins
        )
        response_name = "__pycatdap_residual_label__"
        label_kind = "residual_label"
        residuals = y_true_arr.astype(np.float64) - y_pred_arr.astype(np.float64)
        n_correct = None
        n_incorrect = None
        mae = float(np.mean(np.abs(residuals)))
        rmse = float(np.sqrt(np.mean(residuals**2)))

    # F-1 guard: refuse to overwrite a pre-existing column.
    if response_name in df.columns:
        msg = (
            f"error_analysis: df already contains reserved column "
            f"{response_name!r}; drop or rename it before calling. "
            f"Reserved names: {_RESERVED_LABEL_NAMES}"
        )
        raise ValueError(msg)

    df_labeled = df.assign(**{response_name: label_series.values})
    ta = target_analysis(
        df_labeled,
        response=response_name,
        top_k=top_k,
        bins=bins,
        criterion=criterion,
    )

    confusion = (
        _build_confusion(label_series, label_kind)
        if resolved_task == "classification" and label_kind == "confusion_label"
        else None
    )

    residual_pooling = (
        _build_residual_pooling(label_series)
        if label_kind == "residual_label"
        else None
    )

    top_slices = _extract_slices(
        ta.top_summaries,
        ranking=ta.ranking,
        label_kind=label_kind,
        top_k=top_k,
    )

    return ErrorAnalysisResult(
        task=resolved_task,
        label_kind=label_kind,
        response_name=response_name,
        feature_ranking=ta.ranking,
        top_summaries=ta.top_summaries,
        top_slices=top_slices,
        confusion=confusion,
        residual_pooling=(
            MappingProxyType(residual_pooling) if residual_pooling is not None else None
        ),
        n_rows=len(df),
        n_correct=n_correct,
        n_incorrect=n_incorrect,
        mae=mae,
        rmse=rmse,
        # H-0012 PR-H3: retain raw labels so result.plot_confusion() /
        # result.residual_plot() can render without round-tripping. The
        # .copy() is a defensive copy so the result's __post_init__
        # freeze doesn't propagate to the caller's array.
        y_true=y_true_arr.copy(),
        y_pred=y_pred_arr.copy(),
        # H-0013 PR-K2: retain positive-class probabilities (when supplied)
        # so result.calibration_curve() can render. Defensive copy mirrors
        # y_true / y_pred above.
        y_proba=y_proba_arr.copy() if y_proba_arr is not None else None,
    )


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _resolve_label_arrays(
    df: pd.DataFrame,
    y_true: str | pd.Series | npt.NDArray[Any] | Sequence[Any],
    y_pred: str | pd.Series | npt.NDArray[Any] | Sequence[Any],
) -> tuple[npt.NDArray[Any], npt.NDArray[Any]]:
    """Normalise y_true / y_pred to numpy arrays, dereferencing column
    names against ``df`` where appropriate."""
    y_true_arr = _resolve_one(df, y_true, "y_true")
    y_pred_arr = _resolve_one(df, y_pred, "y_pred")
    return y_true_arr, y_pred_arr


def _resolve_one(
    df: pd.DataFrame,
    val: str | pd.Series | npt.NDArray[Any] | Sequence[Any],
    role: str,
) -> npt.NDArray[Any]:
    if isinstance(val, str):
        if val not in df.columns:
            msg = f"error_analysis: {role}={val!r} is not a column of df"
            raise KeyError(msg)
        return np.asarray(df[val])
    return np.asarray(val)


def _build_confusion(
    label_series: pd.Series,
    label_kind: str,
) -> pd.DataFrame:
    """Build a fixed-shape confusion summary.

    F-2: ``confusion_label`` declares a fixed 4-category dtype, but
    ``pd.crosstab`` still drops 0-count rows.  We surface a flat 1-column
    table reindexed to the canonical TP/FP/FN/TN order with zeros filled
    in for absent categories.
    """
    counts = label_series.value_counts(dropna=False)
    if label_kind == "confusion_label":
        canonical = ["TP", "FP", "FN", "TN"]
        counts = counts.reindex(canonical).fillna(0).astype(int)
    return counts.to_frame(name="count")


def _build_residual_pooling(label_series: pd.Series) -> dict[str, Any]:
    """Summarise the residual_label bin layout for downstream consumers.

    Reports the per-bin count plus the bin label catalogue. Concrete
    boundary values are intentionally omitted here — the binning is
    AIC-derived inside ``_residual_label_aic_pool`` and the boundaries
    live in the categorical dtype's intermediate state, not on the
    Series itself.
    """
    counts = label_series.value_counts(dropna=False).sort_index()
    return {
        "bins": [str(idx) for idx in counts.index],
        "counts": {str(idx): int(val) for idx, val in counts.items()},
    }


def _extract_slices(
    top_summaries: Any,
    *,
    ranking: pd.DataFrame,
    label_kind: str,
    top_k: int,
) -> tuple[Slice, ...]:
    """Surface single-variable slices where one error category
    concentrates with ``|pearson_residual| >= 2.0``.

    Strategy per ``label_kind``:

    - ``error_label`` → look at the ``"incorrect"`` row only
    - ``confusion_label`` → consider ``"FP"`` and ``"FN"`` rows
    - ``residual_label`` → consider the smallest and largest bin labels
      (F-3 guarantees they are monotonic in residual value)
    """
    target_categories: list[str]
    if label_kind == "error_label":
        target_categories = ["incorrect"]
    elif label_kind == "confusion_label":
        target_categories = ["FP", "FN"]
    else:
        # residual_label: use the extremes of the categorical index
        target_categories = []  # set per-summary below

    delta_aic_map = {
        str(row["variable"]): float(row["delta_aic"]) for _, row in ranking.iterrows()
    }

    candidates: list[Slice] = []
    for var_name, summary in top_summaries.items():
        if not isinstance(summary, TargetSummary):
            continue  # regression target summaries do not expose pearson_residuals
        residuals = summary.pearson_residuals
        counts = summary.counts

        if label_kind == "residual_label":
            cats_in_summary = [str(idx) for idx in residuals.index]
            if len(cats_in_summary) <= 1:
                continue
            target_categories = [cats_in_summary[0], cats_in_summary[-1]]

        for err_cat in target_categories:
            if err_cat not in residuals.index:
                continue
            row_resid = residuals.loc[err_cat]
            row_counts = counts.loc[err_cat]
            col_totals = counts.sum(axis=0)
            for category in row_resid.index:
                resid_val = float(row_resid[category])
                if abs(resid_val) < _RESIDUAL_THRESHOLD:
                    continue
                n_in_slice = int(col_totals.loc[category])
                if n_in_slice == 0:
                    continue
                n_err = int(row_counts.loc[category])
                candidates.append(
                    Slice(
                        variable=var_name,
                        category=str(category),
                        error_category=err_cat,
                        n_in_slice=n_in_slice,
                        n_error_in_slice=n_err,
                        error_rate=n_err / n_in_slice,
                        pearson_residual=resid_val,
                        delta_aic=delta_aic_map.get(var_name, float("nan")),
                    )
                )

    candidates.sort(key=lambda s: abs(s.pearson_residual), reverse=True)
    return tuple(candidates[: 3 * max(top_k, 1)])


__all__ = ["error_analysis"]
