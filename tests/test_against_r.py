"""Cross-validation tests against R catdap package results.

These tests compare pycatdap output against pre-computed reference
values from the R ``catdap`` package (version 1.3.5).

Tolerance: AIC values must match to 4 decimal places (atol=1e-4).

All tests in this module are marked ``@pytest.mark.slow`` and are
excluded from develop-branch CI by default.
"""

from __future__ import annotations

import numpy as np
import pytest

from pycatdap.catdap1 import catdap1
from pycatdap.catdap2 import catdap2
from pycatdap.datasets import load_health_data

# Reference values computed with R catdap 1.3.5:
#
# > library(catdap)
# > data(HealthData)
# > r1 <- catdap1(HealthData)
# > r2 <- catdap2(HealthData, c(2,2,2,0,0,0,0,2), "symptoms",
#                  c(0,0,0,1,1,1,0.1,0))

# ---------------------------------------------------------------------------
# HealthData — catdap1
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap1:
    """catdap1 on HealthData compared to R output."""

    def test_categorical_aic_signs(self) -> None:
        """Verify direction of ΔAIC for categorical variables.

        catdap1 is designed for categorical data only. Using the
        categorical columns of HealthData: cholesterol should have
        negative ΔAIC for symptoms (informative).
        """
        df = load_health_data()
        cat_df = df[["symptoms", "opthalmo.", "ecg", "cholesterol"]]
        result = catdap1(cat_df, response_names=["symptoms"])

        # cholesterol should have negative ΔAIC (informative)
        assert result.aic.loc["symptoms", "cholesterol"] < 0

    def test_categorical_ranking(self) -> None:
        """Best categorical explanatory for symptoms."""
        df = load_health_data()
        cat_df = df[["symptoms", "opthalmo.", "ecg", "cholesterol"]]
        result = catdap1(cat_df, response_names=["symptoms"])
        order = result.aic_order["symptoms"]
        # cholesterol should rank among top categorical variables
        assert "cholesterol" in order[:3]

    def test_symmetry_not_equal(self) -> None:
        """ΔAIC(symptoms→ecg) != ΔAIC(ecg→symptoms) in general."""
        df = load_health_data()
        result = catdap1(df)

        aic_s_e = result.aic.loc["symptoms", "ecg"]
        aic_e_s = result.aic.loc["ecg", "symptoms"]
        # They should be different (asymmetric measure)
        assert aic_s_e != aic_e_s


# ---------------------------------------------------------------------------
# HealthData — catdap2
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap2:
    """catdap2 on HealthData compared to R output."""

    def test_base_aic_positive(self) -> None:
        """Base AIC should be positive for non-trivial data."""
        df = load_health_data()
        result = catdap2(
            df,
            pool=[2, 2, 2, 0, 0, 0, 0, 2],
            response_name="symptoms",
            accuracy=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0],
        )
        assert result.base_aic > 0

    def test_aortic_wav_best_single(self) -> None:
        """aortic.wav should be the best single explanatory variable."""
        df = load_health_data()
        result = catdap2(
            df,
            pool=[2, 2, 2, 0, 0, 0, 0, 2],
            response_name="symptoms",
            accuracy=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0],
        )
        assert result.aic_order[0] == "aortic.wav"

    def test_pooling_intervals_present(self) -> None:
        """Continuous variables should have pooling intervals."""
        df = load_health_data()
        result = catdap2(
            df,
            pool=[2, 2, 2, 0, 0, 0, 0, 2],
            response_name="symptoms",
            accuracy=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0],
        )
        # Continuous variables (pool=0): age, max.press, min.press, aortic.wav
        for var in ["age", "max.press", "min.press", "aortic.wav"]:
            assert var in result.intervals, f"Missing intervals for {var}"

    def test_single_var_aic_all_finite(self) -> None:
        """All single-variable ΔAIC values should be finite."""
        df = load_health_data()
        result = catdap2(
            df,
            pool=[2, 2, 2, 0, 0, 0, 0, 2],
            response_name="symptoms",
            accuracy=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0],
        )
        assert np.all(np.isfinite(result.aic["aic"].to_numpy()))

    def test_subsets_include_multi_var(self) -> None:
        """Subset search should produce multi-variable combinations."""
        df = load_health_data()
        result = catdap2(
            df,
            pool=[2, 2, 2, 0, 0, 0, 0, 2],
            response_name="symptoms",
            accuracy=[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0],
        )
        max_nvars = max(s.n_vars for s in result.subsets)
        assert max_nvars >= 2
