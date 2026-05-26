"""Tests for pycatdap._io.atomic_write_text."""

from __future__ import annotations

import threading
from pathlib import Path

import pytest

from pycatdap._io import atomic_write_text


class TestAtomicWriteText:
    def test_writes_file_with_content(self, tmp_path: Path) -> None:
        dest = tmp_path / "out.html"
        atomic_write_text(dest, "hello")
        assert dest.read_text() == "hello"

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        dest = tmp_path / "nested" / "dir" / "out.html"
        atomic_write_text(dest, "hello")
        assert dest.exists()
        assert dest.read_text() == "hello"

    def test_overwrites_existing_file(self, tmp_path: Path) -> None:
        dest = tmp_path / "out.html"
        dest.write_text("old content")
        atomic_write_text(dest, "new content")
        assert dest.read_text() == "new content"

    def test_no_tmp_leftover_after_success(self, tmp_path: Path) -> None:
        dest = tmp_path / "out.html"
        atomic_write_text(dest, "hello")
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        assert not tmp.exists(), "temporary file should be renamed away"

    def test_accepts_string_path(self, tmp_path: Path) -> None:
        dest = str(tmp_path / "out.html")
        atomic_write_text(dest, "hello")
        assert Path(dest).read_text() == "hello"

    def test_encoding_round_trip_utf8(self, tmp_path: Path) -> None:
        dest = tmp_path / "utf8.html"
        atomic_write_text(dest, "東京 × Tōkyō")
        assert dest.read_text(encoding="utf-8") == "東京 × Tōkyō"

    def test_concurrent_readers_never_see_empty(self, tmp_path: Path) -> None:
        """The point of atomicity: readers see prior OR new content, never empty.

        With non-atomic ``Path.write_text`` this test would frequently observe
        empty reads. With ``os.replace`` the rename is atomic and readers
        always see one of the two complete states.
        """
        dest = tmp_path / "concurrent.html"
        dest.write_text("INITIAL")
        new_content = "X" * 4096  # large enough to make non-atomic write slow

        empty_observations = []
        stop_event = threading.Event()

        def reader() -> None:
            while not stop_event.is_set():
                try:
                    content = dest.read_text()
                except FileNotFoundError:
                    continue
                if content == "":
                    empty_observations.append(True)

        readers = [threading.Thread(target=reader) for _ in range(4)]
        for r in readers:
            r.start()

        try:
            for _ in range(100):
                atomic_write_text(dest, new_content)
        finally:
            stop_event.set()
            for r in readers:
                r.join(timeout=2.0)

        assert empty_observations == [], (
            f"Atomic write should never expose an empty file, "
            f"got {len(empty_observations)} empty reads"
        )


class TestPublicWritersAreAtomic:
    """Smoke tests confirming the public to_html writers use the atomic helper."""

    def test_describe_to_html_atomic(self, tmp_path: Path) -> None:
        import pandas as pd

        import pycatdap

        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        out = tmp_path / "describe.html"
        pycatdap.describe(df).to_html(path=out)
        # No leftover .tmp
        tmp = out.with_suffix(out.suffix + ".tmp")
        assert not tmp.exists()
        assert out.read_text().startswith("<!DOCTYPE html>")

    def test_target_summary_to_html_atomic(self, tmp_path: Path) -> None:
        import pandas as pd

        import pycatdap

        df = pd.DataFrame(
            {
                "y": ["a", "b", "a", "b", "a", "b"] * 10,
                "x": ["p", "q", "p", "q", "p", "q"] * 10,
            }
        )
        out = tmp_path / "target.html"
        pycatdap.target_summary(df, target="y", explanatory="x").to_html(path=out)
        tmp = out.with_suffix(out.suffix + ".tmp")
        assert not tmp.exists()
        assert out.read_text().startswith("<!DOCTYPE html>")


@pytest.mark.parametrize("size", [0, 1, 100, 10_000])
def test_atomic_write_various_sizes(tmp_path: Path, size: int) -> None:
    dest = tmp_path / f"size_{size}.txt"
    content = "X" * size
    atomic_write_text(dest, content)
    assert dest.read_text() == content
