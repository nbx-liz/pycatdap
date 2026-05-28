"""Target-driven analysis API (H-0008 PR-D3).

``target_analysis(df, response)`` ranks every non-response column by
ΔAIC against ``response`` and keeps the full :class:`TargetSummary`
(or :class:`RegressionTargetSummary`) for the top-K most informative
columns. It is the target-driven counterpart to
:func:`pycatdap.profile`: where ``profile()`` scans pairwise
associations across all columns, ``target_analysis()`` focuses on one
response and produces a ranked, detailed view.

Returns :class:`TargetAnalysisResult` with the same 4-method
serialization contract as :class:`pycatdap.ProfileResult`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from pycatdap._target_pair import (
    RegressionTargetSummary,
    TargetSummary,
    target_summary,
)
from pycatdap.eda import _detect_kind
from pycatdap.profile import VariableCard, _build_variables, _card_to_dict


@dataclass(frozen=True)
class TargetAnalysisResult:
    """Result of :func:`target_analysis`.

    Attributes
    ----------
    response : str
        Response (target) column name.
    ranking : pd.DataFrame
        Columns ``variable / delta_aic / kind / n_obs`` for every
        non-response column, sorted ascending by ``delta_aic`` (most
        informative first).
    top_summaries : dict[str, TargetSummary | RegressionTargetSummary]
        Full :func:`pycatdap.target_summary` objects for the top-K
        most informative columns, keyed by column name.
    response_card : VariableCard
        :class:`pycatdap.VariableCard` describing the response column
        itself (kind, n_obs, n_missing, n_unique, top value, etc.).
    n_rows, n_cols : int
        Shape of the inspected frame.
    """

    response: str
    ranking: pd.DataFrame
    top_summaries: dict[str, TargetSummary | RegressionTargetSummary]
    response_card: VariableCard
    n_rows: int
    n_cols: int

    def show(self) -> None:
        """Render a ranked summary suitable for Jupyter or plain stdout."""
        header = (
            f"TargetAnalysisResult — response={self.response!r}, "
            f"{self.n_rows} rows × {self.n_cols} cols, "
            f"{len(self.top_summaries)} top summaries kept"
        )
        try:
            from IPython.display import display
        except ImportError:
            print(header)
            print()
            print(self.ranking.to_string(index=False))
            return

        print(header)
        display(self.ranking)
        for col, summary in self.top_summaries.items():
            display(f"--- top: {col} (ΔAIC = {summary.delta_aic:.4f}) ---")
            summary.show()

    def to_html(self, path: str | Path | None = None) -> str:
        """Render a single-file HTML report.

        Plotly figures for the top-K cross-tabs are embedded inline
        (``include_plotlyjs="inline"``) so the file is fully self-
        contained and viewable offline.

        Parameters
        ----------
        path : str, Path, or None
            If given, the HTML is also written to this path atomically
            via :func:`pycatdap._io.atomic_write_text`. Returns the HTML
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
        except ImportError as exc:
            msg = (
                "jinja2 is required for HTML reports. "
                "Install it with: pip install 'pycatdap[plotly]'"
            )
            raise ImportError(msg) from exc

        from importlib.resources import files as _resource_files

        template_text = (
            _resource_files("pycatdap.templates")
            .joinpath("target_analysis.html.j2")
            .read_text(encoding="utf-8")
        )
        env = Environment(autoescape=select_autoescape(default=True))
        template = env.from_string(template_text)

        from pycatdap._version import __version__

        # Render top summaries as inline Plotly HTML. The first figure
        # carries the plotly.js bundle; subsequent figures reuse it
        # (matches the profile.to_html pattern).
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

        html = template.render(
            response=self.response,
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            ranking=_ranking_to_records(self.ranking),
            response_card=self.response_card,
            top_summaries=top_rendered,
            pycatdap_version=__version__,
        )

        if path is not None:
            from pycatdap._io import atomic_write_text

            atomic_write_text(path, html, encoding="utf-8")

        return html

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable dict."""
        return {
            "response": self.response,
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "response_card": _card_to_dict(self.response_card),
            "ranking": _ranking_to_records(self.ranking),
            "top_summaries": {
                col: summary.to_dict() for col, summary in self.top_summaries.items()
            },
        }

    def to_plotly_json(self) -> dict[str, Any]:
        """Return per-section Plotly figure specs (DP-4).

        ``ranking`` renders as a Plotly bar chart of ΔAIC; each entry
        of ``top_summaries`` reuses its native ``to_plotly_json()``.
        """
        return {
            "ranking": _ranking_bar_spec(self.ranking),
            "top_summaries": {
                col: summary.to_plotly_json()
                for col, summary in self.top_summaries.items()
            },
        }


# -- helpers ----------------------------------------------------------------


def _ranking_to_records(ranking: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert the ranking DataFrame to a JSON-friendly list of records.

    Uses ``to_dict("records")`` rather than ``itertuples`` so the per-
    cell type is ``Any`` for mypy strict (itertuples returns a union of
    every possible pandas cell type — including ``datetime`` and
    ``complex`` — which doesn't satisfy ``float()``).
    """
    return [
        {
            "variable": str(rec["variable"]),
            "delta_aic": float(rec["delta_aic"]),
            "kind": str(rec["kind"]),
            "n_obs": int(rec["n_obs"]),
        }
        for rec in ranking.to_dict("records")
    ]


def _ranking_bar_spec(ranking: pd.DataFrame) -> dict[str, Any]:
    """Build a horizontal Plotly bar of ΔAIC per variable."""
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
            "title": "Variable ranking by ΔAIC",
            "xaxis": {"title": "ΔAIC (lower = more informative)"},
            "yaxis": {"title": "variable", "autorange": "reversed"},
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


def target_analysis(
    df: pd.DataFrame,
    response: str,
    *,
    top_k: int = 5,
    bins: int | None = None,
    criterion: Literal["aic", "aicc", "bic"] = "bic",
) -> TargetAnalysisResult:
    """Rank explanatory variables by ΔAIC against ``response``.

    For every non-response column, runs :func:`pycatdap.target_summary`
    with ``response`` as the target and the column as the explanatory,
    then sorts by ``delta_aic`` ascending (most negative = most
    informative). The top-K columns get their full
    :class:`TargetSummary` (or :class:`RegressionTargetSummary` for a
    continuous response) retained on the result.

    Parameters
    ----------
    df : DataFrame
        Source frame.
    response : str
        Target column. Must exist in ``df.columns``.
    top_k : int
        Number of top-ranked columns to retain full summaries for.
        Default 5. Capped at the number of available explanatories.
        ``top_k=0`` returns an empty ``top_summaries``.
    bins : int or None
        Binning for continuous explanatories, forwarded to
        :func:`target_summary`. ``None`` selects AIC-optimal binning.
    criterion : {'aic', 'aicc', 'bic'}
        Penalty family for the Gaussian regression path (continuous
        response).

    Returns
    -------
    TargetAnalysisResult

    Raises
    ------
    KeyError
        If ``response`` is not in ``df.columns``.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> r = pycatdap.target_analysis(df, response="Survived", top_k=3)
    >>> r.response == "Survived"
    True
    """
    if response not in df.columns:
        msg = f"target_analysis: response column not found: {response!r}"
        raise KeyError(msg)

    n_rows, n_cols = df.shape
    cards = _build_variables(df, response=None)
    response_card = next(c for c in cards if c.name == response)

    rows: list[dict[str, Any]] = []
    summaries_full: dict[str, TargetSummary | RegressionTargetSummary] = {}
    for name in df.columns:
        if name == response:
            continue
        s = target_summary(
            df,
            target=response,
            explanatory=name,
            bins=bins,
            criterion=criterion,
        )
        rows.append(
            {
                "variable": str(name),
                "delta_aic": float(s.delta_aic),
                "kind": _detect_kind(df[name]),
                "n_obs": int(df[name].notna().sum()),
            }
        )
        summaries_full[str(name)] = s

    ranking = pd.DataFrame(rows, columns=["variable", "delta_aic", "kind", "n_obs"])
    # Stable sort so ties keep input column order.
    ranking = ranking.sort_values(
        "delta_aic", ascending=True, kind="mergesort"
    ).reset_index(drop=True)

    if top_k <= 0:
        top_summaries: dict[str, TargetSummary | RegressionTargetSummary] = {}
    else:
        top_names = ranking["variable"].head(top_k).tolist()
        top_summaries = {name: summaries_full[name] for name in top_names}

    return TargetAnalysisResult(
        response=response,
        ranking=ranking,
        top_summaries=top_summaries,
        response_card=response_card,
        n_rows=n_rows,
        n_cols=n_cols,
    )


__all__ = ["TargetAnalysisResult", "target_analysis"]
