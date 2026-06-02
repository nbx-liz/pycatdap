"""Association matrix across all column pairs of a DataFrame.

Provides :func:`association_matrix`, an m × m matrix of pairwise
association scores. Each cell ``M.loc[i, j]`` reports "how much does
``j`` explain ``i`` (treating ``i`` as the response)" — so the matrix is
intentionally asymmetric: ``M.loc[i, j] != M.loc[j, i]`` carries
directional information about explanatory power.

The default ``measure="aic"`` path (H-0006) routes through
:func:`pycatdap.target_summary` so continuous targets are handled via
the H-0005 regression-AIC machinery. H-0008 PR-D5 extends the function
to dispatch on any registered :mod:`pycatdap.measures` measure: for
non-AIC measures, both columns are binned uniformly (via
:func:`pandas.qcut`) and a crosstab is built before applying the
measure callable.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

from pycatdap import measures
from pycatdap._target_pair import target_summary
from pycatdap.measures._registry import Measure

Criterion = Literal["aic", "aicc", "bic"]


def association_matrix(
    df: pd.DataFrame,
    *,
    measure: str = "aic",
    bins: int | None = None,
    criterion: Criterion = "bic",
) -> pd.DataFrame:
    """Compute the m × m association matrix across all column pairs.

    For each ordered pair ``(i, j)`` with ``i != j``, the cell holds
    the association score between the target ``i`` and the explanatory
    ``j``. The matrix is **asymmetric** — for ``measure="aic"`` this is
    because ΔAIC depends on which side is treated as the response;
    for other measures (cramers_v, mutual_info, etc.) the score itself
    is symmetric but binning artefacts and missing-value patterns can
    still make the matrix asymmetric in practice.

    The diagonal is ``NaN`` (self-association is mathematically
    undefined under all supported measures).

    Parameters
    ----------
    df : DataFrame
        Source data; all columns are scanned.
    measure : str
        Name of a registered :mod:`pycatdap.measures` measure. The
        standard built-ins are ``"aic"`` (default; uses
        :func:`target_summary` so continuous targets work via the
        H-0005 regression AIC), ``"cramers_v"``, and ``"mutual_info"``.
        Any custom measure registered via
        :func:`pycatdap.measures.register` is also accepted.
    bins : int or None
        Binning specification. For ``measure="aic"`` this is forwarded
        to :func:`target_summary`; ``None`` selects AIC-optimal
        binning. For non-AIC measures, ``bins`` is the number of
        quantiles (``pd.qcut``) used to bin continuous columns;
        ``None`` defaults to 5.
    criterion : {'aic', 'aicc', 'bic'}
        Penalty family for the Gaussian regression path. Ignored for
        non-AIC measures and for cells where the target is
        categorical.

    Returns
    -------
    DataFrame
        Square ``(n_cols, n_cols)`` frame indexed and column-labelled by
        ``df.columns``. Diagonal is ``NaN``.

    Raises
    ------
    ValueError
        If *df* has no columns.
    KeyError
        If *measure* is not registered. Use
        :func:`pycatdap.measures.list_measures` to see the available
        names.

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
    cols = list(df.columns)
    if not cols:
        msg = "association_matrix: df must have at least one column"
        raise ValueError(msg)

    if measure == "aic":
        return _aic_matrix(df, cols, bins=bins, criterion=criterion)

    # Non-AIC path: look up the measure callable, then build cross-freqs
    # via uniform qcut binning of continuous columns.
    measure_fn = measures.get(measure)
    return _generic_measure_matrix(df, cols, measure_fn, bins=bins)


def _aic_matrix(
    df: pd.DataFrame,
    cols: list[str],
    *,
    bins: int | None,
    criterion: Criterion,
) -> pd.DataFrame:
    """ΔAIC matrix via target_summary (preserves the H-0006 behavior)."""
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


def _generic_measure_matrix(
    df: pd.DataFrame,
    cols: list[str],
    measure_fn: Measure,
    *,
    bins: int | None,
) -> pd.DataFrame:
    """Compute a measure matrix via qcut binning + crosstab.

    Both columns are coerced to categorical via :func:`_binize` so the
    same measure callable works regardless of the input dtypes. The
    measure is applied to the resulting ``(C_target × C_explanatory)``
    cross-frequency table.
    """
    n_bins = bins if bins is not None else 5
    binned: dict[str, pd.Series] = {col: _binize(df[col], n_bins) for col in cols}

    matrix = np.full((len(cols), len(cols)), np.nan, dtype=float)
    for i, target in enumerate(cols):
        for j, explanatory in enumerate(cols):
            if i == j:
                continue
            ct = pd.crosstab(binned[target], binned[explanatory])
            if ct.size == 0 or ct.to_numpy().sum() == 0:
                # No overlapping non-null observations — leave NaN.
                continue
            matrix[i, j] = float(measure_fn(ct.to_numpy(dtype=np.float64)))
    return pd.DataFrame(matrix, index=cols, columns=cols)


def _binize(series: pd.Series, n_bins: int) -> pd.Series:
    """Coerce a continuous-numeric series to categorical via qcut.

    Boolean and non-numeric series are returned unchanged. NaN values
    are mapped to a distinct ``_missing_`` category so they participate
    in the crosstab. ``pd.qcut`` with ``duplicates="drop"`` is robust
    against all-NaN, constant, and degenerate distributions — no
    additional fallback is required.
    """
    if pd.api.types.is_bool_dtype(series) or not pd.api.types.is_numeric_dtype(series):
        return series.astype("object").fillna("_missing_")
    binned: pd.Series = pd.qcut(series, q=n_bins, duplicates="drop")
    # Render to strings so the cross-tab indexes look the same as the
    # categorical / object path above and missing values fold in.
    return binned.astype("object").fillna("_missing_")


__all__ = ["association_matrix"]
