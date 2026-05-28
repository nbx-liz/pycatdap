"""Tests for :mod:`pycatdap.measures` (H-0008 PR-D4).

Three standard measures (``aic`` / ``cramers_v`` / ``mutual_info``)
plus a tiny registry (``register`` / ``get`` / ``list_measures``) for
pluggable interestingness measures (DP-6).

Each measure has the same signature: ``f(cross_freq: np.ndarray) ->
float``. The registry stores the three standards at import time so
:func:`pycatdap.measures.get` can look them up by name.
"""

from __future__ import annotations

import numpy as np
import pytest

from pycatdap import measures

# -- Test data --------------------------------------------------------------


@pytest.fixture()
def independent_table() -> np.ndarray:
    """A 2x2 table with row and column independence (rank-1)."""
    # P(row=0) = 0.5, P(col=0) = 0.5 → cells are n * 0.25 each
    return np.array([[25.0, 25.0], [25.0, 25.0]])


@pytest.fixture()
def perfect_table() -> np.ndarray:
    """A 2x2 table with perfect association (diagonal-only)."""
    return np.array([[50.0, 0.0], [0.0, 50.0]])


@pytest.fixture()
def moderate_table() -> np.ndarray:
    """A 2x3 table with a moderate but non-extreme association."""
    return np.array([[20.0, 10.0, 5.0], [5.0, 10.0, 20.0]])


# -- aic --------------------------------------------------------------------


def test_aic_returns_float(independent_table: np.ndarray) -> None:
    val = measures.aic(independent_table)
    assert isinstance(val, float)


def test_aic_is_positive_for_independent_table(
    independent_table: np.ndarray,
) -> None:
    # An exactly independent table pays the model-complexity penalty
    # without recouping any log-likelihood, so delta AIC > 0.
    assert measures.aic(independent_table) > 0


def test_aic_is_negative_for_perfect_association(
    perfect_table: np.ndarray,
) -> None:
    # A perfectly informative explanatory variable beats the null model.
    assert measures.aic(perfect_table) < 0


def test_aic_rejects_one_dimensional_input() -> None:
    with pytest.raises(ValueError, match="2D"):
        measures.aic(np.array([1.0, 2.0, 3.0]))


def test_aic_rejects_empty_table() -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        measures.aic(np.zeros((2, 2)))


# -- cramers_v --------------------------------------------------------------


def test_cramers_v_zero_for_independent_table(
    independent_table: np.ndarray,
) -> None:
    assert measures.cramers_v(independent_table) == pytest.approx(0.0)


def test_cramers_v_one_for_perfect_association(
    perfect_table: np.ndarray,
) -> None:
    assert measures.cramers_v(perfect_table) == pytest.approx(1.0)


def test_cramers_v_in_unit_range(moderate_table: np.ndarray) -> None:
    v = measures.cramers_v(moderate_table)
    assert 0.0 < v < 1.0


def test_cramers_v_returns_zero_for_degenerate_shape() -> None:
    # 1xN or Nx1 has denom min(r-1, c-1) == 0 — return 0 not NaN
    single_row = np.array([[10.0, 20.0, 30.0]])
    assert measures.cramers_v(single_row) == 0.0


def test_cramers_v_rejects_one_dimensional_input() -> None:
    with pytest.raises(ValueError, match="2D"):
        measures.cramers_v(np.array([1.0, 2.0, 3.0]))


def test_cramers_v_rejects_empty_table() -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        measures.cramers_v(np.zeros((2, 2)))


# -- mutual_info ------------------------------------------------------------


def test_mutual_info_zero_for_independent_table(
    independent_table: np.ndarray,
) -> None:
    assert measures.mutual_info(independent_table) == pytest.approx(0.0)


def test_mutual_info_positive_for_perfect_association(
    perfect_table: np.ndarray,
) -> None:
    # I(X;Y) = H(X) for a perfect mapping; for a 2x2 balanced table
    # H(X) = ln(2) ≈ 0.693 nats.
    assert measures.mutual_info(perfect_table) == pytest.approx(np.log(2), rel=1e-9)


def test_mutual_info_positive_for_moderate_association(
    moderate_table: np.ndarray,
) -> None:
    assert measures.mutual_info(moderate_table) > 0


def test_mutual_info_handles_zero_cells() -> None:
    # zero cells must not break the log(p/(p_i*p_j)) computation
    table = np.array([[10.0, 0.0], [0.0, 10.0]])
    val = measures.mutual_info(table)
    assert val == pytest.approx(np.log(2), rel=1e-9)


def test_mutual_info_rejects_one_dimensional_input() -> None:
    with pytest.raises(ValueError, match="2D"):
        measures.mutual_info(np.array([1.0, 2.0, 3.0]))


def test_mutual_info_rejects_empty_table() -> None:
    with pytest.raises(ValueError, match="at least one observation"):
        measures.mutual_info(np.zeros((2, 2)))


# -- registry ---------------------------------------------------------------


def test_standard_measures_pre_registered() -> None:
    """The three built-ins must be reachable via the registry on import."""
    assert measures.get("aic") is measures.aic
    assert measures.get("cramers_v") is measures.cramers_v
    assert measures.get("mutual_info") is measures.mutual_info


def test_list_measures_includes_standards() -> None:
    names = set(measures.list_measures())
    assert {"aic", "cramers_v", "mutual_info"} <= names


def test_register_and_get_round_trip() -> None:
    """User can register a custom measure and look it up."""

    def my_measure(cf: np.ndarray) -> float:
        return float(cf.sum())

    measures.register("__test_my_measure", my_measure)
    try:
        assert measures.get("__test_my_measure") is my_measure
        assert "__test_my_measure" in measures.list_measures()
    finally:
        # Cleanup so tests stay independent. unregister is intentionally
        # NOT a public API — tests use direct dict access for hygiene.
        measures._registry._REGISTRY.pop("__test_my_measure", None)


def test_get_unknown_measure_raises_key_error() -> None:
    with pytest.raises(KeyError, match="not registered"):
        measures.get("__not_a_real_measure")


def test_register_overwrites_existing_name() -> None:
    """Re-registering a name silently overwrites the previous binding."""

    def first(cf: np.ndarray) -> float:
        return 1.0

    def second(cf: np.ndarray) -> float:
        return 2.0

    measures.register("__overwrite_me", first)
    measures.register("__overwrite_me", second)
    try:
        assert measures.get("__overwrite_me") is second
    finally:
        measures._registry._REGISTRY.pop("__overwrite_me", None)


def test_public_subpackage_re_export() -> None:
    import pycatdap

    assert pycatdap.measures is measures
