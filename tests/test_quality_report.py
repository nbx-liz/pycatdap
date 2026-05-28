"""Tests for :func:`pycatdap.quality_report` (H-0008 PR-D2).

``quality_report(df)`` is a focused data-quality scan: it shares
:func:`pycatdap._quality._scan_quality` with :func:`pycatdap.profile`
but skips the heavier ``association_matrix`` / ``catdap2`` passes, so
it stays fast on wide CI datasets. The returned :class:`QualityReport`
exposes a ``.passed`` boolean tailored for ``assert qr.passed`` in
pytest / CI.
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def df_clean() -> pd.DataFrame:
    # n=40 keeps `b` under the n_unique > 50 cardinality threshold so
    # the fixture stays warning-free with default thresholds.
    rng = np.random.default_rng(seed=7)
    return pd.DataFrame(
        {
            "a": rng.choice(["x", "y", "z"], size=40),
            "b": rng.normal(0, 1, size=40),
            "c": rng.choice([True, False], size=40),
        }
    )


@pytest.fixture()
def df_with_issues() -> pd.DataFrame:
    n = 200
    return pd.DataFrame(
        {
            "almost_all_nan": [np.nan] * 110 + list(range(90)),
            "constant_col": ["x"] * n,
            "id_like": [f"id-{i}" for i in range(n)],
            # 150 unique strings to trigger high_cardinality without
            # being a perfect id (n_unique < n_obs)
            "high_card": [f"v-{i % 150}" for i in range(n)],
            "ok": np.arange(n, dtype=float),
        }
    )


def test_returns_quality_report(df_clean: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_clean)
    assert isinstance(qr, pycatdap.QualityReport)
    assert qr.n_rows == len(df_clean)
    assert qr.n_cols == len(df_clean.columns)


def test_clean_frame_passes(df_clean: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_clean)
    assert qr.passed is True
    assert qr.warnings == []


def test_constant_column_triggers_warning() -> None:
    df = pd.DataFrame({"const": ["x"] * 50, "var": np.arange(50)})
    qr = pycatdap.quality_report(df)
    assert qr.passed is False
    assert any(w.kind == "constant" and w.column == "const" for w in qr.warnings)


def test_high_missing_triggers_warning() -> None:
    df = pd.DataFrame(
        {
            "mostly_nan": [np.nan] * 80 + [1.0] * 20,
            "ok": np.arange(100),
        }
    )
    qr = pycatdap.quality_report(df)
    assert qr.passed is False
    assert any(w.kind == "high_missing" for w in qr.warnings)


def test_id_candidate_only_for_categorical() -> None:
    df = pd.DataFrame(
        {
            "ids": [f"r{i}" for i in range(100)],
            "continuous": np.linspace(0, 1, 100),
        }
    )
    qr = pycatdap.quality_report(df)
    kinds = {(w.column, w.kind) for w in qr.warnings}
    assert ("ids", "id_candidate") in kinds
    assert ("continuous", "id_candidate") not in kinds


def test_high_cardinality_is_info_severity_passes() -> None:
    # high_cardinality is INFO not WARNING — qr.passed should stay True
    df = pd.DataFrame({"hc": [f"v-{i % 150}" for i in range(200)]})
    qr = pycatdap.quality_report(df)
    assert any(w.kind == "high_cardinality" for w in qr.warnings)
    assert qr.passed is True  # info-severity findings do not fail the report


def test_multiple_warnings_combined(df_with_issues: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    kinds = {w.kind for w in qr.warnings}
    assert {"high_missing", "constant", "id_candidate", "high_cardinality"} <= kinds
    assert qr.passed is False


def test_quality_thresholds_empty_dict_uses_defaults() -> None:
    # feedback_python_falsy_or_default_trap: quality_thresholds={} must
    # NOT be confused with "unset" (which it would under `or` semantics).
    df = pd.DataFrame({"const": ["x"] * 10})
    qr = pycatdap.quality_report(df, quality_thresholds={})
    assert any(w.kind == "constant" for w in qr.warnings)


def test_quality_thresholds_override() -> None:
    df = pd.DataFrame(
        {
            "mostly_present": [np.nan] * 20 + list(range(80)),
            "ok": np.arange(100),
        }
    )
    # default high_missing=0.5 → no warning; tighten to 0.1
    default = pycatdap.quality_report(df)
    assert not any(
        w.kind == "high_missing" and w.column == "mostly_present"
        for w in default.warnings
    )
    tight = pycatdap.quality_report(df, quality_thresholds={"high_missing": 0.1})
    assert any(
        w.kind == "high_missing" and w.column == "mostly_present"
        for w in tight.warnings
    )


def test_by_severity_groups_warnings(df_with_issues: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    grouped = qr.by_severity()
    assert set(grouped.keys()) <= {"info", "warning"}
    assert all(w.severity == "warning" for w in grouped.get("warning", []))
    assert all(w.severity == "info" for w in grouped.get("info", []))


def test_by_kind_groups_warnings(df_with_issues: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    grouped = qr.by_kind()
    # each kind appears at most once in the test frame
    for kind, group in grouped.items():
        assert all(w.kind == kind for w in group)


def test_to_dict_is_json_serializable(df_with_issues: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    d = qr.to_dict()
    assert d["n_rows"] == len(df_with_issues)
    assert d["n_cols"] == len(df_with_issues.columns)
    assert "warnings" in d
    # round-trips through json
    json.dumps(d)


def test_to_plotly_json_returns_dict(df_with_issues: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    spec = qr.to_plotly_json()
    assert isinstance(spec, dict)
    # warnings section should always be present
    assert "warnings_table" in spec
    # plotly-spec shape: each figure has "data" and "layout"
    fig = spec["warnings_table"]
    assert "data" in fig
    assert "layout" in fig


def test_show_falls_back_to_print(
    df_with_issues: pd.DataFrame, capsys: pytest.CaptureFixture[str]
) -> None:
    qr = pycatdap.quality_report(df_with_issues)
    qr.show()
    out = capsys.readouterr().out
    assert "QualityReport" in out


def test_to_html_returns_string(df_with_issues: pd.DataFrame) -> None:
    pytest.importorskip("jinja2")
    qr = pycatdap.quality_report(df_with_issues)
    html = qr.to_html()
    assert isinstance(html, str)
    assert "<html" in html.lower()
    # warnings table should appear in body
    assert "constant" in html
    assert "id_candidate" in html


def test_to_html_writes_atomic(df_with_issues: pd.DataFrame, tmp_path: Path) -> None:
    pytest.importorskip("jinja2")
    out = tmp_path / "qr.html"
    qr = pycatdap.quality_report(df_with_issues)
    html = qr.to_html(path=out)
    assert out.exists()
    assert out.read_text(encoding="utf-8") == html
    # atomic_write_text uses tmp + os.replace — no leftover .tmp files
    assert list(tmp_path.glob("*.tmp")) == []


def test_to_html_empty_warnings(df_clean: pd.DataFrame) -> None:
    pytest.importorskip("jinja2")
    qr = pycatdap.quality_report(df_clean)
    html = qr.to_html()
    # empty-state copy should make the report readable even with zero warnings
    assert "no quality warnings" in html.lower() or "passed" in html.lower()


def test_to_html_raises_clean_import_error_without_jinja2(
    df_clean: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When jinja2 is missing, to_html raises ImportError with an install hint."""
    import sys

    monkeypatch.setitem(sys.modules, "jinja2", None)
    qr = pycatdap.quality_report(df_clean)
    with pytest.raises(ImportError, match="jinja2 is required"):
        qr.to_html()


def test_frozen_dataclass(df_clean: pd.DataFrame) -> None:
    qr = pycatdap.quality_report(df_clean)
    with pytest.raises(FrozenInstanceError):
        qr.warnings = []  # type: ignore[misc]


def test_public_re_export() -> None:
    assert pycatdap.quality_report is not None
    assert pycatdap.QualityReport is not None


def test_show_without_ipython_falls_back_to_stdout(
    df_with_issues: pd.DataFrame,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """show() falls back to print() when IPython is unavailable."""
    import sys

    monkeypatch.setitem(sys.modules, "IPython", None)
    monkeypatch.setitem(sys.modules, "IPython.display", None)
    qr = pycatdap.quality_report(df_with_issues)
    qr.show()
    out = capsys.readouterr().out
    assert "QualityReport" in out
    # warnings table must reach stdout in fallback mode
    assert "constant" in out


def test_show_with_no_warnings_fallback(
    df_clean: pd.DataFrame,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """show() prints only the header line when there are no warnings."""
    import sys

    monkeypatch.setitem(sys.modules, "IPython", None)
    monkeypatch.setitem(sys.modules, "IPython.display", None)
    qr = pycatdap.quality_report(df_clean)
    qr.show()
    out = capsys.readouterr().out
    assert "QualityReport" in out
    assert "passed" in out
