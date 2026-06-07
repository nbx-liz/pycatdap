"""Deterministic synthetic data generators for the benchmark suite.

Every generator is seeded with a fixed base seed so the *workload* is identical
across runs and machines; only the measured timing varies. Inputs returned here
are never mutated by the benchmarked functions (pycatdap is immutable by
contract), so a single generated frame can be reused across benchmark rounds.

These are NOT the real OpenML datasets. ``make_adult_like`` mimics the Adult
Income shape (14 mixed columns) without fetching, avoiding network-timing
variance and the OOM hazard of unbounded slice discovery on the full dataset
(see HISTORY H-0021 and memory ``incident_discover_slices_oom``).
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import pandas as pd

# Fixed base seed: deterministic, reproducible workloads.
_SEED = 20260607


def make_categorical(
    n_rows: int, n_cols: int = 10, n_cats: int = 5, *, seed: int = _SEED
) -> pd.DataFrame:
    """All-categorical frame of shape ``(n_rows, n_cols)`` for catdap1."""
    rng = np.random.default_rng(seed)
    cats = [f"cat{i}" for i in range(n_cats)]
    data = {f"c{j}": rng.choice(cats, size=n_rows) for j in range(n_cols)}
    return pd.DataFrame(data)


def make_mixed(
    n_rows: int, n_cols: int = 10, *, seed: int = _SEED
) -> tuple[pd.DataFrame, list[int]]:
    """Mixed frame + per-column pool codes for catdap2.

    Column 0 (``"response"``) is the categorical response. Of the remaining
    ``n_cols - 1`` columns, even-indexed ones are continuous (pool ``1`` =
    unequal) and odd-indexed ones categorical (pool ``2``). The returned pool
    list is aligned to the DataFrame column order.
    """
    rng = np.random.default_rng(seed)
    frame: dict[str, npt.NDArray[np.generic]] = {
        "response": rng.choice(["A", "B", "C"], size=n_rows)
    }
    pool: list[int] = [2]
    for j in range(n_cols - 1):
        if j % 2 == 0:
            # Bounded-precision continuous (see make_continuous_response).
            frame[f"num{j}"] = np.round(rng.normal(size=n_rows), 1)
            pool.append(1)
        else:
            frame[f"cat{j}"] = rng.choice([f"g{k}" for k in range(4)], size=n_rows)
            pool.append(2)
    return pd.DataFrame(frame), pool


def make_continuous_response(
    n_rows: int, *, seed: int = _SEED
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.object_]]:
    """``(values, response)`` arrays for ``optimal_binning`` benchmarks.

    ``values`` is rounded to one decimal place. AIC binning starts from
    fine-grained bins of width ``accuracy`` (auto-detected as the smallest gap
    between sorted unique values), so all-unique floats would explode the
    initial bin count and make greedy merging O(unique^2). Real continuous
    features have finite measurement precision; rounding mimics that and keeps
    the initial bin count bounded and independent of ``n_rows`` — the benchmark
    then measures the genuine O(n_rows) frequency-table build.
    """
    rng = np.random.default_rng(seed)
    values = np.round(rng.normal(size=n_rows), 1).astype(np.float64)
    response = rng.choice(["yes", "no"], size=n_rows).astype(object)
    return values, response


# Adult-Income-like shape: 6 continuous + 8 categorical = 14 columns.
_ADULT_CONTINUOUS = (
    "age",
    "fnlwgt",
    "education_num",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
)
_ADULT_CATEGORICAL = {
    "workclass": 7,
    "education": 16,
    "marital_status": 7,
    "occupation": 14,
    "relationship": 6,
    "race": 5,
    "sex": 2,
    "native_country": 10,
}


def make_adult_like(
    n_rows: int = 5_000, *, error_rate: float = 0.2, seed: int = _SEED
) -> tuple[pd.DataFrame, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
    """Synthetic 14-column mixed frame mimicking Adult Income.

    Returns ``(df, y_true, y_pred)`` for ``discover_error_slices`` benchmarks.
    ``y_pred`` equals ``y_true`` except on a random ``error_rate`` fraction,
    giving a realistic, bounded error signal. Heavily bounded by design so the
    benchmark never approaches the OOM regime of the real dataset.
    """
    rng = np.random.default_rng(seed)
    frame: dict[str, npt.NDArray[np.generic]] = {
        col: rng.integers(0, 100, size=n_rows).astype(float)
        for col in _ADULT_CONTINUOUS
    }
    for col, card in _ADULT_CATEGORICAL.items():
        frame[col] = rng.choice([f"{col[:3]}{k}" for k in range(card)], size=n_rows)
    df = pd.DataFrame(frame)
    y_true = rng.integers(0, 2, size=n_rows)
    flip = rng.random(n_rows) < error_rate
    y_pred = np.where(flip, 1 - y_true, y_true)
    return df, y_true, y_pred
