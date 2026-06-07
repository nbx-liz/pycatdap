"""discover_error_slices benchmark on an Adult-Income-like synthetic frame.

This is the #20 acceptance scenario (CATDAP-02 on a 14-column dataset). It is
HARD-BOUNDED and marked ``slow``: ``max_vars=2``, a capped ``max_candidates``,
and a 5k-row subsample keep it far from the OOM regime that unbounded discovery
on the full Adult Income hit (memory ``incident_discover_slices_oom``). A
synthetic frame is used instead of ``fetch_adult_income`` to avoid OpenML
network-timing variance (memory ``feedback_make_ci_d4_network_hang``).
"""

from __future__ import annotations

import pytest
from _data import make_adult_like

from pycatdap.error import discover_error_slices

_MAX_VARS = 2
_MAX_CANDIDATES = 50_000
_TOP_K = 10


@pytest.mark.slow
def test_discover_error_slices_adult_like(benchmark) -> None:
    df, y_true, y_pred = make_adult_like(n_rows=5_000)
    result = benchmark(
        discover_error_slices,
        df,
        y_true,
        y_pred,
        max_vars=_MAX_VARS,
        top_k=_TOP_K,
        max_candidates=_MAX_CANDIDATES,
    )
    assert result.n_total == 5_000
    assert not result.truncated
