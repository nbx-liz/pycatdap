"""Phase H result containers (H-0011 PR-G1).

Defines :class:`Slice` and :class:`ErrorAnalysisResult`, the data
classes returned by :func:`pycatdap.error_analysis` (Phase H, v0.8.0).

Both apply the v0.6.1 H-0009 immutable pattern from day 1:

- ``@dataclass(frozen=True)`` blocks attribute reassignment
- ``ErrorAnalysisResult.__post_init__`` freezes the underlying numpy
  buffers of ``feature_ranking`` and ``confusion`` (when present)
- ``top_slices`` is declared as ``tuple[Slice, ...]`` (no ``list``)
- ``top_summaries`` is declared as ``Mapping`` and expected to be a
  ``types.MappingProxyType`` (no ``dict``)
- ``residual_pooling`` is normalised to ``MappingProxyType`` inside
  ``__post_init__`` so user-supplied ``dict`` inputs are not held by
  reference

The ``error_analysis()`` wrapper that actually constructs these objects
lands in PR-G2; PR-G1 only contracts the dataclasses and their
serialisation helpers.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal

import numpy as np
import pandas as pd

from pycatdap._target_pair import RegressionTargetSummary, TargetSummary


@dataclass(frozen=True)
class Slice:
    """A single (variable, category) cell where one error category is
    disproportionately concentrated.

    Phase H surfaces single-variable slices only; multivariable subgroup
    discovery is the responsibility of Phase L
    (``discover_error_slices``).

    Attributes
    ----------
    variable : str
        Explanatory variable name.
    category : str
        The specific value (or bin label) of ``variable`` that this
        slice describes — e.g. ``"young"`` or ``"[45.0, 60.0)"``.
    error_category : str
        The error-label category that is concentrated here. One of
        ``"incorrect"`` (from ``error_label``), ``"FP" / "FN"`` (from
        ``confusion_label``), or a bin label such as ``"bin_3"`` (from
        ``residual_label``).
    n_in_slice : int
        Total number of rows in this slice.
    n_error_in_slice : int
        Of which, how many fall under ``error_category``.
    error_rate : float
        ``n_error_in_slice / n_in_slice``.
    pearson_residual : float
        Standardised residual of the contingency cell. ``|residual| > 2``
        flags a statistically meaningful concentration.
    delta_aic : float
        ΔAIC of the parent variable against the label column. Shared by
        all slices on the same variable.
    """

    variable: str
    category: str
    error_category: str
    n_in_slice: int
    n_error_in_slice: int
    error_rate: float
    pearson_residual: float
    delta_aic: float


@dataclass(frozen=True)
class ErrorAnalysisResult:
    """Result container for :func:`pycatdap.error_analysis` (H-0011).

    Mirrors the immutability discipline established by
    :class:`pycatdap.TargetAnalysisResult` (H-0009): every container
    field is locked down at construction time so downstream code cannot
    silently mutate the result.

    Attributes
    ----------
    task : {"classification", "regression"}
        The task auto-detected by ``_detect_task`` or supplied by the
        caller via ``task=``.
    label_kind : {"error_label", "confusion_label", "residual_label"}
        Which Phase G labeller produced the synthetic response column.
    response_name : str
        Name of the synthetic label column injected into ``df`` before
        the internal ``target_analysis()`` call.
    feature_ranking : pd.DataFrame
        Columns ``variable / delta_aic / kind / n_obs``. Read-only since
        construction (numpy buffer frozen in ``__post_init__``).
    top_summaries : Mapping[str, TargetSummary | RegressionTargetSummary]
        Per-variable :class:`TargetSummary` for the top-K most
        informative explanatories. Wrapped in
        :class:`types.MappingProxyType`.
    top_slices : tuple[Slice, ...]
        Single-variable slices where one error category concentrates
        with ``|pearson_residual| >= 2.0``, sorted descending by
        magnitude. Capped at ``3 * top_k`` entries.
    confusion : pd.DataFrame or None
        Binary classification only. Cross-tab of ``confusion_label``
        rows × explanatory categories of the top-1 variable, reindexed
        to a fixed ``["TP", "FP", "FN", "TN"]`` row order. Numpy buffer
        frozen.
    residual_pooling : Mapping[str, Any] or None
        Regression only. Maps ``bin_<i>`` to ``(low, high)`` boundary
        tuples derived from the AIC-pooled residual binning. Wrapped in
        :class:`types.MappingProxyType` regardless of input type.
    n_rows : int
        Number of rows in the analysed frame.
    n_correct, n_incorrect : int or None
        Classification only.
    mae, rmse : float or None
        Regression only.
    """

    task: Literal["classification", "regression"]
    label_kind: Literal["error_label", "confusion_label", "residual_label"]
    response_name: str
    feature_ranking: pd.DataFrame = field(repr=False)
    top_summaries: Mapping[str, TargetSummary | RegressionTargetSummary] = field(
        repr=False
    )
    top_slices: tuple[Slice, ...] = field(repr=False)
    confusion: pd.DataFrame | None = field(repr=False)
    residual_pooling: Mapping[str, Any] | None = field(repr=False)
    n_rows: int
    n_correct: int | None
    n_incorrect: int | None
    mae: float | None
    rmse: float | None

    def __post_init__(self) -> None:
        # Freeze the numpy buffers of the contained DataFrames so
        # downstream `.values[i] = ...` mutations raise rather than
        # silently corrupting the result. DataFrame-level operations
        # (drop / assign) still allocate new buffers and remain allowed
        # — documented as "read-only" in the field docstrings.
        for col in self.feature_ranking.columns:
            values = self.feature_ranking[col].values
            if isinstance(values, np.ndarray):
                values.flags.writeable = False

        if self.confusion is not None:
            for col in self.confusion.columns:
                values = self.confusion[col].values
                if isinstance(values, np.ndarray):
                    values.flags.writeable = False

        # Normalise residual_pooling to MappingProxyType so a caller
        # who passes a raw dict cannot keep mutating it after handover.
        if self.residual_pooling is not None and not isinstance(
            self.residual_pooling, MappingProxyType
        ):
            object.__setattr__(
                self,
                "residual_pooling",
                MappingProxyType(dict(self.residual_pooling)),
            )

    # ------------------------------------------------------------------
    # show()
    # ------------------------------------------------------------------

    def show(self) -> None:
        """Render a textual or notebook summary of the result."""
        header = (
            f"ErrorAnalysisResult — task={self.task!r}, "
            f"label_kind={self.label_kind!r}, n_rows={self.n_rows}"
        )
        if self.task == "classification":
            header += f", correct={self.n_correct}, incorrect={self.n_incorrect}"
        elif self.task == "regression":
            mae_str = f"{self.mae:.4f}" if self.mae is not None else "n/a"
            rmse_str = f"{self.rmse:.4f}" if self.rmse is not None else "n/a"
            header += f", MAE={mae_str}, RMSE={rmse_str}"

        try:
            from IPython.display import display
        except ImportError:
            print(header)
            print()
            if self.confusion is not None:
                print("Confusion:")
                print(self.confusion.to_string())
                print()
            print("Feature ranking:")
            print(self.feature_ranking.to_string(index=False))
            if self.top_slices:
                print()
                print("Top slices:")
                for s in self.top_slices:
                    print(
                        f"  {s.variable}={s.category} "
                        f"[{s.error_category}]: rate={s.error_rate:.3f}, "
                        f"residual={s.pearson_residual:+.2f}"
                    )
            return

        print(header)
        if self.confusion is not None:
            display("--- Confusion ---")
            display(self.confusion)
        display("--- Feature ranking ---")
        display(self.feature_ranking)
        if self.top_slices:
            display("--- Top slices ---")
            display(pd.DataFrame([s.__dict__ for s in self.top_slices]))
        for col, summary in self.top_summaries.items():
            display(f"--- top: {col} (ΔAIC = {summary.delta_aic:.4f}) ---")
            summary.show()

    # ------------------------------------------------------------------
    # to_dict()
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation."""
        return {
            "task": self.task,
            "label_kind": self.label_kind,
            "response_name": self.response_name,
            "n_rows": self.n_rows,
            "n_correct": self.n_correct,
            "n_incorrect": self.n_incorrect,
            "mae": self.mae,
            "rmse": self.rmse,
            "feature_ranking": _ranking_to_records(self.feature_ranking),
            "top_slices": [_slice_to_dict(s) for s in self.top_slices],
            "confusion": (
                _confusion_to_records(self.confusion)
                if self.confusion is not None
                else None
            ),
            "residual_pooling": (
                {k: list(v) for k, v in self.residual_pooling.items()}
                if self.residual_pooling is not None
                else None
            ),
            "top_summaries": {
                col: summary.to_dict() for col, summary in self.top_summaries.items()
            },
        }


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _ranking_to_records(ranking: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "variable": str(rec["variable"]),
            "delta_aic": float(rec["delta_aic"]),
            "kind": str(rec["kind"]),
            "n_obs": int(rec["n_obs"]),
        }
        for rec in ranking.to_dict("records")
    ]


def _confusion_to_records(confusion: pd.DataFrame) -> dict[str, dict[str, int]]:
    return {
        str(row): {str(col): int(confusion.loc[row, col]) for col in confusion.columns}
        for row in confusion.index
    }


def _slice_to_dict(s: Slice) -> dict[str, Any]:
    return {
        "variable": s.variable,
        "category": s.category,
        "error_category": s.error_category,
        "n_in_slice": int(s.n_in_slice),
        "n_error_in_slice": int(s.n_error_in_slice),
        "error_rate": float(s.error_rate),
        "pearson_residual": float(s.pearson_residual),
        "delta_aic": float(s.delta_aic),
    }


__all__ = ["ErrorAnalysisResult", "Slice"]
