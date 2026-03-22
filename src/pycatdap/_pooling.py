"""Continuous variable categorization (pooling) via AIC minimization.

Converts continuous variables into categorical ones by finding AIC-optimal
bin boundaries.  Two methods are provided:

* **Equal pooling** (``pool=0``): top-down, equal-interval bins merged greedily.
* **Unequal pooling** (``pool=1``, default): bottom-up, fine bins merged until
  no merge improves AIC.

Input arrays are never mutated.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from pycatdap._aic import _safe_xlogy

# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PoolingResult:
    """Result of AIC-optimal binning.

    Attributes
    ----------
    codes : ndarray of int
        Bin assignment for each observation (0-indexed).
    boundaries : list[float]
        Sorted internal bin boundary values.  ``len(boundaries) == n_bins - 1``
        where *n_bins* is the number of distinct bins.
    """

    codes: npt.NDArray[np.intp]
    boundaries: list[float]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _auto_accuracy(values: npt.NDArray[np.float64]) -> float:
    """Guess accuracy from the smallest non-zero gap between sorted values."""
    sorted_vals = np.sort(np.unique(values))
    if len(sorted_vals) <= 1:
        return 1.0
    diffs = np.diff(sorted_vals)
    positive_diffs = diffs[diffs > 0]
    if len(positive_diffs) == 0:
        return 1.0
    return float(np.min(positive_diffs))


def _initial_bins(
    values: npt.NDArray[np.float64],
    accuracy: float,
) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.float64]]:
    """Divide the value range into fine-grained bins of width *accuracy*.

    Returns
    -------
    bin_codes : ndarray of int
        Bin index for each observation.
    edges : ndarray of float
        Bin edge values (length = n_bins + 1).
    """
    vmin, vmax = float(values.min()), float(values.max())

    if vmax - vmin < accuracy:
        # All values in a single bin
        return np.zeros(len(values), dtype=np.intp), np.array([vmin, vmax + accuracy])

    n_bins = max(1, int(np.ceil((vmax - vmin) / accuracy)))
    edges = np.linspace(vmin, vmax + accuracy * 0.01, n_bins + 1)
    # np.digitize returns 1-based indices; subtract 1, clip to valid range
    codes = np.clip(np.digitize(values, edges[1:-1]), 0, n_bins - 1).astype(np.intp)
    return codes, edges


def _build_bin_freq_table(
    bin_codes: npt.NDArray[np.intp],
    response_codes: npt.NDArray[np.intp],
    n_bins: int,
    n_resp_cats: int,
) -> npt.NDArray[np.float64]:
    """Build a (n_resp_cats, n_bins) frequency table from bin and response codes."""
    freq = np.zeros((n_resp_cats, n_bins), dtype=np.float64)
    np.add.at(freq, (response_codes, bin_codes), 1)
    return freq


def _bin_aic(freq: npt.NDArray[np.float64]) -> float:
    """Compute AIC(E; F) for a frequency table (response x bins).

    AIC = -2 * sum(n_ij * ln(n_ij / n_j)) + 2 * (C_E - 1) * C_F
    """
    c_e, c_f = freq.shape
    marg_f = freq.sum(axis=0)
    ratio = np.where(marg_f > 0, freq / marg_f, 0.0)
    loglik = float(np.sum(_safe_xlogy(freq, ratio)))
    penalty = 2.0 * (c_e - 1) * c_f
    return float(-2.0 * loglik + penalty)


def _merge_bins(
    freq: npt.NDArray[np.float64],
    i: int,
) -> npt.NDArray[np.float64]:
    """Return a new frequency table with bins *i* and *i+1* merged."""
    new_freq: npt.NDArray[np.float64] = np.delete(freq, i + 1, axis=1).copy()
    new_freq[:, i] = freq[:, i] + freq[:, i + 1]
    return new_freq


def _encode_response(
    response: npt.NDArray[np.object_],
) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.object_]]:
    """Encode response labels to integer codes."""
    uniq, codes = np.unique(response, return_inverse=True)
    return codes.astype(np.intp), uniq


def _codes_from_boundaries(
    values: npt.NDArray[np.float64],
    boundaries: list[float],
) -> npt.NDArray[np.intp]:
    """Assign bin codes from a sorted boundary list."""
    if not boundaries:
        return np.zeros(len(values), dtype=np.intp)
    return np.digitize(values, boundaries).astype(np.intp)


# ---------------------------------------------------------------------------
# Equal pooling (pool=0, top-down)
# ---------------------------------------------------------------------------


def equal_pooling(
    values: npt.NDArray[np.float64],
    response: npt.NDArray[np.object_],
    accuracy: float,
) -> PoolingResult:
    """Equal-interval pooling (top-down greedy merge).

    Start with bins of width *accuracy*, then greedily merge adjacent
    bins when merging reduces AIC.

    Parameters
    ----------
    values : ndarray
        Continuous variable values.
    response : ndarray
        Response variable labels (categorical).
    accuracy : float
        Minimum bin width (observation precision).

    Returns
    -------
    PoolingResult
    """
    values = np.asarray(values, dtype=np.float64)
    if len(values) == 0:
        return PoolingResult(codes=np.array([], dtype=np.intp), boundaries=[])

    resp_codes, _ = _encode_response(np.asarray(response))

    bin_codes, edges = _initial_bins(values, accuracy)
    n_bins = len(edges) - 1
    n_resp_cats = int(resp_codes.max()) + 1

    freq = _build_bin_freq_table(bin_codes, resp_codes, n_bins, n_resp_cats)

    # Remove empty bins
    nonempty = freq.sum(axis=0) > 0
    if not np.all(nonempty):
        freq = freq[:, nonempty]
        edges = np.concatenate(
            # Keep first edge, then non-empty right edges
            [edges[:1], edges[1:][nonempty]]
        )
        # Pad last edge if needed
        if len(edges) <= freq.shape[1]:
            edges = np.append(edges, edges[-1] + accuracy)

    # Greedy merge: merge the pair that most decreases AIC
    current_aic = _bin_aic(freq)
    changed = True
    while changed and freq.shape[1] > 1:
        changed = False
        best_delta = 0.0
        best_idx = -1
        best_freq: npt.NDArray[np.float64] | None = None

        for i in range(freq.shape[1] - 1):
            merged = _merge_bins(freq, i)
            new_aic = _bin_aic(merged)
            delta = new_aic - current_aic
            if delta < best_delta:
                best_delta = delta
                best_idx = i
                best_freq = merged

        if best_freq is not None:
            freq = best_freq
            # Remove the merged edge
            edges = np.delete(edges, best_idx + 1)
            current_aic += best_delta
            changed = True

    # Build boundaries (internal edges, excluding first and last)
    boundaries = sorted(float(e) for e in edges[1:-1])
    codes = _codes_from_boundaries(values, boundaries)
    return PoolingResult(codes=codes, boundaries=boundaries)


# ---------------------------------------------------------------------------
# Unequal pooling (pool=1, bottom-up) — default
# ---------------------------------------------------------------------------


def unequal_pooling(
    values: npt.NDArray[np.float64],
    response: npt.NDArray[np.object_],
    accuracy: float,
) -> PoolingResult:
    """Unequal-interval pooling (bottom-up greedy merge).

    Start with fine bins of width *accuracy*, then iteratively merge the
    adjacent pair that yields the largest AIC decrease.  Stop when no
    merge improves AIC.

    Parameters
    ----------
    values : ndarray
        Continuous variable values.
    response : ndarray
        Response variable labels (categorical).
    accuracy : float
        Minimum bin width.

    Returns
    -------
    PoolingResult
    """
    values = np.asarray(values, dtype=np.float64)
    if len(values) == 0:
        return PoolingResult(codes=np.array([], dtype=np.intp), boundaries=[])

    resp_codes, _ = _encode_response(np.asarray(response))

    bin_codes, edges = _initial_bins(values, accuracy)
    n_bins = len(edges) - 1
    n_resp_cats = int(resp_codes.max()) + 1

    freq = _build_bin_freq_table(bin_codes, resp_codes, n_bins, n_resp_cats)

    # Remove empty bins
    nonempty = freq.sum(axis=0) > 0
    if not np.all(nonempty):
        freq = freq[:, nonempty]
        edges = np.concatenate([edges[:1], edges[1:][nonempty]])
        if len(edges) <= freq.shape[1]:
            edges = np.append(edges, edges[-1] + accuracy)

    # Bottom-up: iteratively merge best adjacent pair
    current_aic = _bin_aic(freq)
    while freq.shape[1] > 1:
        best_delta = 0.0
        best_idx = -1
        best_freq: npt.NDArray[np.float64] | None = None

        for i in range(freq.shape[1] - 1):
            merged = _merge_bins(freq, i)
            new_aic = _bin_aic(merged)
            delta = new_aic - current_aic
            if delta < best_delta:
                best_delta = delta
                best_idx = i
                best_freq = merged

        if best_freq is None:
            break  # No merge improves AIC

        freq = best_freq
        edges = np.delete(edges, best_idx + 1)
        current_aic += best_delta

    boundaries = sorted(float(e) for e in edges[1:-1])
    codes = _codes_from_boundaries(values, boundaries)
    return PoolingResult(codes=codes, boundaries=boundaries)


# ---------------------------------------------------------------------------
# Public dispatch
# ---------------------------------------------------------------------------


def optimal_binning(
    values: npt.NDArray[np.float64],
    response: npt.NDArray[np.object_],
    method: str = "bottom_up",
    accuracy: float | None = None,
) -> PoolingResult:
    """Categorize a continuous variable via AIC-optimal binning.

    Parameters
    ----------
    values : ndarray
        Continuous variable values.
    response : ndarray
        Response variable labels (categorical).
    method : {'bottom_up', 'top_down'}
        ``'bottom_up'`` (default) uses unequal pooling;
        ``'top_down'`` uses equal pooling.
    accuracy : float or None
        Minimum bin width.  If ``None``, auto-detected from data.

    Returns
    -------
    PoolingResult
        Bin codes and boundary values.

    Raises
    ------
    ValueError
        If *method* is not ``'bottom_up'`` or ``'top_down'``.
    """
    values = np.asarray(values, dtype=np.float64)
    response = np.asarray(response)

    if accuracy is None:
        accuracy = _auto_accuracy(values)

    if method == "bottom_up":
        return unequal_pooling(values, response, accuracy)
    if method == "top_down":
        return equal_pooling(values, response, accuracy)

    msg = f"method must be 'bottom_up' or 'top_down', got '{method}'"
    raise ValueError(msg)
