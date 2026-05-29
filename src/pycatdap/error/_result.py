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
from pathlib import Path
from types import MappingProxyType
from typing import Any, Literal

import numpy as np
import numpy.typing as npt
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
    y_true, y_pred : ndarray or None
        Raw aligned ground-truth and predicted labels, retained so the
        :meth:`plot_confusion` / :meth:`residual_plot` delegation
        methods can render without round-tripping through the user.
        Frozen at construction (H-0009 numpy ``writeable = False``).
        Defaults to ``None`` so existing test fixtures that built
        ``ErrorAnalysisResult`` instances directly still work; the
        :func:`pycatdap.error_analysis` wrapper always supplies them.
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
    y_true: npt.NDArray[Any] | None = field(default=None, repr=False)
    y_pred: npt.NDArray[Any] | None = field(default=None, repr=False)

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

        # H-0012 PR-H3: freeze the y_true / y_pred buffers in place so
        # delegation methods cannot mutate them. None guard per the
        # cross-check Claim 3 finding.
        if self.y_true is not None and isinstance(self.y_true, np.ndarray):
            self.y_true.flags.writeable = False
        if self.y_pred is not None and isinstance(self.y_pred, np.ndarray):
            self.y_pred.flags.writeable = False

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

    # ------------------------------------------------------------------
    # to_plotly_json()
    # ------------------------------------------------------------------

    def to_plotly_json(self) -> dict[str, Any]:
        """Return per-section Plotly figure specs (DP-4).

        Sections:
        - ``feature_ranking``: horizontal bar of ΔAIC per variable
        - ``confusion`` (classification only): bar of category counts
        - ``top_summaries``: each entry's native ``to_plotly_json()``
        """
        spec: dict[str, Any] = {
            "feature_ranking": _ranking_bar_spec(self.feature_ranking),
            "top_summaries": {
                col: summary.to_plotly_json()
                for col, summary in self.top_summaries.items()
            },
        }
        if self.confusion is not None:
            spec["confusion"] = _confusion_bar_spec(self.confusion)
        return spec

    # ------------------------------------------------------------------
    # to_html()
    # ------------------------------------------------------------------

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a single-file HTML report.

        Plotly figures for the top-K cross-tabs are embedded inline
        (``include_plotlyjs="inline"``) so the file is fully self-
        contained and viewable offline.

        Parameters
        ----------
        path : str, Path, or None
            If given, the HTML is also written atomically via
            :func:`pycatdap._io.atomic_write_text`. Returns the HTML
            string in both modes.

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
            .joinpath("error_analysis.html.j2")
            .read_text(encoding="utf-8")
        )
        env = Environment(autoescape=select_autoescape(default=True))
        template = env.from_string(template_text)

        from pycatdap._version import __version__

        top_rendered: list[dict[str, str]] = []
        for i, (col, summary) in enumerate(self.top_summaries.items()):
            include_js: Literal["inline", False] = "inline" if i == 0 else False
            top_rendered.append(
                {
                    "name": col,
                    "delta_aic": f"{summary.delta_aic:.4f}",
                    "html": _summary_to_html(summary, include_plotlyjs=include_js),
                }
            )

        confusion_records: list[dict[str, Any]] | None
        if self.confusion is not None:
            confusion_records = [
                {
                    "category": str(idx),
                    "count": int(self.confusion.loc[idx, "count"])
                    if "count" in self.confusion.columns
                    else int(self.confusion.loc[idx].sum()),
                }
                for idx in self.confusion.index
            ]
        else:
            confusion_records = None

        html = template.render(
            task=self.task,
            label_kind=self.label_kind,
            response_name=self.response_name,
            n_rows=self.n_rows,
            n_correct=self.n_correct,
            n_incorrect=self.n_incorrect,
            mae=self.mae,
            rmse=self.rmse,
            ranking=_ranking_to_records(self.feature_ranking),
            confusion=confusion_records,
            top_slices=[_slice_to_dict(s) for s in self.top_slices],
            top_summaries=top_rendered,
            pycatdap_version=__version__,
        )

        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")

        return html

    # ------------------------------------------------------------------
    # to_divexplorer_format()
    # ------------------------------------------------------------------

    def to_divexplorer_format(self) -> pd.DataFrame:
        """Return a DivExplorer-compatible flat DataFrame of slices.

        Columns: ``description / size / error_rate / delta_aic /
        pearson_residual``. One row per :class:`Slice`. Empty (but
        well-typed) DataFrame when no slice cleared the
        ``|pearson_residual| >= 2.0`` threshold.

        See <https://github.com/divexplorer/divexplorer> for the
        reference subgroup-DataFrame shape Phase L will fully integrate
        with; PR-G3 ships the format compatibility only.
        """
        records = [
            {
                "description": f"{s.variable} = {s.category}",
                "size": int(s.n_in_slice),
                "error_rate": float(s.error_rate),
                "delta_aic": float(s.delta_aic),
                "pearson_residual": float(s.pearson_residual),
                "error_category": s.error_category,
                "variable": s.variable,
                "category": s.category,
            }
            for s in self.top_slices
        ]
        return pd.DataFrame(
            records,
            columns=[
                "description",
                "size",
                "error_rate",
                "delta_aic",
                "pearson_residual",
                "error_category",
                "variable",
                "category",
            ],
        )

    # ------------------------------------------------------------------
    # Phase I+J delegation (H-0012 PR-H3)
    # ------------------------------------------------------------------

    def plot_confusion(
        self,
        *,
        backend: Literal["matplotlib", "plotly"] = "matplotlib",
        **kwargs: Any,
    ) -> Any:
        """Plot the confusion matrix using the stored ``y_true`` / ``y_pred``.

        Works for both binary and multi-class classification (per
        H-0012 §F-ter: \"the wrapper falls back to ``error_label`` on
        multi-class, but the heatmap renders any N×N matrix\").

        Parameters
        ----------
        backend : {"matplotlib", "plotly"}
            Plotting backend.
        **kwargs
            Forwarded to :func:`pycatdap.error.plot_confusion`
            (``labels``, ``normalize``, ``ax``, ``cmap``, ``show_values``
            for matplotlib; ``colorscale`` for plotly).

        Raises
        ------
        ValueError
            If ``self.task == "regression"`` (use :meth:`residual_plot`
            instead) or if the raw labels were not retained (legacy
            constructor calls that left ``y_true=None`` / ``y_pred=None``).
        """
        if self.task != "classification":
            msg = (
                f"plot_confusion is classification-only; got task="
                f"{self.task!r}. Use residual_plot for regression."
            )
            raise ValueError(msg)
        if self.y_true is None or self.y_pred is None:
            msg = (
                "plot_confusion requires y_true / y_pred; this "
                "ErrorAnalysisResult was constructed without them. "
                "Re-run pycatdap.error_analysis() to populate them, "
                "or pass them directly to pycatdap.error.plot_confusion()."
            )
            raise ValueError(msg)

        from pycatdap.error.confusion import plot_confusion as _plot_confusion

        return _plot_confusion(self.y_true, self.y_pred, backend=backend, **kwargs)

    def residual_plot(
        self,
        *,
        backend: Literal["matplotlib", "plotly"] = "matplotlib",
        **kwargs: Any,
    ) -> Any:
        """Plot residuals using the stored ``y_true`` / ``y_pred``.

        Parameters
        ----------
        backend : {"matplotlib", "plotly"}
            Plotting backend.
        **kwargs
            Forwarded to :func:`pycatdap.error.residual_plot`
            (``kind``, ``color_by``, ``ax``).

        Raises
        ------
        ValueError
            If ``self.task == "classification"`` (use
            :meth:`plot_confusion` instead) or if the raw labels were
            not retained.
        """
        if self.task != "regression":
            msg = (
                f"residual_plot is regression-only; got task="
                f"{self.task!r}. Use plot_confusion for classification."
            )
            raise ValueError(msg)
        if self.y_true is None or self.y_pred is None:
            msg = (
                "residual_plot requires y_true / y_pred; this "
                "ErrorAnalysisResult was constructed without them. "
                "Re-run pycatdap.error_analysis() to populate them, "
                "or pass them directly to pycatdap.error.residual_plot()."
            )
            raise ValueError(msg)

        from pycatdap.error.residual import residual_plot as _residual_plot

        return _residual_plot(self.y_true, self.y_pred, backend=backend, **kwargs)


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


def _ranking_bar_spec(ranking: pd.DataFrame) -> dict[str, Any]:
    variables = [str(v) for v in ranking["variable"].tolist()]
    delta_aic = [float(v) for v in ranking["delta_aic"].tolist()]
    return {
        "data": [
            {
                "type": "bar",
                "orientation": "h",
                "x": delta_aic,
                "y": variables,
                "marker": {
                    "color": ["#1a7f37" if v < 0 else "#cf222e" for v in delta_aic],
                },
            }
        ],
        "layout": {
            "title": "Feature ranking by ΔAIC against error label",
            "xaxis": {"title": "ΔAIC (lower = more informative)"},
            "yaxis": {"title": "variable", "autorange": "reversed"},
        },
    }


def _confusion_bar_spec(confusion: pd.DataFrame) -> dict[str, Any]:
    """Render the confusion summary as a category-count bar."""
    if "count" in confusion.columns:
        labels = [str(idx) for idx in confusion.index]
        counts = [int(confusion.loc[idx, "count"]) for idx in confusion.index]
    else:
        labels = [str(idx) for idx in confusion.index]
        counts = [int(confusion.loc[idx].sum()) for idx in confusion.index]
    return {
        "data": [
            {
                "type": "bar",
                "x": labels,
                "y": counts,
                "marker": {
                    "color": [
                        "#1a7f37" if lbl in {"TP", "TN"} else "#cf222e"
                        for lbl in labels
                    ],
                },
            }
        ],
        "layout": {
            "title": "Confusion label counts",
            "xaxis": {"title": "category"},
            "yaxis": {"title": "count"},
        },
    }


def _summary_to_html(
    summary: TargetSummary | RegressionTargetSummary,
    *,
    include_plotlyjs: Literal["inline", False],
) -> str:
    """Render one TargetSummary as a Plotly Table HTML fragment."""
    import plotly.graph_objects as go

    spec = summary.to_plotly_json()
    fig = go.Figure(spec)
    return str(fig.to_html(include_plotlyjs=include_plotlyjs, full_html=False))


__all__ = ["ErrorAnalysisResult", "Slice"]
