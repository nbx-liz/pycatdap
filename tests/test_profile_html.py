"""Tests for ProfileResult.to_html (H-0007 PR-C2).

HTML report generation via jinja2 template with inline Plotly figures.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def df_titanic_like() -> pd.DataFrame:
    rng = np.random.default_rng(seed=2026)
    n = 100
    cat = rng.choice(["a", "b", "c"], size=n)
    return pd.DataFrame(
        {
            "survived": rng.choice(["yes", "no"], size=n),
            "class": rng.choice(["1st", "2nd", "3rd"], size=n),
            "fare": np.where(cat == "a", 5.0, 50.0) + rng.normal(0.0, 5.0, size=n),
            "boarded": cat,
        }
    )


@pytest.fixture()
def df_with_warnings() -> pd.DataFrame:
    n = 60
    return pd.DataFrame(
        {
            "good": [i % 3 for i in range(n)],
            "constant": ["x"] * n,
        }
    )


class TestReturnType:
    """to_html() returns a string in both no-path and path modes."""

    def test_returns_string_without_path(self, df_titanic_like: pd.DataFrame) -> None:
        pytest.importorskip("jinja2")
        result = pycatdap.profile(df_titanic_like, response="survived")
        html = result.to_html()
        assert isinstance(html, str)
        assert html.startswith("<!DOCTYPE html>") or html.startswith("<html")

    def test_returns_string_and_writes_file(
        self, df_titanic_like: pd.DataFrame, tmp_path: Path
    ) -> None:
        pytest.importorskip("jinja2")
        path = tmp_path / "report.html"
        result = pycatdap.profile(df_titanic_like, response="survived")
        html = result.to_html(path)
        assert isinstance(html, str)
        assert path.exists()
        assert path.read_text() == html


class TestStructure:
    """The rendered HTML contains every documented section."""

    @pytest.fixture()
    def html(self, df_titanic_like: pd.DataFrame) -> str:
        pytest.importorskip("jinja2")
        result = pycatdap.profile(df_titanic_like, response="survived")
        return result.to_html()

    def test_has_overview_section(self, html: str) -> None:
        assert re.search(r"Overview", html, re.IGNORECASE)

    def test_has_variables_section(self, html: str) -> None:
        assert re.search(r"Variables", html, re.IGNORECASE)

    def test_has_association_section(self, html: str) -> None:
        assert re.search(r"associations?", html, re.IGNORECASE)

    def test_has_top_subsets_when_response_given(self, html: str) -> None:
        assert re.search(r"subsets?", html, re.IGNORECASE)

    def test_variables_section_lists_every_column(
        self, df_titanic_like: pd.DataFrame, html: str
    ) -> None:
        for col in df_titanic_like.columns:
            assert col in html, f"Variables section missing {col!r}"


class TestNoResponseMode:
    """response=None hides top_subsets but keeps the rest."""

    def test_top_subsets_section_omitted_without_response(
        self, df_titanic_like: pd.DataFrame
    ) -> None:
        pytest.importorskip("jinja2")
        html = pycatdap.profile(df_titanic_like).to_html()
        # We still expect overview/variables/association headers
        assert "Overview" in html
        assert "Variables" in html
        # No CATDAP-02 results means no Top subsets header
        assert "Top subsets" not in html


class TestQualityWarnings:
    """Quality warnings section is hidden when empty, shown when populated."""

    def test_warnings_visible_when_present(
        self, df_with_warnings: pd.DataFrame
    ) -> None:
        pytest.importorskip("jinja2")
        html = pycatdap.profile(df_with_warnings).to_html()
        # constant column triggers a warning
        assert "constant" in html.lower()
        # Should mention either "warning" or "quality" near the warnings block
        assert re.search(r"warning|quality", html, re.IGNORECASE)

    def test_warnings_section_omitted_when_empty(self) -> None:
        pytest.importorskip("jinja2")
        clean_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        html = pycatdap.profile(clean_df).to_html()
        # The "Quality warnings" header should NOT appear at all
        assert "Quality warnings" not in html


class TestSelfContained:
    """HTML is single-file, no external asset references."""

    def test_no_external_css_link(self, df_titanic_like: pd.DataFrame) -> None:
        pytest.importorskip("jinja2")
        html = pycatdap.profile(df_titanic_like).to_html()
        # rel="stylesheet" pointing to non-data URI = bad
        external_css = re.findall(
            r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\'](https?://[^"\']+)',
            html,
        )
        assert external_css == [], f"external CSS detected: {external_css}"

    def test_plotly_js_embedded_inline(self, df_titanic_like: pd.DataFrame) -> None:
        """Plotly.js main library must be inlined (Issue #14: offline-viewable).

        Note: the inlined plotly.js bundle includes third-party sub-libraries
        (e.g. maplibre) whose source contains incidental ``cdn.plot.ly``
        URLs. Those do not break offline viewability — only the absence of
        a top-level Plotly <script src="https://..."> would. We assert the
        positive side (Plotly is callable) and a substantial bundle size.
        """
        pytest.importorskip("jinja2")
        pytest.importorskip("plotly")
        html = pycatdap.profile(df_titanic_like).to_html()
        assert "Plotly.newPlot" in html or "Plotly.plot" in html
        # No <script src="...plotly..."> tag — that would mean CDN load.
        external_plotly = re.findall(
            r'<script[^>]+src=["\']([^"\']*plotly[^"\']*)["\']', html
        )
        assert external_plotly == [], (
            f"external plotly <script src=> detected: {external_plotly}"
        )
        # Inline bundle is multi-MB; sanity check that we are not running
        # in some accidental CDN mode.
        assert len(html) > 1_000_000, (
            f"HTML is only {len(html)} bytes; inline plotly should be > 1 MB"
        )


class TestAtomicWrite:
    """to_html(path) uses atomic write (consistent with H-0005 to_html)."""

    def test_atomic_write_used(
        self,
        df_titanic_like: pd.DataFrame,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        pytest.importorskip("jinja2")
        from pycatdap import _io

        calls: list[Path] = []
        original = _io.atomic_write_text

        def spy(path: str | Path, text: str, encoding: str = "utf-8") -> None:
            calls.append(Path(path))
            original(path, text, encoding=encoding)

        monkeypatch.setattr(_io, "atomic_write_text", spy)
        # ALSO patch the reference imported into profile module if any.
        import pycatdap.profile as profile_mod

        if hasattr(profile_mod, "atomic_write_text"):
            monkeypatch.setattr(profile_mod, "atomic_write_text", spy)

        path = tmp_path / "report.html"
        pycatdap.profile(df_titanic_like).to_html(path)

        assert path in calls, "atomic_write_text was not called"


class TestMissingJinja2:
    """When jinja2 is missing, to_html raises with an install hint."""

    def test_import_error_points_to_extras(
        self, df_titanic_like: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Simulate jinja2 absence by inserting a None entry in sys.modules.
        monkeypatch.setitem(sys.modules, "jinja2", None)
        result = pycatdap.profile(df_titanic_like)
        with pytest.raises(ImportError, match=r"pycatdap\[plotly\]"):
            result.to_html()
