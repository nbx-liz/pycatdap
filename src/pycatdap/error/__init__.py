"""Phase G error labeling utilities (H-0010, v0.7.0).

This subpackage converts prediction outputs into categorical labels
suitable for CATDAP analysis. Required by all subsequent ML error
analysis phases (H/I+J/K/L).

The 4 public functions all return ``pd.Series`` with categorical dtype.
No result dataclass is introduced here — Phase H will bundle a
ranking + slice container (``ErrorAnalysisResult``) using the H-0009
immutable pattern.

Public API
----------
- :func:`error_label` — binary "correct" / "incorrect" labels
- :func:`confusion_label` — binary TP / FP / FN / TN labels
- :func:`residual_label` — regression residuals binned (aic_pool /
  quantile / equal_width)
- :func:`abs_residual_pool` — |residual| binned via AIC pooling
- :func:`_detect_task` — heuristic task auto-detection helper

Notes
-----
:func:`confusion_label` raises ``NotImplementedError`` for multiclass
inputs in v0.7.0; one-vs-rest support is deferred per H-0010 §C.
"""

from __future__ import annotations

from pycatdap.error._labels import (
    _detect_task,
    abs_residual_pool,
    confusion_label,
    error_label,
    residual_label,
)
from pycatdap.error._result import ErrorAnalysisResult, Slice
from pycatdap.error.analysis import error_analysis
from pycatdap.error.calibration import (
    brier_score,
    calibration_curve,
    calibration_table,
    expected_calibration_error,
    maximum_calibration_error,
)
from pycatdap.error.confusion import (
    confusion_aic,
    plot_confusion,
    plot_confusion_by_slice,
)
from pycatdap.error.residual import (
    residual_by_category,
    residual_plot,
    residual_pool_plot,
)

__all__ = [
    "ErrorAnalysisResult",
    "Slice",
    "_detect_task",
    "abs_residual_pool",
    "brier_score",
    "calibration_curve",
    "calibration_table",
    "confusion_aic",
    "confusion_label",
    "error_analysis",
    "error_label",
    "expected_calibration_error",
    "maximum_calibration_error",
    "plot_confusion",
    "plot_confusion_by_slice",
    "residual_by_category",
    "residual_label",
    "residual_plot",
    "residual_pool_plot",
]
