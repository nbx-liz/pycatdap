"""catdap2 (AIC subset search) scaling benchmarks.

Scales rows and column count over a mixed categorical/continuous frame.
``nvar`` is pinned to a small constant so the multi-variable subset search stays
bounded — with ``nvar=None`` catdap2 searches every combination of all columns
(2^cols), which would explode at 10+ columns.
"""

from __future__ import annotations

import pytest
from _data import make_mixed

from pycatdap import catdap2

_NVAR = 5


@pytest.mark.parametrize("n_cols", [5, 10])
@pytest.mark.parametrize("n_rows", [100, 1_000, 10_000])
def test_catdap2_mixed(benchmark, n_rows: int, n_cols: int) -> None:
    df, pool = make_mixed(n_rows, n_cols=n_cols)
    result = benchmark(catdap2, df, pool=pool, response_name="response", nvar=_NVAR)
    # aic is a long-format frame: one row per explanatory variable (response
    # excluded), columns ["variable", "aic"].
    assert list(result.aic.columns) == ["variable", "aic"]
    assert len(result.aic) == n_cols - 1
