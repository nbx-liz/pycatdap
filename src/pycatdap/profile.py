"""One-call EDA report API (H-0007 Phase C).

Wraps :func:`pycatdap.describe`, :func:`pycatdap.association_matrix`,
:func:`pycatdap.target_summary`, and :func:`pycatdap.catdap2` behind a
single entry point that returns a :class:`ProfileResult`. The result
holds frozen dataclasses for variable cards and quality warnings, plus
the m x m AIC association matrix, and (when a response is given) the
top CATDAP-02 subsets.

HTML rendering via ``.to_html()`` lands in PR-C2 (jinja2 template).
This module provides the data layer and ``show / to_dict /
to_plotly_json`` methods.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

from pycatdap._association import association_matrix
from pycatdap._target_pair import target_summary
from pycatdap.catdap2 import Catdap2Result, catdap2
from pycatdap.eda import _detect_kind, _summarize_column

WarningKind = Literal["high_cardinality", "constant", "id_candidate", "high_missing"]
WarningSeverity = Literal["info", "warning"]


_DEFAULT_QUALITY_THRESHOLDS: dict[str, float] = {
    "high_cardinality": 0.5,  # nunique / n_obs threshold
    "high_cardinality_abs_min": 50.0,  # AND nunique > this
    "high_missing": 0.5,
}


@dataclass(frozen=True)
class QualityWarning:
    """One quality finding from :func:`profile`.

    Attributes
    ----------
    severity : {"info", "warning"}
        Severity tag for UI rendering.
    kind : {"high_cardinality", "constant", "id_candidate", "high_missing"}
        The specific finding category.
    column : str
        Affected column name.
    message : str
        Human-readable description.
    metric : float
        The numeric value that triggered the warning (e.g. missing rate,
        cardinality ratio).
    """

    severity: WarningSeverity
    kind: WarningKind
    column: str
    message: str
    metric: float


@dataclass(frozen=True)
class VariableCard:
    """Per-column data for the profile report.

    Attributes
    ----------
    name : str
        Column name.
    kind : str
        Result of :func:`pycatdap.eda._detect_kind`.
    n_obs, n_missing, n_unique : int
        Row counts.
    top_value : object or None
        Most frequent value (or ``None`` if the column is entirely null).
    top_freq : int or None
        Frequency of ``top_value``.
    stats : dict or None
        Numeric summary (mean / std / min / q25 / median / q75 / max) for
        continuous columns. ``None`` for non-continuous.
    delta_aic_vs_response : float or None
        ``target_summary(df, target=response, explanatory=name).delta_aic``
        when ``response`` was supplied to :func:`profile`; ``None``
        otherwise (and ``None`` for the response column itself).
    intervals : list of float or None
        AIC-optimal bin boundaries for a continuous column. ``None`` for
        non-continuous columns or when binning was not computed.
    """

    name: str
    kind: str
    n_obs: int
    n_missing: int
    n_unique: int
    top_value: Any
    top_freq: int | None
    stats: dict[str, float] | None
    delta_aic_vs_response: float | None
    intervals: list[float] | None


@dataclass(frozen=True)
class ProfileResult:
    """Output of :func:`profile` — one-call EDA snapshot.

    Attributes
    ----------
    overview : dict
        Table-level statistics (n_rows, n_cols, n_missing, missing_rate,
        n_duplicates, memory_bytes, dtype_counts).
    variables : list of VariableCard
        Per-column cards, in the original ``df.columns`` order.
    association : DataFrame
        m x m ΔAIC matrix (output of :func:`pycatdap.association_matrix`).
    top_subsets : Catdap2Result or None
        CATDAP-02 top-K subsets when ``response`` is provided to
        :func:`profile`; ``None`` otherwise.
    quality_warnings : list of QualityWarning
        Findings on missingness / cardinality / constants / id-likes.
    response : str or None
        The ``response`` argument passed to :func:`profile`.
    n_rows, n_cols : int
        Convenience accessors mirroring ``overview['n_rows']`` and
        ``overview['n_cols']``.
    """

    overview: dict[str, Any] = field(repr=False)
    variables: list[VariableCard] = field(repr=False)
    association: pd.DataFrame = field(repr=False)
    top_subsets: Catdap2Result | None = field(repr=False)
    quality_warnings: list[QualityWarning] = field(repr=False)
    response: str | None
    n_rows: int
    n_cols: int

    def __repr__(self) -> str:
        n_warn = len(self.quality_warnings)
        return (
            f"ProfileResult(rows={self.n_rows}, cols={self.n_cols}, "
            f"response={self.response!r}, warnings={n_warn})"
        )

    def show(self) -> None:
        """Render an inline summary suitable for Jupyter or plain stdout."""
        header = f"ProfileResult — {self.n_rows} rows × {self.n_cols} cols" + (
            f" (response={self.response!r})" if self.response else ""
        )
        try:
            from IPython.display import HTML, display
        except ImportError:
            print(header)
            print(self._overview_table().to_string())
            print()
            print(self._variables_table().to_string())
            if self.quality_warnings:
                print()
                print(self._warnings_table().to_string())
            return

        display(HTML(f"<h3>{header}</h3>"))
        display(self._overview_table())
        display(self._variables_table())
        if self.quality_warnings:
            display(self._warnings_table())

    def _overview_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [(k, v) for k, v in self.overview.items()],
            columns=["metric", "value"],
        )

    def _variables_table(self) -> pd.DataFrame:
        rows = [
            {
                "name": c.name,
                "kind": c.kind,
                "n_unique": c.n_unique,
                "n_missing": c.n_missing,
                "top": c.top_value,
                "delta_aic": c.delta_aic_vs_response,
            }
            for c in self.variables
        ]
        return pd.DataFrame(rows)

    def _warnings_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "severity": w.severity,
                    "kind": w.kind,
                    "column": w.column,
                    "metric": w.metric,
                    "message": w.message,
                }
                for w in self.quality_warnings
            ]
        )

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a single-file HTML report (H-0007 PR-C2).

        Plotly figures are embedded inline (``include_plotlyjs="inline"``)
        so the file is fully self-contained and viewable offline.

        Parameters
        ----------
        path : str, Path, or None
            If given, the HTML is also written to this path using
            :func:`pycatdap._io.atomic_write_text` (safe against
            concurrent readers, e.g. ``mkdocs serve``). Returns the HTML
            string in both modes.

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
        except ImportError as exc:  # pragma: no cover - exercised via monkeypatch
            msg = (
                "jinja2 is required for HTML reports. "
                "Install it with: pip install 'pycatdap[plotly]'"
            )
            raise ImportError(msg) from exc

        try:
            from importlib.resources import files as _resource_files
        except ImportError:  # pragma: no cover
            from importlib_resources import (
                files as _resource_files,  # type: ignore[no-redef]
            )

        template_text = (
            _resource_files("pycatdap.templates")
            .joinpath("profile.html.j2")
            .read_text(encoding="utf-8")
        )
        env = Environment(autoescape=select_autoescape(default=True))
        template = env.from_string(template_text)

        from pycatdap._version import __version__

        association_html = _render_association_html(self.association)
        top_subsets_html = (
            _render_top_subsets_html(self.top_subsets)
            if self.top_subsets is not None
            else ""
        )

        html = template.render(
            response=self.response,
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            overview=self.overview,
            variables=self.variables,
            quality_warnings=self.quality_warnings,
            association_heatmap_html=association_html,
            top_subsets_html=top_subsets_html,
            pycatdap_version=__version__,
        )

        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html)

        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict (via ``json.dumps(..., default=str)``)."""
        return {
            "overview": dict(self.overview),
            "variables": [_card_to_dict(c) for c in self.variables],
            "association": _df_to_dict(self.association),
            "top_subsets": (
                _df_to_dict(self.top_subsets.aic)
                if self.top_subsets is not None
                else None
            ),
            "quality_warnings": [_warning_to_dict(w) for w in self.quality_warnings],
            "response": self.response,
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return per-section Plotly figure specs for LizyStudio (DP-4).

        Builds the specs directly (no plotly dependency) for consumption
        by ``react-plotly.js`` or any Plotly renderer. Currently exposes
        the AIC heatmap and (when a response is set) the CATDAP-02
        single-variable bar.
        """
        sections: dict[str, Any] = {
            "association_heatmap": _association_heatmap_spec(self.association),
        }
        if self.top_subsets is not None:
            sections["top_subsets"] = self.top_subsets.to_plotly_json()
        return sections


def profile(
    df: pd.DataFrame,
    *,
    response: str | None = None,
    bins: int | None = None,
    criterion: Literal["aic", "aicc", "bic"] = "bic",
    top_k_subsets: int = 5,
    quality_thresholds: dict[str, float] | None = None,
) -> ProfileResult:
    """Build a one-call EDA report (H-0007 Phase C).

    Wraps :func:`pycatdap.describe`, :func:`pycatdap.association_matrix`,
    :func:`pycatdap.target_summary` (when ``response`` is given), and
    :func:`pycatdap.catdap2` behind a single call.

    Parameters
    ----------
    df : DataFrame
        Source data; not modified.
    response : str or None
        Optional response (target) column. When given:

        - each :class:`VariableCard` gets a ``delta_aic_vs_response``
        - :attr:`ProfileResult.top_subsets` is populated via CATDAP-02
    bins : int or None
        Forwarded to :func:`pycatdap.association_matrix` for binning
        continuous explanatories.
    criterion : {"aic", "aicc", "bic"}
        Penalty family for the Gaussian regression cells (H-0005).
    top_k_subsets : int
        ``nvar`` value passed to :func:`pycatdap.catdap2` when
        ``response`` is set. Default 5.
    quality_thresholds : dict or None
        Override default warning thresholds. Recognized keys:

        - ``"high_cardinality"`` (default 0.5): nunique / n_obs ratio
        - ``"high_cardinality_abs_min"`` (default 50): nunique floor
        - ``"high_missing"`` (default 0.5): missing rate

    Returns
    -------
    ProfileResult

    Raises
    ------
    KeyError
        If *response* is given but not in ``df.columns``.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> p = pycatdap.profile(df, response="Survived")
    >>> p.n_rows == len(df)
    True
    """
    if response is not None and response not in df.columns:
        msg = f"profile: response column not found: {response!r}"
        raise KeyError(msg)

    thresholds = dict(_DEFAULT_QUALITY_THRESHOLDS)
    if quality_thresholds:
        thresholds.update(quality_thresholds)

    n_rows, n_cols = df.shape
    overview = _build_overview(df, n_rows, n_cols)
    variables = _build_variables(df, response=response)
    assoc = association_matrix(df, bins=bins, criterion=criterion)
    top_subsets = (
        _run_catdap2(df, response=response, top_k_subsets=top_k_subsets)
        if response is not None
        else None
    )
    quality_warnings = _scan_quality(df, variables, thresholds)

    return ProfileResult(
        overview=overview,
        variables=variables,
        association=assoc,
        top_subsets=top_subsets,
        quality_warnings=quality_warnings,
        response=response,
        n_rows=n_rows,
        n_cols=n_cols,
    )


def _build_overview(df: pd.DataFrame, n_rows: int, n_cols: int) -> dict[str, Any]:
    n_missing = int(df.isna().sum().sum())
    total_cells = n_rows * n_cols
    missing_rate = float(n_missing / total_cells) if total_cells else float("nan")
    n_duplicates = int(df.duplicated().sum())
    memory_bytes = int(df.memory_usage(index=True, deep=True).sum())
    dtype_counts = {
        str(dtype): int(count) for dtype, count in df.dtypes.value_counts().items()
    }
    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "n_missing": n_missing,
        "missing_rate": missing_rate,
        "n_duplicates": n_duplicates,
        "memory_bytes": memory_bytes,
        "dtype_counts": dtype_counts,
    }


def _build_variables(df: pd.DataFrame, *, response: str | None) -> list[VariableCard]:
    cards: list[VariableCard] = []
    for name in df.columns:
        col = df[name]
        summary = _summarize_column(col)

        stats: dict[str, float] | None
        if summary["kind"] == "continuous":
            stats = {
                key: float(summary[key])
                for key in ("mean", "std", "min", "q25", "median", "q75", "max")
                if summary[key] is not None
            }
        else:
            stats = None

        delta_aic: float | None = None
        if response is not None and name != response:
            delta_aic = float(
                target_summary(df, target=response, explanatory=name).delta_aic
            )

        cards.append(
            VariableCard(
                name=str(name),
                kind=str(summary["kind"]),
                n_obs=int(summary["n_obs"]),
                n_missing=int(summary["n_missing"]),
                n_unique=int(summary["n_unique"]),
                top_value=summary["top"],
                top_freq=(
                    int(summary["top_freq"])
                    if summary["top_freq"] is not None
                    else None
                ),
                stats=stats,
                delta_aic_vs_response=delta_aic,
                intervals=None,  # populated by PR-C2 HTML template if needed
            )
        )
    return cards


def _run_catdap2(
    df: pd.DataFrame,
    *,
    response: str,
    top_k_subsets: int,
) -> Catdap2Result | None:
    """Run catdap2 with per-column pooling derived from dtype."""
    pool: list[int] = []
    for name in df.columns:
        kind = _detect_kind(df[name])
        # 1 = unequal pooling for continuous, 2 = categorical otherwise.
        pool.append(1 if kind == "continuous" else 2)
    return catdap2(df, pool=pool, response_name=response, nvar=top_k_subsets)


def _scan_quality(
    df: pd.DataFrame,
    cards: list[VariableCard],
    thresholds: dict[str, float],
) -> list[QualityWarning]:
    warnings: list[QualityWarning] = []
    high_card_ratio = thresholds["high_cardinality"]
    high_card_abs = thresholds["high_cardinality_abs_min"]
    high_missing = thresholds["high_missing"]

    for card in cards:
        if card.n_obs == 0:
            continue

        missing_rate = card.n_missing / card.n_obs

        if missing_rate > high_missing:
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="high_missing",
                    column=card.name,
                    message=(
                        f"{missing_rate * 100:.1f}% of values are missing "
                        f"(threshold {high_missing * 100:.0f}%)"
                    ),
                    metric=missing_rate,
                )
            )

        if card.n_unique <= 1:
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="constant",
                    column=card.name,
                    message="column has at most one distinct non-null value",
                    metric=float(card.n_unique),
                )
            )
            continue  # other warnings would double-trigger

        if (
            card.kind in {"categorical", "other"}
            and card.n_unique == card.n_obs - card.n_missing
        ):
            warnings.append(
                QualityWarning(
                    severity="warning",
                    kind="id_candidate",
                    column=card.name,
                    message="every non-null value is unique (identifier?)",
                    metric=1.0,
                )
            )
            continue

        unique_ratio = card.n_unique / card.n_obs if card.n_obs else 0.0
        if unique_ratio > high_card_ratio and card.n_unique > high_card_abs:
            warnings.append(
                QualityWarning(
                    severity="info",
                    kind="high_cardinality",
                    column=card.name,
                    message=(
                        f"{card.n_unique} distinct values "
                        f"({unique_ratio * 100:.1f}% of rows; threshold "
                        f"{high_card_ratio * 100:.0f}% and > "
                        f"{int(high_card_abs)})"
                    ),
                    metric=unique_ratio,
                )
            )

    return warnings


# -- helpers for to_html ---------------------------------------------------


def _render_association_html(association: pd.DataFrame) -> str:
    """Render the association heatmap as inline Plotly HTML.

    Uses ``include_plotlyjs="inline"`` so the bundled HTML is self-
    contained / offline-viewable (Issue #14 acceptance criterion).
    Inline mode adds ~3 MB per figure but is only paid once per call:
    subsequent figures in the same HTML reuse the bundle (``"cdn"``
    vs ``"inline"`` is per-Figure; we render only this one Figure inline
    and the rest with ``include_plotlyjs=False``).
    """
    from pycatdap.plot.plotly import aic_heatmap as _aic_heatmap_plotly

    fig = _aic_heatmap_plotly(association)
    return str(fig.to_html(include_plotlyjs="inline", full_html=False))


def _render_top_subsets_html(top_subsets: Catdap2Result) -> str:
    """Render the CATDAP-02 single-variable bar as Plotly HTML.

    Reuses the plotly.js bundle inlined by the association heatmap, so
    we pass ``include_plotlyjs=False`` here.
    """
    import plotly.graph_objects as go

    spec = top_subsets.to_plotly_json()
    fig = go.Figure(spec)
    return str(fig.to_html(include_plotlyjs=False, full_html=False))


# -- helpers for to_plotly_json -------------------------------------------


def _association_heatmap_spec(association: pd.DataFrame) -> dict[str, Any]:
    """Build a Plotly Heatmap figure spec from the ΔAIC matrix.

    Mirrors :func:`pycatdap.plot.plotly.aic_heatmap` but constructs the
    dict directly so the function works without plotly installed.
    """
    data = association.to_numpy(dtype=float)
    finite = data[np.isfinite(data)]
    abs_max = float(np.nanmax(np.abs(finite))) if finite.size else 1.0
    if abs_max == 0.0:
        abs_max = 1.0
    return {
        "data": [
            {
                "type": "heatmap",
                "z": [
                    [None if not np.isfinite(v) else float(v) for v in row]
                    for row in data
                ],
                "x": [str(c) for c in association.columns],
                "y": [str(r) for r in association.index],
                "colorscale": "RdYlGn_r",
                "zmid": 0,
                "zmin": -abs_max,
                "zmax": abs_max,
                "colorbar": {"title": "ΔAIC"},
            }
        ],
        "layout": {
            "title": "ΔAIC heatmap",
            "xaxis": {"title": "Explanatory"},
            "yaxis": {"title": "Response", "autorange": "reversed"},
        },
    }


# -- helpers for to_dict ---------------------------------------------------


def _df_to_dict(df: pd.DataFrame) -> dict[str, Any]:
    return {
        "index": [str(i) for i in df.index],
        "columns": [str(c) for c in df.columns],
        "data": [
            [
                None
                if pd.isna(v)
                else (
                    float(v)
                    if isinstance(v, (int, float, np.floating, np.integer))
                    else str(v)
                )
                for v in row
            ]
            for row in df.itertuples(index=False, name=None)
        ],
    }


def _card_to_dict(card: VariableCard) -> dict[str, Any]:
    return {
        "name": card.name,
        "kind": card.kind,
        "n_obs": card.n_obs,
        "n_missing": card.n_missing,
        "n_unique": card.n_unique,
        "top_value": card.top_value,
        "top_freq": card.top_freq,
        "stats": dict(card.stats) if card.stats is not None else None,
        "delta_aic_vs_response": card.delta_aic_vs_response,
        "intervals": list(card.intervals) if card.intervals is not None else None,
    }


def _warning_to_dict(w: QualityWarning) -> dict[str, Any]:
    return {
        "severity": w.severity,
        "kind": w.kind,
        "column": w.column,
        "message": w.message,
        "metric": w.metric,
    }


# Re-export `replace` for downstream construction if needed.
__all__ = [
    "ProfileResult",
    "QualityWarning",
    "VariableCard",
    "profile",
    "replace",
]
