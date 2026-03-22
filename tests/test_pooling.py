"""Tests for continuous variable pooling."""

from __future__ import annotations

import numpy as np
import pytest

from pycatdap._pooling import (
    PoolingResult,
    equal_pooling,
    optimal_binning,
    unequal_pooling,
)

# ---------------------------------------------------------------------------
# Helper to create response arrays aligned with continuous values
# ---------------------------------------------------------------------------


def _make_bimodal_data(
    n: int = 200,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Two groups: values < 5 map to response 'a', values >= 5 to 'b'."""
    rng = np.random.default_rng(seed)
    values = np.concatenate([rng.uniform(0, 5, n // 2), rng.uniform(5, 10, n // 2)])
    response = np.array(["a"] * (n // 2) + ["b"] * (n // 2))
    return values, response


def _make_monotone_data(
    n: int = 300,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Monotonically related: low values → 'x', mid → 'y', high → 'z'."""
    rng = np.random.default_rng(seed)
    values = rng.uniform(0, 30, n)
    response = np.where(values < 10, "x", np.where(values < 20, "y", "z"))
    return values, response


# ---------------------------------------------------------------------------
# PoolingResult
# ---------------------------------------------------------------------------


class TestPoolingResult:
    """Tests for the PoolingResult container."""

    def test_result_fields(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        assert isinstance(result, PoolingResult)
        assert isinstance(result.codes, np.ndarray)
        assert isinstance(result.boundaries, list)

    def test_codes_length_matches_input(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        assert len(result.codes) == len(values)

    def test_codes_are_nonnegative_ints(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        assert np.all(result.codes >= 0)
        assert result.codes.dtype == np.intp or np.issubdtype(
            result.codes.dtype, np.integer
        )

    def test_boundaries_sorted(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        assert result.boundaries == sorted(result.boundaries)

    def test_boundaries_within_data_range(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        if result.boundaries:
            assert result.boundaries[0] >= values.min()
            assert result.boundaries[-1] <= values.max()


# ---------------------------------------------------------------------------
# equal_pooling
# ---------------------------------------------------------------------------


class TestEqualPooling:
    """Tests for top-down equal-interval pooling (pool=0)."""

    def test_returns_pooling_result(self) -> None:
        values, response = _make_bimodal_data()
        result = equal_pooling(values, response, accuracy=1.0)
        assert isinstance(result, PoolingResult)

    def test_bimodal_finds_split(self) -> None:
        """Bimodal data should find at least one boundary near 5."""
        values, response = _make_bimodal_data()
        result = equal_pooling(values, response, accuracy=1.0)
        assert len(result.boundaries) >= 1
        # At least one boundary near the split point
        near_five = any(3.0 <= b <= 7.0 for b in result.boundaries)
        assert near_five

    def test_all_same_value_single_bin(self) -> None:
        """All identical values should produce a single bin."""
        values = np.full(50, 3.0)
        response = np.array(["a"] * 25 + ["b"] * 25)
        result = equal_pooling(values, response, accuracy=1.0)
        assert len(set(result.codes)) == 1

    def test_input_not_mutated(self) -> None:
        values, response = _make_bimodal_data()
        v_copy, r_copy = values.copy(), response.copy()
        equal_pooling(values, response, accuracy=1.0)
        np.testing.assert_array_equal(values, v_copy)
        np.testing.assert_array_equal(response, r_copy)


# ---------------------------------------------------------------------------
# unequal_pooling
# ---------------------------------------------------------------------------


class TestUnequalPooling:
    """Tests for bottom-up unequal-interval pooling (pool=1)."""

    def test_returns_pooling_result(self) -> None:
        values, response = _make_bimodal_data()
        result = unequal_pooling(values, response, accuracy=1.0)
        assert isinstance(result, PoolingResult)

    def test_bimodal_finds_two_groups(self) -> None:
        """Clear bimodal structure should produce ~2 bins."""
        values, response = _make_bimodal_data()
        result = unequal_pooling(values, response, accuracy=1.0)
        n_bins = len(set(result.codes))
        # Should collapse to a small number of bins
        assert 2 <= n_bins <= 5

    def test_monotone_preserves_ordering(self) -> None:
        """Monotone response should produce ordered bins."""
        values, response = _make_monotone_data()
        result = unequal_pooling(values, response, accuracy=1.0)
        # Boundaries should be sorted
        assert result.boundaries == sorted(result.boundaries)

    def test_all_same_value_single_bin(self) -> None:
        values = np.full(50, 7.0)
        response = np.array(["a"] * 25 + ["b"] * 25)
        result = unequal_pooling(values, response, accuracy=1.0)
        assert len(set(result.codes)) == 1

    def test_input_not_mutated(self) -> None:
        values, response = _make_bimodal_data()
        v_copy, r_copy = values.copy(), response.copy()
        unequal_pooling(values, response, accuracy=1.0)
        np.testing.assert_array_equal(values, v_copy)
        np.testing.assert_array_equal(response, r_copy)


# ---------------------------------------------------------------------------
# optimal_binning (dispatch)
# ---------------------------------------------------------------------------


class TestOptimalBinning:
    """Tests for the public dispatch function."""

    def test_default_is_bottom_up(self) -> None:
        """Default method should be 'bottom_up' (unequal pooling)."""
        values, response = _make_bimodal_data()
        result_default = optimal_binning(values, response, accuracy=1.0)
        result_bu = unequal_pooling(values, response, accuracy=1.0)
        np.testing.assert_array_equal(result_default.codes, result_bu.codes)
        assert result_default.boundaries == result_bu.boundaries

    def test_top_down_dispatches(self) -> None:
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response, method="top_down", accuracy=1.0)
        assert isinstance(result, PoolingResult)

    def test_invalid_method_raises(self) -> None:
        values, response = _make_bimodal_data()
        with pytest.raises(ValueError, match="method"):
            optimal_binning(values, response, method="invalid", accuracy=1.0)

    def test_auto_accuracy(self) -> None:
        """When accuracy is None, should auto-detect from data."""
        values, response = _make_bimodal_data()
        result = optimal_binning(values, response)
        assert isinstance(result, PoolingResult)
        assert len(result.codes) == len(values)

    def test_codes_cover_all_observations(self) -> None:
        values, response = _make_monotone_data()
        result = optimal_binning(values, response, accuracy=1.0)
        # Every observation must be assigned a bin
        assert not np.any(np.isnan(result.codes.astype(float)))
        assert len(result.codes) == len(values)
