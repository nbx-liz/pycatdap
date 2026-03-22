"""Optimal explanatory variable subset search.

Implements a stepwise (greedy forward) search for the best subset of
explanatory variables that minimizes ΔAIC for a given response variable.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import pandas as pd

from pycatdap._aic import compute_delta_aic
from pycatdap._contingency import build_crosstab, build_multidim_crosstab


@dataclass(frozen=True)
class SubsetResult:
    """Result for a single variable subset.

    Attributes
    ----------
    variables : tuple[str, ...]
        Explanatory variable names in this subset.
    n_vars : int
        Number of variables in the subset.
    n_categories : int
        Total number of combined categories.
    aic : float
        ΔAIC value for this subset.
    """

    variables: tuple[str, ...]
    n_vars: int
    n_categories: int
    aic: float


def _rank_single_variables(
    data: pd.DataFrame,
    response: str,
    candidates: list[str],
) -> list[tuple[str, float, int]]:
    """Rank candidate explanatory variables by ΔAIC.

    Returns
    -------
    list of (variable_name, delta_aic, n_categories)
        Sorted ascending by ΔAIC (best first).
    """
    rankings: list[tuple[str, float, int]] = []
    for var in candidates:
        cross, marg_e, marg_f, n = build_crosstab(data, response, var)
        delta = compute_delta_aic(cross, marg_e, marg_f, n)
        n_cats = cross.shape[1]
        rankings.append((var, delta, n_cats))
    rankings.sort(key=lambda x: x[1])
    return rankings


def search_best_subset(
    data: pd.DataFrame,
    response: str,
    explanatory_candidates: list[str],
    max_vars: int | None = None,
    nvar: int | None = None,
) -> list[SubsetResult]:
    """Search for the best explanatory variable subsets using stepwise AIC.

    Parameters
    ----------
    data : DataFrame
        Input data (not modified).
    response : str
        Response variable column name.
    explanatory_candidates : list[str]
        Candidate explanatory variable column names.
    max_vars : int or None
        Maximum subset size to explore.  Defaults to the number of candidates.
    nvar : int or None
        Number of top single-variable candidates to retain for multi-variable
        search.  Defaults to all candidates.

    Returns
    -------
    list[SubsetResult]
        Results grouped by subset size and sorted by ΔAIC within each group.
    """
    if max_vars is None:
        max_vars = len(explanatory_candidates)
    if nvar is None:
        nvar = len(explanatory_candidates)

    # Step 1: Rank single variables
    rankings = _rank_single_variables(data, response, explanatory_candidates)

    results: list[SubsetResult] = []

    # Add single-variable results
    for var, aic, n_cats in rankings:
        results.append(
            SubsetResult(
                variables=(var,),
                n_vars=1,
                n_categories=n_cats,
                aic=aic,
            )
        )

    if max_vars <= 1:
        return results

    # Step 2: Multi-variable search with nvar pruning
    # Keep top nvar variables for combination search
    top_vars = [var for var, _, _ in rankings[:nvar]]

    for k in range(2, min(max_vars, len(top_vars)) + 1):
        k_results: list[SubsetResult] = []
        for combo in combinations(top_vars, k):
            var_list = list(combo)
            cross, marg_e, marg_f, n = build_multidim_crosstab(data, response, var_list)
            delta = compute_delta_aic(cross, marg_e, marg_f, n)
            n_cats = cross.shape[1]
            k_results.append(
                SubsetResult(
                    variables=combo,
                    n_vars=k,
                    n_categories=n_cats,
                    aic=delta,
                )
            )
        k_results.sort(key=lambda r: r.aic)
        results.extend(k_results)

    return results
