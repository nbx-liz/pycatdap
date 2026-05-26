"""Cross-validation tests against R catdap package results.

These tests compare pycatdap output against pre-computed reference
values from the R ``catdap`` package (version 1.3.5).

There are two layers of tests:

1. **Property-based tests** (``TestHealthDataCatdap1``, ``TestHealthDataCatdap2``):
   Check the qualitative behavior reproducible without R reference CSVs
   (signs of ΔAIC, ranking inclusion, structural presence). These run
   whenever ``pytest -m slow`` is invoked.

2. **Strict numerical tests** (``TestHealthDataCatdap1StrictR``, etc.):
   Load CSV reference files produced by R catdap 1.3.5 and assert
   ``np.testing.assert_allclose(atol=1e-4)``. These tests are
   automatically skipped if the reference CSVs are not present.
   To generate the CSVs, see ``CONTRIBUTING.md`` § "R version cross-check".

All tests in this module are marked ``@pytest.mark.slow`` and are
excluded from develop-branch CI by default.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pycatdap.catdap1 import catdap1
from pycatdap.catdap2 import catdap2
from pycatdap.datasets import load_health_data

REFERENCE_DIR = Path(__file__).parent.parent / "docs" / "r_reference"


def _load_reference(filename: str) -> pd.DataFrame:
    """Load an R reference CSV, or skip the test if it does not exist.

    Parameters
    ----------
    filename : str
        Name of the CSV file under ``docs/r_reference/``.

    Returns
    -------
    pd.DataFrame
        Reference values loaded from CSV.

    Raises
    ------
    pytest.skip.Exception
        If the file does not exist. Includes regeneration instructions.
    """
    path = REFERENCE_DIR / filename
    if not path.exists():
        pytest.skip(
            f"R reference CSV not found: {path}. "
            f"Generate via 'Rscript docs/r_reference/generate_reference.R' "
            f"(requires R + the catdap package). "
            f"See CONTRIBUTING.md for the full procedure."
        )
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# HealthData — catdap1 — property-based tests (no CSV needed)
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap1:
    """catdap1 on HealthData — qualitative behavior matches R catdap."""

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
        """ΔAIC is asymmetric when C_E != C_F."""
        # 2x2 tables are symmetric by construction; use different category counts
        df = pd.DataFrame(
            {
                "A": ["x", "x", "y", "y", "y"] * 20,
                "B": ["p", "q", "r", "p", "q"] * 20,
            }
        )
        result = catdap1(df)
        aic_ab = result.aic.loc["A", "B"]
        aic_ba = result.aic.loc["B", "A"]
        # C_A=2, C_B=3 → asymmetric penalty → different ΔAIC
        assert aic_ab != aic_ba


# ---------------------------------------------------------------------------
# HealthData — catdap2 — property-based tests (no CSV needed)
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap2:
    """catdap2 on HealthData — qualitative behavior matches R catdap."""

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


# ---------------------------------------------------------------------------
# HealthData — catdap1 — strict numerical comparison vs R catdap 1.3.5
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap1StrictR:
    """Strict numerical comparison of catdap1 output vs R catdap 1.3.5.

    Skipped automatically when ``docs/r_reference/health_catdap1.csv`` is
    not present. See ``CONTRIBUTING.md`` for regeneration.
    """

    def test_health_catdap1_aic_matches_r_atol_1e_4(self) -> None:
        """ΔAIC values for HealthData categorical columns match R within 1e-4."""
        ref = _load_reference("health_catdap1.csv")

        df = load_health_data()
        cat_df = df[["symptoms", "opthalmo.", "ecg", "cholesterol"]]
        result = catdap1(cat_df, response_names=["symptoms"])

        py_row = result.aic.loc["symptoms"].dropna()

        # Verify each variable in the reference exists in our output and matches.
        for _, ref_row in ref.iterrows():
            var = ref_row["variable"]
            r_aic = float(ref_row["aic"])
            assert var in py_row.index, (
                f"Variable {var!r} present in R reference but missing from "
                f"pycatdap output."
            )
            np.testing.assert_allclose(
                py_row[var],
                r_aic,
                atol=1e-4,
                err_msg=f"ΔAIC mismatch for {var!r}: "
                f"pycatdap={py_row[var]:.6f}, R={r_aic:.6f}",
            )


# ---------------------------------------------------------------------------
# HealthData — catdap2 — strict numerical comparison vs R catdap 1.3.5
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestHealthDataCatdap2StrictR:
    """Strict numerical comparison of catdap2 output vs R catdap 1.3.5.

    Skipped automatically when the required CSVs are not present.
    See ``CONTRIBUTING.md`` for regeneration.
    """

    _POOL = [2, 2, 2, 0, 0, 0, 0, 2]
    _ACCURACY = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.1, 0.0]

    def test_health_catdap2_single_var_aic_matches_r_atol_1e_4(self) -> None:
        """Single-variable AIC for HealthData matches R within 1e-4."""
        ref = _load_reference("health_catdap2_aic.csv")

        df = load_health_data()
        result = catdap2(
            df,
            pool=self._POOL,
            response_name="symptoms",
            accuracy=self._ACCURACY,
        )
        py_aic = dict(
            zip(
                result.aic["variable"].tolist(),
                result.aic["aic"].to_numpy(dtype=float),
                strict=False,
            )
        )

        for _, ref_row in ref.iterrows():
            var = ref_row["variable"]
            r_aic = float(ref_row["aic"])
            assert var in py_aic, (
                f"Variable {var!r} present in R reference but missing from "
                f"pycatdap result."
            )
            np.testing.assert_allclose(
                py_aic[var],
                r_aic,
                atol=1e-4,
                err_msg=f"AIC mismatch for {var!r}: "
                f"pycatdap={py_aic[var]:.6f}, R={r_aic:.6f}",
            )

    def test_health_catdap2_subsets_match_r_atol_1e_4(self) -> None:
        """Best-subset AIC values for HealthData match R within 1e-4.

        Subsets are matched by the sorted tuple of explanatory variables.
        """
        ref = _load_reference("health_catdap2_subsets.csv")

        df = load_health_data()
        result = catdap2(
            df,
            pool=self._POOL,
            response_name="symptoms",
            accuracy=self._ACCURACY,
        )
        py_subsets: dict[tuple[str, ...], float] = {
            tuple(sorted(s.variables)): float(s.aic) for s in result.subsets
        }

        for _, ref_row in ref.iterrows():
            r_vars = tuple(sorted(str(ref_row["variables"]).split(";")))
            r_aic = float(ref_row["aic"])
            assert r_vars in py_subsets, (
                f"Subset {r_vars} present in R reference but missing from "
                f"pycatdap subsets."
            )
            np.testing.assert_allclose(
                py_subsets[r_vars],
                r_aic,
                atol=1e-4,
                err_msg=f"AIC mismatch for subset {r_vars}: "
                f"pycatdap={py_subsets[r_vars]:.6f}, R={r_aic:.6f}",
            )
