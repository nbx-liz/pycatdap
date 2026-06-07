"""Shared pytest configuration for the benchmark suite.

Benchmarks live OUTSIDE ``testpaths`` (= ``["tests"]``) and run only via
``make bench``; ``make test`` / ``make ci`` never collect this directory. With
pytest's default (prepend) import mode and no ``__init__.py`` here, the
``benchmarks/`` directory is placed on ``sys.path`` when this package is
collected, so the ``bench_*`` modules can import the sibling ``_data`` helpers.
"""

from __future__ import annotations
