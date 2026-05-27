"""Internal I/O helpers.

Public report writers (`DescribeResult.to_html`, `TargetSummary.to_html`, and
future `profile()` / `error_analysis()` outputs) need to be safe against
concurrent readers — for example a `mkdocs serve` watcher polling the file
while pycatdap rewrites it. `Path.write_text` is NOT atomic; a reader that
opens the file mid-write observes an empty or partial document.

This module centralizes the tmp-file + ``os.replace`` pattern so every
public writer can adopt it without duplicating the logic.
"""

from __future__ import annotations

import os
from pathlib import Path


def atomic_write_text(path: str | Path, text: str, encoding: str = "utf-8") -> None:
    """Write ``text`` to ``path`` atomically.

    Concurrent readers observe either the prior content or the new content,
    never an empty intermediate state. Implemented as ``write to .tmp``
    followed by :func:`os.replace`, which is atomic on POSIX (rename(2)) and
    Windows (MoveFileEx with REPLACE_EXISTING).

    Parameters
    ----------
    path : str or Path
        Destination file path. Parent directory is created if missing.
    text : str
        Content to write.
    encoding : str
        Text encoding, default ``"utf-8"``.

    Notes
    -----
    The temporary file is placed in the same directory as the destination
    (named ``<dest>.tmp``) to ensure ``os.replace`` is a same-filesystem
    rename. Cross-device renames are not atomic on POSIX.
    """
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(text, encoding=encoding)
    os.replace(tmp, dest)


__all__ = ["atomic_write_text"]
