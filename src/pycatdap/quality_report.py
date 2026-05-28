"""Focused data-quality scan (H-0008 PR-D2).

Companion to :func:`pycatdap.profile`: shares the same warning logic
via :func:`pycatdap._quality._scan_quality` but skips the heavier
``association_matrix`` / ``catdap2`` passes, so it stays fast on wide
CI datasets and is suitable as a pytest assertion (``assert
qr.passed``).

Returns :class:`QualityReport`, which mirrors the 4-method serialization
contract of :class:`pycatdap.ProfileResult`
(``.show / .to_html / .to_dict / .to_plotly_json``) plus a CI-friendly
``.passed`` property and ``.by_severity / .by_kind`` groupers.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from pycatdap._quality import (
    _DEFAULT_QUALITY_THRESHOLDS,
    QualityWarning,
    _scan_quality,
)
from pycatdap.profile import _build_variables


@dataclass(frozen=True)
class QualityReport:
    """Result of :func:`quality_report`.

    Attributes
    ----------
    warnings : list[QualityWarning]
        Quality findings in column order. Empty when the frame passes
        every default check.
    n_rows, n_cols : int
        Shape of the inspected frame.
    """

    warnings: list[QualityWarning]
    n_rows: int
    n_cols: int

    @property
    def passed(self) -> bool:
        """``True`` when no ``"warning"``-severity findings are present.

        ``"info"``-severity findings (e.g. high cardinality) do not
        flip ``passed`` to ``False`` — they are advisory only.

        Designed for the CI idiom::

            qr = pycatdap.quality_report(df)
            assert qr.passed, qr.show()
        """
        return not any(w.severity == "warning" for w in self.warnings)

    def by_severity(self) -> dict[str, list[QualityWarning]]:
        """Group warnings by ``severity`` (``"info"`` / ``"warning"``)."""
        grouped: dict[str, list[QualityWarning]] = {}
        for w in self.warnings:
            grouped.setdefault(w.severity, []).append(w)
        return grouped

    def by_kind(self) -> dict[str, list[QualityWarning]]:
        """Group warnings by ``kind`` (e.g. ``"high_missing"``)."""
        grouped: dict[str, list[QualityWarning]] = {}
        for w in self.warnings:
            grouped.setdefault(w.kind, []).append(w)
        return grouped

    def show(self) -> None:
        """Render an inline summary suitable for Jupyter or plain stdout."""
        header = (
            f"QualityReport — {self.n_rows} rows × {self.n_cols} cols · "
            f"{'passed' if self.passed else 'failed'} "
            f"({len(self.warnings)} warning"
            f"{'s' if len(self.warnings) != 1 else ''})"
        )
        try:
            from IPython.display import display
        except ImportError:
            print(header)
            if self.warnings:
                print(self._warnings_table().to_string())
            return

        print(header)
        if self.warnings:
            display(self._warnings_table())

    def _warnings_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "severity": w.severity,
                    "kind": w.kind,
                    "column": w.column,
                    "message": w.message,
                    "metric": w.metric,
                }
                for w in self.warnings
            ]
        )

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a single-file HTML report.

        Mirrors :meth:`pycatdap.ProfileResult.to_html` — uses jinja2 and
        :func:`pycatdap._io.atomic_write_text`. No Plotly figures are
        embedded because the report is text-only, so ``jinja2`` is the
        only optional dependency.

        Parameters
        ----------
        path : str, Path, or None
            If given, the HTML is also written to this path atomically.
            Returns the HTML string in both modes.

        Returns
        -------
        str
            The rendered HTML.

        Raises
        ------
        ImportError
            If ``jinja2`` is not installed (ship as part of
            ``pycatdap[plotly]`` extras).
        """
        try:
            from jinja2 import Environment, select_autoescape
        except ImportError as exc:
            msg = (
                "jinja2 is required for HTML reports. "
                "Install it with: pip install 'pycatdap[plotly]'"
            )
            raise ImportError(msg) from exc

        from importlib.resources import files as _resource_files

        template_text = (
            _resource_files("pycatdap.templates")
            .joinpath("quality_report.html.j2")
            .read_text(encoding="utf-8")
        )
        env = Environment(autoescape=select_autoescape(default=True))
        template = env.from_string(template_text)

        from pycatdap._version import __version__

        counts_by_kind = dict(Counter(w.kind for w in self.warnings))

        html = template.render(
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            warnings=self.warnings,
            counts_by_kind=counts_by_kind,
            passed=self.passed,
            pycatdap_version=__version__,
        )

        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")

        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return {
            "warnings": [
                {
                    "severity": w.severity,
                    "kind": w.kind,
                    "column": w.column,
                    "message": w.message,
                    "metric": w.metric,
                }
                for w in self.warnings
            ],
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "passed": self.passed,
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return a Plotly figure spec dict (DP-4).

        QualityReport has no numerical figures, but the warnings list
        renders as a Plotly Table for LizyStudio / react-plotly.js
        consumers. Built directly (no plotly dependency at import time).
        """
        return {"warnings_table": _warnings_table_spec(self.warnings)}


def _warnings_table_spec(warnings: list[QualityWarning]) -> dict[str, Any]:
    """Build a Plotly Table figure spec for the warnings list."""
    return {
        "data": [
            {
                "type": "table",
                "header": {
                    "values": ["severity", "kind", "column", "message", "metric"],
                    "align": "left",
                },
                "cells": {
                    "values": [
                        [w.severity for w in warnings],
                        [w.kind for w in warnings],
                        [w.column for w in warnings],
                        [w.message for w in warnings],
                        [w.metric for w in warnings],
                    ],
                    "align": "left",
                },
            }
        ],
        "layout": {"title": "Quality warnings"},
    }


def quality_report(
    df: pd.DataFrame,
    *,
    quality_thresholds: dict[str, float] | None = None,
) -> QualityReport:
    """Scan ``df`` for data-quality issues and return a :class:`QualityReport`.

    A focused alternative to :func:`pycatdap.profile` when only the
    quality-warning section is needed. Shares the same warning logic
    (:func:`pycatdap._quality._scan_quality`) but skips
    :func:`pycatdap.association_matrix` and :func:`pycatdap.catdap2`,
    so the runtime stays roughly linear in ``n_rows × n_cols``.

    Default checks emit:

    - ``high_missing`` (severity ``"warning"``) when missing rate > 50%
    - ``constant`` (severity ``"warning"``) when ``n_unique <= 1``
    - ``id_candidate`` (severity ``"warning"``) when every non-null value
      is unique for a categorical column
    - ``high_cardinality`` (severity ``"info"``) when ``n_unique / n_obs``
      > 50% and ``n_unique`` > 50

    Parameters
    ----------
    df : DataFrame
        Source frame to inspect.
    quality_thresholds : dict or None
        Override default warning thresholds. Recognized keys:

        - ``"high_cardinality"`` (default 0.5): nunique / n_obs ratio
        - ``"high_cardinality_abs_min"`` (default 50): nunique floor
        - ``"high_missing"`` (default 0.5): missing rate

        Passing ``{}`` is treated as "use defaults" (not "reset to no
        thresholds"); ``None`` means the same. Per-key overrides leave
        the rest at default — partial dicts are supported.

    Returns
    -------
    QualityReport

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> qr = pycatdap.quality_report(df)
    >>> isinstance(qr.passed, bool)
    True
    """
    n_rows, n_cols = df.shape

    thresholds = dict(_DEFAULT_QUALITY_THRESHOLDS)
    # Explicit None check, not truthy-check: `quality_thresholds={}` is a
    # legitimate "use defaults" call and must not be confused with an
    # unset parameter. (feedback_python_falsy_or_default_trap)
    if quality_thresholds is not None:
        thresholds.update(quality_thresholds)

    variables = _build_variables(df, response=None)
    warnings = _scan_quality(df, variables, thresholds)

    return QualityReport(warnings=warnings, n_rows=n_rows, n_cols=n_cols)


__all__ = ["QualityReport", "quality_report"]
