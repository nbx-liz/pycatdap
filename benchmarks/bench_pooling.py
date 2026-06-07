"""optimal_binning (AIC-optimal continuous binning) scaling benchmarks.

Scales the row count for the default bottom-up (unequal pooling) method, the
hot path used by catdap2 and slice discovery to discretise continuous columns.
"""

from __future__ import annotations

import pytest
from _data import make_continuous_response

from pycatdap._pooling import optimal_binning


@pytest.mark.parametrize("n_rows", [1_000, 10_000, 100_000])
def test_optimal_binning_bottom_up(benchmark, n_rows: int) -> None:
    values, response = make_continuous_response(n_rows)
    result = benchmark(optimal_binning, values, response)
    assert result.codes.shape[0] == n_rows
