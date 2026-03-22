"""Contingency table construction utilities.

Converts pandas DataFrames into numpy arrays suitable for AIC computation.
Input DataFrames are never mutated.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.typing import NDArray


def build_crosstab(
    data: pd.DataFrame,
    response: str,
    explanatory: str,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], int]:
    """Build a two-way frequency table from a DataFrame.

    Rows with ``NaN`` in either column are dropped before tabulation.

    Parameters
    ----------
    data : DataFrame
        Input data (not modified).
    response : str
        Column name of the response variable (rows of cross-table).
    explanatory : str
        Column name of the explanatory variable (columns of cross-table).

    Returns
    -------
    cross_freq : ndarray, shape (C_E, C_F)
        Cross-frequency table.
    marginal_e : ndarray, shape (C_E,)
        Marginal frequencies of the response variable.
    marginal_f : ndarray, shape (C_F,)
        Marginal frequencies of the explanatory variable.
    n : int
        Total number of valid observations.

    Raises
    ------
    KeyError
        If *response* or *explanatory* is not in the DataFrame.
    """
    # Validate columns exist (raises KeyError if not)
    _ = data[response], data[explanatory]

    # Drop NaN in the two relevant columns only — do not modify input
    subset = data[[response, explanatory]].dropna()

    ct = pd.crosstab(subset[response], subset[explanatory])
    cross_freq = ct.to_numpy(dtype=np.float64)
    marginal_e = cross_freq.sum(axis=1).astype(np.float64)
    marginal_f = cross_freq.sum(axis=0).astype(np.float64)
    n = int(cross_freq.sum())

    return cross_freq, marginal_e, marginal_f, n


def build_multidim_crosstab(
    data: pd.DataFrame,
    response: str,
    explanatory_set: list[str],
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64], int]:
    """Build a cross-frequency table with a composite explanatory variable.

    The explanatory variables are combined into a single composite variable
    (tupled categories) before tabulation.

    Parameters
    ----------
    data : DataFrame
        Input data (not modified).
    response : str
        Column name of the response variable.
    explanatory_set : list[str]
        Column names of the explanatory variables to combine.

    Returns
    -------
    cross_freq : ndarray, shape (C_E, C_F_combined)
        Cross-frequency table.
    marginal_e : ndarray, shape (C_E,)
        Marginal frequencies of the response variable.
    marginal_f : ndarray, shape (C_F_combined,)
        Marginal frequencies of the composite explanatory variable.
    n : int
        Total number of valid observations.

    Raises
    ------
    ValueError
        If *explanatory_set* is empty.
    KeyError
        If *response* or any column in *explanatory_set* is not in the DataFrame.
    """
    if not explanatory_set:
        msg = "explanatory_set must not be empty"
        raise ValueError(msg)

    # Validate all columns exist
    _ = data[response]
    for col in explanatory_set:
        _ = data[col]

    if len(explanatory_set) == 1:
        return build_crosstab(data, response, explanatory_set[0])

    cols = [response, *explanatory_set]
    subset = data[cols].dropna()

    # Use unit separator (U+001F) to avoid collisions with category labels
    composite = subset[explanatory_set].astype(str).agg("\x1f".join, axis=1)
    temp = pd.DataFrame(
        {
            "_response_": subset[response].to_numpy(),
            "_composite_": composite.to_numpy(),
        }
    )

    ct = pd.crosstab(temp["_response_"], temp["_composite_"])
    cross_freq = ct.to_numpy(dtype=np.float64)
    marginal_e = cross_freq.sum(axis=1).astype(np.float64)
    marginal_f = cross_freq.sum(axis=0).astype(np.float64)
    n = int(cross_freq.sum())

    return cross_freq, marginal_e, marginal_f, n
