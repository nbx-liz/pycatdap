"""Tests for core AIC computation."""

from __future__ import annotations

from unittest.mock import patch

import numpy as np
import pytest

from pycatdap._aic import (
    _safe_xlogy,
    compute_aic_twoway,
    compute_base_aic,
    compute_delta_aic,
)

# ---------------------------------------------------------------------------
# _safe_xlogy
# ---------------------------------------------------------------------------


class TestSafeXlogy:
    """Tests for the 0*ln(0)=0 safe log helper."""

    def test_zero_frequency_returns_zero(self) -> None:
        """0 * ln(0) must equal 0 (CATDAP convention)."""
        result = _safe_xlogy(np.array([0.0]), np.array([0.0]))
        assert result[0] == 0.0

    def test_zero_x_positive_y(self) -> None:
        """0 * ln(y) = 0 for any positive y."""
        result = _safe_xlogy(np.array([0.0]), np.array([5.0]))
        assert result[0] == 0.0

    def test_normal_values(self) -> None:
        """x * ln(y) for standard positive values."""
        x = np.array([2.0, 3.0])
        y = np.array([4.0, 5.0])
        expected = x * np.log(y)
        np.testing.assert_allclose(_safe_xlogy(x, y), expected)

    def test_scalar_inputs(self) -> None:
        """Should work with scalar-like 0-d arrays."""
        x = np.array(3.0)
        y = np.array(2.0)
        result = _safe_xlogy(x, y)
        np.testing.assert_allclose(result, 3.0 * np.log(2.0))

    def test_without_scipy(self) -> None:
        """Fallback path when scipy is not installed.

        Note: This test verifies the function's *contract* (correct values
        including 0*ln(0)=0) rather than proving which code path is used,
        since the try/except branch is resolved at import time.
        """
        with patch.dict("sys.modules", {"scipy": None, "scipy.special": None}):
            x = np.array([0.0, 2.0, 3.0])
            y = np.array([0.0, 4.0, 5.0])
            result = _safe_xlogy(x, y)
            expected = np.array([0.0, 2.0 * np.log(4.0), 3.0 * np.log(5.0)])
            np.testing.assert_allclose(result, expected)


# ---------------------------------------------------------------------------
# compute_aic_twoway
# ---------------------------------------------------------------------------


class TestComputeAicTwoway:
    """Tests for AIC(E; F) computation on a two-way table."""

    def test_2x2_table(self) -> None:
        """Hand-computed 2x2 table.

        cross_freq = [[10, 20],
                      [30, 40]]
        marginal_f = [40, 60]
        C_E=2, C_F=2
        AIC = -2 * sum(n_ij * ln(n_ij / n_j)) + 2*(C_E-1)*C_F
        """
        cross = np.array([[10.0, 20.0], [30.0, 40.0]])
        marg_f = np.array([40.0, 60.0])

        loglik = (
            10 * np.log(10 / 40)
            + 20 * np.log(20 / 60)
            + 30 * np.log(30 / 40)
            + 40 * np.log(40 / 60)
        )
        expected = -2 * loglik + 2 * (2 - 1) * 2

        result = compute_aic_twoway(cross, marg_f)
        np.testing.assert_allclose(result, expected, rtol=1e-10)

    def test_3x4_with_zero_cells(self) -> None:
        """Table with zero-frequency cells — must not produce NaN/Inf."""
        cross = np.array(
            [
                [5.0, 0.0, 10.0, 3.0],
                [0.0, 8.0, 0.0, 7.0],
                [15.0, 2.0, 0.0, 0.0],
            ]
        )
        marg_f = cross.sum(axis=0)

        result = compute_aic_twoway(cross, marg_f)
        assert np.isfinite(result)

    def test_uniform_distribution(self) -> None:
        """Uniform cross frequencies should yield a valid finite AIC."""
        cross = np.full((3, 4), 10.0)
        marg_f = cross.sum(axis=0)

        result = compute_aic_twoway(cross, marg_f)
        assert np.isfinite(result)

    def test_single_response_category(self) -> None:
        """C_E = 1: penalty should be 0, result finite."""
        cross = np.array([[10.0, 20.0, 30.0]])
        marg_f = cross.sum(axis=0)

        result = compute_aic_twoway(cross, marg_f)
        # penalty = 2 * (1-1) * 3 = 0
        # log-likelihood: sum(n_ij * ln(n_ij/n_j)) = sum(n_ij * ln(1)) = 0
        assert result == 0.0

    def test_empty_table_raises(self) -> None:
        """All-zero table should raise ValueError."""
        cross = np.zeros((2, 3))
        marg_f = np.zeros(3)

        with pytest.raises(ValueError, match="at least one observation"):
            compute_aic_twoway(cross, marg_f)

    def test_input_not_mutated(self) -> None:
        """Input arrays must not be modified."""
        cross = np.array([[10.0, 20.0], [30.0, 40.0]])
        marg_f = np.array([40.0, 60.0])
        cross_copy = cross.copy()
        marg_f_copy = marg_f.copy()

        compute_aic_twoway(cross, marg_f)

        np.testing.assert_array_equal(cross, cross_copy)
        np.testing.assert_array_equal(marg_f, marg_f_copy)


# ---------------------------------------------------------------------------
# compute_base_aic
# ---------------------------------------------------------------------------


class TestComputeBaseAic:
    """Tests for AIC(E; phi) — null model."""

    def test_uniform_marginal(self) -> None:
        """Uniform marginal: each category has n/C_E observations.

        marginal_e = [25, 25, 25, 25], n = 100
        AIC = -2 * sum(25 * ln(25/100)) + 2*(4-1)
            = -2 * 4 * 25 * ln(0.25) + 6
        """
        marg_e = np.array([25.0, 25.0, 25.0, 25.0])
        n = 100

        loglik = 4 * 25 * np.log(25 / 100)
        expected = -2 * loglik + 2 * (4 - 1)

        result = compute_base_aic(marg_e, n)
        np.testing.assert_allclose(result, expected, rtol=1e-10)

    def test_skewed_marginal(self) -> None:
        """Skewed marginal: [90, 5, 5], n=100."""
        marg_e = np.array([90.0, 5.0, 5.0])
        n = 100

        loglik = 90 * np.log(90 / 100) + 5 * np.log(5 / 100) + 5 * np.log(5 / 100)
        expected = -2 * loglik + 2 * (3 - 1)

        result = compute_base_aic(marg_e, n)
        np.testing.assert_allclose(result, expected, rtol=1e-10)

    def test_two_categories(self) -> None:
        """Binary outcome: marginal_e = [60, 40], n=100."""
        marg_e = np.array([60.0, 40.0])
        n = 100

        loglik = 60 * np.log(60 / 100) + 40 * np.log(40 / 100)
        expected = -2 * loglik + 2 * (2 - 1)

        result = compute_base_aic(marg_e, n)
        np.testing.assert_allclose(result, expected, rtol=1e-10)

    def test_single_category(self) -> None:
        """C_E = 1: penalty is 0, log-likelihood is n*ln(1) = 0."""
        marg_e = np.array([100.0])
        result = compute_base_aic(marg_e, 100)
        assert result == 0.0

    def test_zero_n_raises(self) -> None:
        """n = 0 should raise ValueError."""
        marg_e = np.array([0.0, 0.0])
        with pytest.raises(ValueError, match="n must be positive"):
            compute_base_aic(marg_e, 0)

    def test_input_not_mutated(self) -> None:
        marg_e = np.array([50.0, 50.0])
        marg_e_copy = marg_e.copy()

        compute_base_aic(marg_e, 100)

        np.testing.assert_array_equal(marg_e, marg_e_copy)


# ---------------------------------------------------------------------------
# compute_delta_aic
# ---------------------------------------------------------------------------


class TestComputeDeltaAic:
    """Tests for ΔAIC = AIC(E;F) - AIC(E;φ)."""

    def test_independent_vars_nonnegative(self) -> None:
        """Independent variables should yield ΔAIC ≈ penalty term (>= 0).

        When E and F are independent, the conditional distribution equals the
        marginal, so the log-likelihood difference is ~0 and ΔAIC ≈ 2*(C_E-1)*(C_F-1).
        """
        rng = np.random.default_rng(42)
        n = 10000
        e = rng.choice(3, size=n)
        f = rng.choice(4, size=n)

        cross = np.zeros((3, 4))
        np.add.at(cross, (e, f), 1)

        marg_e = cross.sum(axis=1)
        marg_f = cross.sum(axis=0)

        delta = compute_delta_aic(cross, marg_e, marg_f, n)
        # For independent variables, delta should be near +2*(C_E-1)*(C_F-1)
        # which is 2*2*3=12, but stochastic — just check non-negative-ish
        assert delta > -1.0

    def test_perfect_association_negative(self) -> None:
        """Perfect association: each F category maps to exactly one E category.

        cross = [[50,  0,  0],
                 [ 0, 50,  0],
                 [ 0,  0, 50]]
        ΔAIC should be strongly negative.
        """
        cross = np.diag([50.0, 50.0, 50.0])
        marg_e = np.array([50.0, 50.0, 50.0])
        marg_f = np.array([50.0, 50.0, 50.0])
        n = 150

        delta = compute_delta_aic(cross, marg_e, marg_f, n)
        assert delta < -10.0

    def test_equals_twoway_minus_base(self) -> None:
        """ΔAIC must equal compute_aic_twoway - compute_base_aic."""
        cross = np.array([[10.0, 20.0], [30.0, 40.0]])
        marg_e = cross.sum(axis=1)
        marg_f = cross.sum(axis=0)
        n = int(cross.sum())

        delta = compute_delta_aic(cross, marg_e, marg_f, n)
        twoway = compute_aic_twoway(cross, marg_f)
        base = compute_base_aic(marg_e, n)

        np.testing.assert_allclose(delta, twoway - base, rtol=1e-10)

    def test_input_not_mutated(self) -> None:
        cross = np.array([[10.0, 20.0], [30.0, 40.0]])
        marg_e = cross.sum(axis=1).copy()
        marg_f = cross.sum(axis=0).copy()
        cross_copy = cross.copy()
        marg_e_copy = marg_e.copy()
        marg_f_copy = marg_f.copy()

        compute_delta_aic(cross, marg_e, marg_f, 100)

        np.testing.assert_array_equal(cross, cross_copy)
        np.testing.assert_array_equal(marg_e, marg_e_copy)
        np.testing.assert_array_equal(marg_f, marg_f_copy)
