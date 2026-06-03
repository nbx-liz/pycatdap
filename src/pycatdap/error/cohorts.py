"""Cohort comparison and drift detection (H-0014 Phase L, PR-L4).

Two public functions, both built on the same AIC engine used everywhere
else in pycatdap:

- :func:`compare_cohorts` — quantify how two cohorts differ. Cohort
  membership (``a`` vs ``b``) is treated as a synthetic binary response;
  each shared column's ΔAIC against it measures how strongly that column
  distinguishes the cohorts (Sweetviz-style report via ``to_html``).
- :func:`detect_drift` — a thin specialisation comparing a training
  cohort against a production cohort, ranking features by drift
  magnitude; optionally reports the production error rate.

Continuous columns are AIC-binned (against the cohort label, on the
stacked data so both cohorts share identical bins) by reusing
:func:`pycatdap.error.discovery._bin_continuous`.

Immutability follows the H-0009 discipline: frozen dataclasses,
MappingProxyType-wrapped mappings, frozen DataFrame numpy buffers.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

import numpy as np
import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap._contingency import build_crosstab
from pycatdap.error._labels import error_label
from pycatdap.error.discovery import _bin_continuous, _is_continuous

#: Synthetic cohort-membership response column.
_COHORT_COL = "_cohort_"

#: Cohort labels.
_A, _B = "a", "b"


def _shared_columns(df_a: pd.DataFrame, df_b: pd.DataFrame) -> list[str]:
    """Columns present in both frames, in ``df_a`` order."""
    b_cols = set(df_b.columns)
    return [c for c in df_a.columns if c in b_cols]


def _prepare_stacked(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Stack both cohorts with a membership column and AIC-bin continuous columns.

    Continuous columns are binned against membership so both cohorts
    share identical bins.
    """
    a = df_a[columns].reset_index(drop=True)
    b = df_b[columns].reset_index(drop=True)
    cohort = np.array([_A] * len(a) + [_B] * len(b), dtype=object)
    stacked = pd.concat([a, b], ignore_index=True)

    prepared = pd.DataFrame(index=stacked.index)
    for col in columns:
        series = stacked[col]
        if _is_continuous(series):
            prepared[col] = _bin_continuous(series, cohort)
        else:
            prepared[col] = series.astype("object")
    prepared[_COHORT_COL] = cohort
    return prepared


def _cohort_aic_table(prepared: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Per-column ΔAIC of cohort membership (negative = discriminative)."""
    records: list[dict[str, Any]] = []
    for col in columns:
        cross, marg_e, marg_f, n = build_crosstab(prepared, _COHORT_COL, col)
        delta = compute_delta_aic(cross, marg_e, marg_f, n) if n > 0 else 0.0
        records.append({"variable": col, "delta_aic": float(delta)})
    table = pd.DataFrame(records, columns=["variable", "delta_aic"])
    sorted_table: pd.DataFrame = table.sort_values(
        "delta_aic", ascending=True, ignore_index=True
    )
    return sorted_table


def _interval_sort_key(value: object) -> tuple[int, float, str]:
    """Sort categories numerically for interval labels, else lexicographically.

    Interval/bound labels look like ``"< 10"`` / ``"[10, 20]"`` / ``">= 20"``.
    Returns ``(group, leading_number, text)`` so plain categoricals sort
    by text and binned labels sort by their first numeric edge.
    """
    text = str(value)
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if match:
        return (0, float(match.group()), text)
    return (1, 0.0, text)


def _distribution(prepared: pd.DataFrame, col: str) -> pd.DataFrame:
    """Normalised per-value distribution of ``col`` in each cohort."""
    sub = prepared[[col, _COHORT_COL]].dropna()
    prop_a = sub[sub[_COHORT_COL] == _A][col].value_counts(normalize=True)
    prop_b = sub[sub[_COHORT_COL] == _B][col].value_counts(normalize=True)
    values = sorted(set(prop_a.index) | set(prop_b.index), key=_interval_sort_key)
    return pd.DataFrame(
        {
            "value": values,
            "prop_a": [float(prop_a.get(v, 0.0)) for v in values],
            "prop_b": [float(prop_b.get(v, 0.0)) for v in values],
            "diff": [float(prop_a.get(v, 0.0) - prop_b.get(v, 0.0)) for v in values],
        }
    )


@dataclass(frozen=True)
class CohortComparison:
    """Result of :func:`compare_cohorts` (immutable).

    Attributes
    ----------
    summary : pd.DataFrame
        One row per shared column: ``variable`` / ``delta_aic`` (cohort
        membership ΔAIC; more negative = the column distinguishes the
        cohorts more) / ``max_abs_diff`` (largest absolute per-value
        proportion difference). Sorted by ``delta_aic`` ascending.
    distributions : Mapping[str, pd.DataFrame]
        Per-column ``value / prop_a / prop_b / diff`` tables.
    n_a, n_b : int
        Row counts of each cohort.
    response_delta : pd.DataFrame or None
        When ``response`` is supplied: per-feature ΔAIC against the
        response within cohort A vs B and their difference, surfacing
        relationship shifts. ``None`` otherwise.
    """

    summary: pd.DataFrame = field(repr=False)
    distributions: Mapping[str, pd.DataFrame] = field(repr=False)
    n_a: int
    n_b: int
    response_delta: pd.DataFrame | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        _freeze_frame(self.summary)
        if not isinstance(self.distributions, MappingProxyType):
            for frame in self.distributions.values():
                _freeze_frame(frame)
            object.__setattr__(
                self, "distributions", MappingProxyType(dict(self.distributions))
            )
        if self.response_delta is not None:
            _freeze_frame(self.response_delta)

    def to_dict(self) -> dict[str, Any]:
        """JSON-serialisable summary."""
        return {
            "n_a": int(self.n_a),
            "n_b": int(self.n_b),
            "summary": self.summary.to_dict(orient="records"),
            "distributions": {
                col: frame.to_dict(orient="records")
                for col, frame in self.distributions.items()
            },
            "response_delta": (
                None
                if self.response_delta is None
                else self.response_delta.to_dict(orient="records")
            ),
        }

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a Sweetviz-style single-file HTML report.

        Parameters
        ----------
        path : str, Path, or None
            If given, also written atomically. The HTML string is
            returned in both modes.

        Raises
        ------
        ImportError
            If ``jinja2`` is not installed (``pip install
            'pycatdap[plotly]'``).
        """
        html = _render_cohort_html(self)
        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")
        return html


@dataclass(frozen=True)
class DriftReport:
    """Result of :func:`detect_drift` (immutable).

    Attributes
    ----------
    drift_ranking : pd.DataFrame
        ``variable`` / ``delta_aic`` for train-vs-prod cohort
        membership, sorted by ``|delta_aic|`` descending (most-drifted
        feature first).
    n_train, n_prod : int
        Row counts.
    error_rate_prod : float or None
        Production error rate (``error_label == "incorrect"`` share) when
        ``y_true`` / ``y_pred`` are supplied; a model-degradation signal.
        ``None`` otherwise.
    """

    drift_ranking: pd.DataFrame = field(repr=False)
    n_train: int
    n_prod: int
    error_rate_prod: float | None = None

    def __post_init__(self) -> None:
        _freeze_frame(self.drift_ranking)

    def to_dict(self) -> dict[str, Any]:
        """JSON-serialisable summary."""
        return {
            "n_train": int(self.n_train),
            "n_prod": int(self.n_prod),
            "error_rate_prod": (
                None if self.error_rate_prod is None else float(self.error_rate_prod)
            ),
            "drift_ranking": self.drift_ranking.to_dict(orient="records"),
        }


def compare_cohorts(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    *,
    response: str | None = None,
) -> CohortComparison:
    """Compare two cohorts by AIC and per-feature distribution.

    Parameters
    ----------
    df_a, df_b : DataFrame
        The two cohorts. Only their shared columns are compared. Neither
        is mutated.
    response : str or None
        When given (and present in both frames), additionally report how
        each feature's ΔAIC against the response shifts between cohorts.

    Returns
    -------
    CohortComparison

    Raises
    ------
    ValueError
        If the frames share no columns.
    """
    shared = _shared_columns(df_a, df_b)
    # response_delta is only meaningful when the response is present in
    # BOTH cohorts; otherwise _feature_response_aic would return 0.0 for
    # the missing side and the "shift" would be garbage (review finding).
    response_in_shared = response is not None and response in shared
    columns = [c for c in shared if c != response] if response_in_shared else shared
    if not columns:
        msg = "df_a and df_b share no comparable columns"
        raise ValueError(msg)

    prepared = _prepare_stacked(df_a, df_b, columns)
    summary = _cohort_aic_table(prepared, columns)

    # max abs per-value proportion diff, joined onto the summary.
    distributions = {col: _distribution(prepared, col) for col in columns}
    max_abs = {
        col: float(frame["diff"].abs().max()) if len(frame) else 0.0
        for col, frame in distributions.items()
    }
    summary = summary.assign(
        max_abs_diff=summary["variable"].map(max_abs).astype(float)
    )

    response_delta = None
    if response_in_shared:
        assert response is not None  # narrowed by response_in_shared
        response_delta = _response_delta_table(df_a, df_b, columns, response)

    return CohortComparison(
        summary=summary,
        distributions=distributions,
        n_a=len(df_a),
        n_b=len(df_b),
        response_delta=response_delta,
    )


def _response_delta_table(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    columns: list[str],
    response: str,
) -> pd.DataFrame:
    """Per-feature ΔAIC against ``response`` in each cohort + the shift."""
    records: list[dict[str, Any]] = []
    for col in columns:
        da = _feature_response_aic(df_a, col, response)
        db = _feature_response_aic(df_b, col, response)
        records.append(
            {
                "variable": col,
                "delta_aic_a": da,
                "delta_aic_b": db,
                "shift": db - da,
            }
        )
    table = pd.DataFrame(
        records, columns=["variable", "delta_aic_a", "delta_aic_b", "shift"]
    )
    ordered: pd.DataFrame = table.reindex(
        table["shift"].abs().sort_values(ascending=False).index
    ).reset_index(drop=True)
    return ordered


def _feature_response_aic(df: pd.DataFrame, col: str, response: str) -> float:
    """ΔAIC of ``col`` against ``response`` within one cohort."""
    if response not in df.columns or col not in df.columns:
        return 0.0
    work = df[[response, col]].copy()
    if _is_continuous(work[col]):
        resp = work[response].astype(object).to_numpy()
        work[col] = _bin_continuous(work[col], resp)
    cross, marg_e, marg_f, n = build_crosstab(work, response, col)
    return float(compute_delta_aic(cross, marg_e, marg_f, n)) if n > 0 else 0.0


def detect_drift(
    df_train: pd.DataFrame,
    df_prod: pd.DataFrame,
    *,
    y_true: Any = None,
    y_pred: Any = None,
) -> DriftReport:
    """Detect feature drift between a training and a production cohort.

    Parameters
    ----------
    df_train, df_prod : DataFrame
        Training and production feature frames. Not mutated.
    y_true, y_pred : array-like, optional
        Production ground-truth and predictions. When both are given,
        the production error rate is reported as a degradation signal.

    Returns
    -------
    DriftReport
    """
    comparison = compare_cohorts(df_train, df_prod)
    ranking = comparison.summary[["variable", "delta_aic"]].copy()
    ranking = ranking.reindex(
        ranking["delta_aic"].abs().sort_values(ascending=False).index
    ).reset_index(drop=True)

    error_rate_prod: float | None = None
    if y_true is not None and y_pred is not None:
        labels = error_label(y_true, y_pred)
        error_rate_prod = float((labels.to_numpy() == "incorrect").mean())

    return DriftReport(
        drift_ranking=ranking,
        n_train=len(df_train),
        n_prod=len(df_prod),
        error_rate_prod=error_rate_prod,
    )


def _freeze_frame(frame: pd.DataFrame) -> None:
    """Freeze the numpy buffers of a DataFrame in place (H-0009)."""
    for col in frame.columns:
        values = frame[col].values
        if isinstance(values, np.ndarray):
            values.flags.writeable = False


def _render_cohort_html(comparison: CohortComparison) -> str:
    """Render the cohort-comparison template."""
    try:
        from jinja2 import Environment, select_autoescape
    except ImportError as exc:
        msg = (
            "jinja2 is required for HTML reports. "
            "Install it with: pip install 'pycatdap[plotly]'"
        )
        raise ImportError(msg) from exc

    from importlib.resources import files as _resource_files

    from pycatdap._version import __version__

    template_text = (
        _resource_files("pycatdap.templates")
        .joinpath("cohort_comparison.html.j2")
        .read_text(encoding="utf-8")
    )
    env = Environment(autoescape=select_autoescape(default=True))
    template = env.from_string(template_text)

    columns = [
        {
            "variable": row["variable"],
            "delta_aic": f"{row['delta_aic']:.4f}",
            "max_abs_diff": f"{row['max_abs_diff']:.4f}",
            "distribution": comparison.distributions[row["variable"]].to_dict(
                orient="records"
            ),
        }
        for _, row in comparison.summary.iterrows()
    ]
    return template.render(
        n_a=comparison.n_a,
        n_b=comparison.n_b,
        columns=columns,
        has_response=comparison.response_delta is not None,
        response_delta=(
            None
            if comparison.response_delta is None
            else comparison.response_delta.to_dict(orient="records")
        ),
        pycatdap_version=__version__,
    )
