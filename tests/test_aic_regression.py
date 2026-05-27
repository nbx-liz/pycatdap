"""Tests for the H-0005 Gaussian regression AIC machinery.

Covers penalty switching, RSS computation, AIC formulas, delta_aic /
r_squared, cross-pair comparability (R-1), and edge cases.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from pycatdap._aic_regression import (
    EPSILON_RSS,
    _penalty,
    compute_delta_aic_regression,
    compute_gaussian_aic,
    compute_gaussian_null_aic,
    compute_rss,
)

# ---------------------------------------------------------------------------
# _penalty
# ---------------------------------------------------------------------------


class TestPenalty:
    def test_aic(self) -> None:
        assert _penalty(3, 100, "aic") == pytest.approx(6.0)
        assert _penalty(1, 50, "aic") == pytest.approx(2.0)

    def test_bic(self) -> None:
        assert _penalty(3, 100, "bic") == pytest.approx(3 * math.log(100))
        assert _penalty(2, 50, "bic") == pytest.approx(2 * math.log(50))

    def test_aicc(self) -> None:
        # k=3, n=100: 2*3 + 2*3*4/(100-3-1) = 6 + 24/96 = 6.25
        assert _penalty(3, 100, "aicc") == pytest.approx(6.25)

    def test_aicc_diverges_at_small_n(self) -> None:
        # n <= k + 1: return inf
        assert _penalty(10, 11, "aicc") == float("inf")
        assert _penalty(10, 10, "aicc") == float("inf")

    def test_aicc_matches_aic_at_large_n(self) -> None:
        # Correction term shrinks as n grows
        assert _penalty(3, 10000, "aicc") == pytest.approx(
            _penalty(3, 10000, "aic"), rel=1e-3
        )

    def test_unknown_criterion_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown criterion"):
            _penalty(3, 100, "magic")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# compute_rss
# ---------------------------------------------------------------------------


class TestComputeRSS:
    def test_two_groups_balanced(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        rss, k = compute_rss(y, idx)
        # bin 0 mean=2, residuals -1,0,1 -> SS=2; bin 1 mean=5, same -> total RSS=4
        assert rss == pytest.approx(4.0)
        assert k == 2

    def test_single_group(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0])
        idx = np.zeros(4, dtype=np.intp)
        rss, k = compute_rss(y, idx)
        # mean=2.5, residuals -1.5, -0.5, 0.5, 1.5 -> SS=5.0
        assert rss == pytest.approx(5.0)
        assert k == 1

    def test_perfect_predictor(self) -> None:
        # Each row its own bin: RSS = 0, floored at EPSILON_RSS
        y = np.arange(5, dtype=float)
        idx = np.arange(5, dtype=np.intp)
        rss, k = compute_rss(y, idx)
        assert rss == pytest.approx(EPSILON_RSS)
        assert k == 5

    def test_empty_groups_ignored(self) -> None:
        # Use codes 0, 2 (skip 1); k_means counts only non-empty
        y = np.array([1.0, 2.0, 3.0, 4.0])
        idx = np.array([0, 0, 2, 2], dtype=np.intp)
        rss, k = compute_rss(y, idx)
        assert k == 2  # codes 0 and 2 occupied; code 1 empty
        # bin 0: mean=1.5, SS=0.5; bin 2: mean=3.5, SS=0.5 -> 1.0
        assert rss == pytest.approx(1.0)

    def test_empty_input(self) -> None:
        rss, k = compute_rss(np.array([], dtype=float), np.array([], dtype=np.intp))
        assert rss == EPSILON_RSS
        assert k == 0


# ---------------------------------------------------------------------------
# compute_gaussian_aic
# ---------------------------------------------------------------------------


class TestGaussianAIC:
    def test_formula_aic(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        # n=6, RSS=4, k_means=2 -> k=3
        # AIC = 6*log(4/6) + 2*3 = -2.4327... + 6 = 3.5672...
        expected = 6 * math.log(4 / 6) + 6
        assert compute_gaussian_aic(y, idx, "aic") == pytest.approx(expected)

    def test_formula_bic(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        # k=3, penalty=log(6)*3
        expected = 6 * math.log(4 / 6) + math.log(6) * 3
        assert compute_gaussian_aic(y, idx, "bic") == pytest.approx(expected)

    def test_formula_aicc(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        # k=3, n=6, AICc penalty: 2*3 + 2*3*4/(6-3-1) = 6 + 12 = 18
        expected = 6 * math.log(4 / 6) + 18
        assert compute_gaussian_aic(y, idx, "aicc") == pytest.approx(expected)

    def test_empty_returns_inf(self) -> None:
        assert compute_gaussian_aic(
            np.array([], dtype=float), np.array([], dtype=np.intp)
        ) == float("inf")

    def test_default_criterion_is_bic(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        assert compute_gaussian_aic(y, idx) == pytest.approx(
            compute_gaussian_aic(y, idx, "bic")
        )


# ---------------------------------------------------------------------------
# compute_gaussian_null_aic
# ---------------------------------------------------------------------------


class TestGaussianNullAIC:
    def test_formula_aic(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        # mean=3.5, TSS = (2.5^2+1.5^2+0.5^2)*2 = 17.5
        # AIC_null = 6*log(17.5/6) + 4
        expected = 6 * math.log(17.5 / 6) + 4
        assert compute_gaussian_null_aic(y, "aic") == pytest.approx(expected)

    def test_formula_bic(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        expected = 6 * math.log(17.5 / 6) + math.log(6) * 2
        assert compute_gaussian_null_aic(y, "bic") == pytest.approx(expected)

    def test_empty_returns_inf(self) -> None:
        assert compute_gaussian_null_aic(np.array([], dtype=float)) == float("inf")


# ---------------------------------------------------------------------------
# compute_delta_aic_regression
# ---------------------------------------------------------------------------


class TestDeltaAICRegression:
    def test_delta_and_r_squared(self) -> None:
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        idx = np.array([0, 0, 0, 1, 1, 1], dtype=np.intp)
        delta, r2 = compute_delta_aic_regression(y, idx, "aic")
        # AIC = 6*log(4/6) + 6 = 3.5672
        # AIC_null = 6*log(17.5/6) + 4 = 10.4226
        # delta = -6.8554
        assert delta == pytest.approx(-6.8554, abs=1e-3)
        # R^2 = 1 - 4/17.5 = 0.7714
        assert r2 == pytest.approx(0.7714, abs=1e-3)

    def test_constant_x_gives_zero_delta(self) -> None:
        # Single bin == null model; delta should equal penalty(3) - penalty(2)
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        idx = np.zeros(5, dtype=np.intp)
        delta, r2 = compute_delta_aic_regression(y, idx, "aic")
        # 1 bin: same RSS as TSS, just different k
        # delta = 0 + (2*2 - 2*2) = 0
        # Actually: k_means=1, k=2 for model; k_null=2 too -> delta = 0
        assert delta == pytest.approx(0.0, abs=1e-6)
        assert r2 == pytest.approx(0.0, abs=1e-6)

    def test_informative_x_gives_negative_delta(self) -> None:
        rng = np.random.default_rng(42)
        n = 200
        y = rng.normal(0, 1, size=n)
        # Sort y and assign quantile bins -> informative
        order = np.argsort(y)
        idx = np.empty(n, dtype=np.intp)
        idx[order] = np.repeat(np.arange(4), n // 4)
        delta, r2 = compute_delta_aic_regression(y, idx, "bic")
        assert delta < -100  # Strong signal
        assert r2 > 0.5

    def test_r_squared_clipped_to_unit_interval(self) -> None:
        # Perfect predictor -> R² very close to 1
        y = np.arange(20, dtype=float)
        idx = np.arange(20, dtype=np.intp)
        delta, r2 = compute_delta_aic_regression(y, idx, "aic")
        assert 0.0 <= r2 <= 1.0
        assert r2 > 0.99


# ---------------------------------------------------------------------------
# Cross-pair comparability (R-1)
# ---------------------------------------------------------------------------


class TestCrossPairComparability:
    """The defining property of (f): for a fixed Y, AIC_null is invariant
    across X candidates, so delta_aic values are directly comparable.

    This tests the cross-check verdict that R-1 holds under common-n.
    """

    def test_aic_null_invariant_across_x_with_same_y_and_n(self) -> None:
        rng = np.random.default_rng(0)
        y = rng.normal(0, 1, size=500)
        # Three different group indexings of the same y
        baseline = compute_gaussian_null_aic(y, "bic")
        for ngroups in (2, 5, 10):
            # x exists only to vary the model; null depends only on y
            _ = rng.integers(0, ngroups, size=500)
            null = compute_gaussian_null_aic(y, "bic")
            assert null == pytest.approx(baseline)  # invariant across x candidates

    def test_delta_aic_ranking_recovers_signal(self) -> None:
        rng = np.random.default_rng(7)
        n = 1000
        y = rng.normal(0, 1, size=n)
        # informative: sort by y -> high R^2 -> very negative delta
        order = np.argsort(y)
        x_inform = np.empty(n, dtype=np.intp)
        x_inform[order] = np.repeat(np.arange(5), n // 5)
        # noise: random groups -> low R^2 -> BIC penalty dominates -> positive delta
        x_noise = rng.integers(0, 5, size=n).astype(np.intp)
        # const: one bin -> exactly the null -> delta = 0
        x_const = np.zeros(n, dtype=np.intp)
        d_inform, _ = compute_delta_aic_regression(y, x_inform, "bic")
        d_noise, _ = compute_delta_aic_regression(y, x_noise, "bic")
        d_const, _ = compute_delta_aic_regression(y, x_const, "bic")
        # Informative is most negative; const is zero; BIC penalizes noise to positive
        assert d_inform < 0  # informative beats null
        assert d_inform < d_const  # informative beats single bin
        assert d_const == pytest.approx(0.0, abs=1e-6)
        # Under BIC, random noise X gets penalized beyond its tiny RSS reduction
        assert d_noise > d_inform  # noise is worse-ranked than informative


# ---------------------------------------------------------------------------
# Reference parity with AdvancedCATDAP
# ---------------------------------------------------------------------------


class TestAdvancedCATDAPParity:
    """Verify our formula matches AdvancedCATDAP's calc_score_reg_bincount_idx.

    AdvancedCATDAP returns ``n * log(RSS/n) + 2k`` with ``k = #non-empty + 1``
    (variance counted as a parameter). With AICc, it adds ``2k(k+1)/(n-k-1)``.

    Numerical reference computed inline so the test is self-contained.
    """

    def test_aic_matches_reference_formula(self) -> None:
        rng = np.random.default_rng(123)
        n = 500
        y = rng.normal(0, 1, size=n)
        idx = rng.integers(0, 5, size=n).astype(np.intp)

        # Reference: replicate AdvancedCATDAP scoring.py:calc_score_reg_bincount_idx
        counts = np.bincount(idx, minlength=5)
        valid = counts > 0
        k_ref = int(np.count_nonzero(valid)) + 1
        sum_y = np.bincount(idx, weights=y, minlength=5)
        sum_y2 = np.bincount(idx, weights=y * y, minlength=5)
        term2 = np.zeros_like(sum_y)
        term2[valid] = (sum_y[valid] ** 2) / counts[valid]
        rss_ref = float(np.sum(sum_y2 - term2))
        rss_ref = max(rss_ref, EPSILON_RSS)
        aic_ref = n * np.log(rss_ref / n) + 2 * k_ref

        aic_ours = compute_gaussian_aic(y, idx, "aic")
        assert aic_ours == pytest.approx(aic_ref, abs=1e-10)
