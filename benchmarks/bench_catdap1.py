"""catdap1 (pairwise categorical AIC) scaling benchmarks.

Scales the row count over a fixed 10-column all-categorical frame. The default
``catdap1(df)`` call treats every column as a response in turn, exercising the
full O(cols^2) crosstab + AIC path.
"""

from __future__ import annotations

import pytest
from _data import make_categorical

from pycatdap import catdap1

_N_COLS = 10


@pytest.mark.parametrize("n_rows", [100, 1_000, 10_000, 100_000])
def test_catdap1_categorical(benchmark, n_rows: int) -> None:
    df = make_categorical(n_rows, n_cols=_N_COLS)
    result = benchmark(catdap1, df)
    # Default all-response call yields a (response x explanatory) ΔAIC matrix:
    # the full O(cols^2) path was exercised.
    assert result.aic.shape == (_N_COLS, _N_COLS)
