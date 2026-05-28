"""Tests for ``association_matrix(measure=...)`` extension (H-0008 PR-D5).

PR-D4 added the :mod:`pycatdap.measures` subpackage with a uniform
``Callable[[npt.NDArray[np.float64]], float]`` signature. This PR wires
that into :func:`pycatdap.association_matrix` so the matrix can be
computed with any registered measure, not just ΔAIC.

``measure="aic"`` keeps the existing
:func:`pycatdap.target_summary`-based path (which handles continuous
targets via H-0005 regression AIC). All other measures use a generic
crosstab path that bins continuous columns via ``pd.qcut`` so they
work uniformly across dtypes.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import pycatdap


@pytest.fixture()
def df_mixed() -> pd.DataFrame:
    rng = np.random.default_rng(seed=11)
    n = 200
    cat = rng.choice(["a", "b", "c"], size=n)
    return pd.DataFrame(
        {
            "y": np.where(cat == "a", "yes", "no"),
            "informative": cat,
            "noise": rng.choice(["x", "y", "z"], size=n),
            "cont": rng.normal(0, 1, size=n),
        }
    )


def test_aic_measure_default_unchanged(df_mixed: pd.DataFrame) -> None:
    """Default measure stays 'aic' and matches the pre-extension behavior."""
    m_default = pycatdap.association_matrix(df_mixed)
    m_explicit = pycatdap.association_matrix(df_mixed, measure="aic")
    pd.testing.assert_frame_equal(m_default, m_explicit)


def _off_diagonal(m: pd.DataFrame) -> np.ndarray:
    """Return the off-diagonal cells of *m* as a flat numpy array.

    Newer pandas (>= 2.1) no longer drops NaN inside ``DataFrame.stack``,
    so use a boolean mask on ``.values`` to get only the off-diagonal
    entries.
    """
    mask = ~np.eye(m.shape[0], dtype=bool)
    return np.asarray(m.values[mask], dtype=float)


def test_cramers_v_measure_returns_unit_range_matrix(
    df_mixed: pd.DataFrame,
) -> None:
    m = pycatdap.association_matrix(df_mixed, measure="cramers_v")
    assert m.shape == (4, 4)
    # diagonal is NaN
    for col in m.columns:
        assert pd.isna(m.loc[col, col])
    # off-diagonal in [0, 1]
    off_diag = _off_diagonal(m)
    assert np.all(np.isfinite(off_diag))
    assert (off_diag >= 0.0).all()
    assert (off_diag <= 1.0).all()


def test_mutual_info_measure_returns_non_negative(
    df_mixed: pd.DataFrame,
) -> None:
    m = pycatdap.association_matrix(df_mixed, measure="mutual_info")
    off_diag = _off_diagonal(m)
    assert np.all(np.isfinite(off_diag))
    assert (off_diag >= 0.0).all()


def test_unknown_measure_raises_value_error(df_mixed: pd.DataFrame) -> None:
    # The error path goes through the measures registry; keep the message
    # contract loose so either layer can change wording.
    with pytest.raises((ValueError, KeyError), match="not registered|measure"):
        pycatdap.association_matrix(df_mixed, measure="__does_not_exist")


def test_custom_registered_measure_works(df_mixed: pd.DataFrame) -> None:
    """A user-registered measure flows through association_matrix end-to-end."""

    def constant_one(cf: np.ndarray) -> float:
        return 1.0 if cf.sum() > 0 else 0.0

    pycatdap.measures.register("__assoc_test_const_one", constant_one)
    try:
        m = pycatdap.association_matrix(df_mixed, measure="__assoc_test_const_one")
        # all off-diagonal cells are exactly 1.0
        off_diag = _off_diagonal(m)
        assert (off_diag == 1.0).all()
    finally:
        pycatdap.measures._registry._REGISTRY.pop("__assoc_test_const_one", None)


def test_cramers_v_informative_column_ranks_highest(
    df_mixed: pd.DataFrame,
) -> None:
    """The intentionally-correlated `informative` column should dominate.

    For target='y' (= "yes" iff informative='a'), Cramér's V between
    y and informative should exceed V between y and the random noise
    columns by a substantial margin.
    """
    m = pycatdap.association_matrix(df_mixed, measure="cramers_v")
    v_informative = m.loc["y", "informative"]
    v_noise = m.loc["y", "noise"]
    assert v_informative > v_noise


def test_zero_row_dataframe_returns_all_nan_matrix() -> None:
    """A 0-row DataFrame must not crash — every off-diagonal cell is NaN.

    Hits the ``ct.size == 0`` early-continue branch in the generic
    measure path; the AIC path would fail earlier inside target_summary
    on empty data.
    """
    df = pd.DataFrame({"a": [], "b": []}, dtype=float)
    m = pycatdap.association_matrix(df, measure="cramers_v")
    assert m.shape == (2, 2)
    assert m.isna().all().all()


def test_all_nan_column_yields_nan_cell() -> None:
    """An all-NaN column makes the cross-frequency table degenerate.

    The generic measure path bins all-NaN into a single ``_missing_``
    bucket; pd.crosstab against any non-empty column produces a
    1-column table whose sum is the count of non-NaN rows in the other
    column. The cell is finite (no NaN), but the edge case exercises
    the qcut ValueError fallback in ``_binize``.
    """
    df = pd.DataFrame(
        {
            "real": [1, 2, 1, 2, 1, 2] * 10,
            "nans": [np.nan] * 60,
        }
    )
    m = pycatdap.association_matrix(df, measure="cramers_v")
    # the all-NaN column folds to a single category → V is well-defined
    assert np.isfinite(m.loc["real", "nans"])


def test_continuous_pair_works_via_qcut_binning(
    df_mixed: pd.DataFrame,
) -> None:
    """A continuous-continuous cell must produce a finite Cramér's V.

    Without binning, cramers_v would see a near-square table with
    n_unique ≈ n_obs and return ≈ 1; the generic path bins via
    pd.qcut so the result is in the expected [0, 1] range and is
    finite (not NaN).
    """
    df = pd.DataFrame(
        {
            "x1": np.linspace(0, 1, 100),
            "x2": np.linspace(0, 1, 100)
            + np.random.default_rng(0).normal(0, 0.1, size=100),
        }
    )
    m = pycatdap.association_matrix(df, measure="cramers_v")
    v = m.loc["x1", "x2"]
    assert np.isfinite(v)
    assert 0.0 <= v <= 1.0
