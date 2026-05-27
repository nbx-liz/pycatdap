"""Association matrix across all column pairs of a DataFrame (H-0006 PR-B2).

Provides :func:`association_matrix`, a thin loop over
:func:`pycatdap.target_summary` that builds an asymmetric m × m matrix
of ΔAIC values. Each cell ``M.loc[i, j]`` reports "how much does
``j`` explain ``i`` (treating ``i`` as the response)" — so the matrix is
intentionally asymmetric: ``M.loc[i, j] != M.loc[j, i]`` carries
directional information about explanatory power.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

from pycatdap._target_pair import target_summary

Measure = Literal["aic"]
Criterion = Literal["aic", "aicc", "bic"]


def association_matrix(
    df: pd.DataFrame,
    *,
    measure: Measure = "aic",
    bins: int | None = None,
    criterion: Criterion = "bic",
) -> pd.DataFrame:
    """Compute the m × m ΔAIC association matrix across all column pairs.

    For each ordered pair ``(i, j)`` with ``i != j``, the cell holds
    ``target_summary(df, target=i, explanatory=j, ...).delta_aic``. The
    matrix is **asymmetric** because ΔAIC depends on which side is
    treated as the response. The diagonal is ``NaN`` (self-association
    is mathematically undefined).

    Parameters
    ----------
    df : DataFrame
        Source data; all columns are scanned.
    measure : {'aic'}
        Association measure. v0.4.0 supports only ``"aic"`` (ΔAIC via
        :func:`target_summary`). ``"cramers_v"`` / ``"mutual_info"``
        are planned for a follow-up Proposal (H-0007).
    bins : int or None
        Binning passed to :func:`target_summary` for continuous
        explanatory variables. ``None`` selects AIC-optimal binning.
    criterion : {'aic', 'aicc', 'bic'}
        Penalty family for the Gaussian regression path (H-0005).
        Ignored for cells where the target is categorical.

    Returns
    -------
    DataFrame
        Square ``(n_cols, n_cols)`` frame indexed and column-labelled by
        ``df.columns``. Diagonal is ``NaN``.

    Raises
    ------
    ValueError
        If *df* has no columns or *measure* is unknown.

    Examples
    --------
    >>> import pycatdap
    >>> df = pycatdap.datasets.load_titanic()
    >>> m = pycatdap.association_matrix(df[["Survived", "Sex", "Pclass"]])
    >>> m.shape
    (3, 3)
    >>> bool(m.loc["Survived", "Sex"] < 0)  # Sex informs Survived
    True
    """
    if measure != "aic":
        msg = (
            f"association_matrix: unknown measure {measure!r}; "
            "v0.4.0 supports only 'aic'. "
            "'cramers_v' and 'mutual_info' are planned for H-0007."
        )
        raise ValueError(msg)

    cols = list(df.columns)
    if not cols:
        msg = "association_matrix: df must have at least one column"
        raise ValueError(msg)

    matrix = np.full((len(cols), len(cols)), np.nan, dtype=float)
    for i, target in enumerate(cols):
        for j, explanatory in enumerate(cols):
            if i == j:
                continue
            result = target_summary(
                df,
                target=target,
                explanatory=explanatory,
                bins=bins,
                criterion=criterion,
            )
            matrix[i, j] = float(result.delta_aic)

    return pd.DataFrame(matrix, index=cols, columns=cols)


__all__ = ["association_matrix"]
