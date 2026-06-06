"""DivExplorer 0.2.x schema rendering (H-0019, #32).

Shared by :meth:`SliceDiscoveryResult.to_divexplorer_format` and
:meth:`ErrorAnalysisResult.to_divexplorer_format` (``schema="divexplorer"``).
Both result types reduce their slices to the same four primitives — itemset,
size, error rate, significance — and this module turns those into the
DivExplorer-0.2.6 column layout
``support / itemset / error / error_div / error_t / length / support_count``
(verified against divexplorer 0.2.6).

``error_t`` carries pycatdap's own statistic (``measure_value`` for multivariable
slices, ``pearson_residual`` for single-variable cells), NOT DivExplorer's
Bayesian/Welch t-value — see ``docs/interop/divexplorer.md``.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

#: DivExplorer 0.2.6 column order (support first), verified empirically.
DIVEXPLORER_COLUMNS = [
    "support",
    "itemset",
    "error",
    "error_div",
    "error_t",
    "length",
    "support_count",
]

#: One slice reduced to the primitives the schema needs:
#: ``(itemset, size, error_rate, significance)``.
DivexplorerRow = tuple[frozenset[str], int, float, float]


def empty_divexplorer_frame() -> pd.DataFrame:
    """Return a typed, empty DivExplorer-0.2.x frame.

    Returns
    -------
    DataFrame
        Zero rows, the seven DivExplorer columns, correct dtypes — so
        downstream numeric consumers do not trip over all-object columns.
    """
    return pd.DataFrame(
        {
            "support": pd.Series([], dtype="float64"),
            "itemset": pd.Series([], dtype="object"),
            "error": pd.Series([], dtype="float64"),
            "error_div": pd.Series([], dtype="float64"),
            "error_t": pd.Series([], dtype="float64"),
            "length": pd.Series([], dtype="int64"),
            "support_count": pd.Series([], dtype="float64"),
        }
    )


def build_divexplorer_frame(
    rows: Iterable[DivexplorerRow],
    *,
    n_total: int | None,
    overall_error_rate: float | None,
) -> pd.DataFrame:
    """Render slices into the DivExplorer 0.2.x schema.

    Parameters
    ----------
    rows : iterable of (frozenset[str], int, float, float)
        ``(itemset, size, error_rate, significance)`` per slice.
    n_total : int or None
        Total dataset row count (denominator of ``support``). Must be a
        positive integer.
    overall_error_rate : float or None
        Dataset-wide error rate (subtracted to form ``error_div``).

    Returns
    -------
    DataFrame
        Columns ``support / itemset / error / error_div / error_t /
        length / support_count``; empty (typed) when ``rows`` is empty.

    Raises
    ------
    ValueError
        If ``n_total`` is missing/non-positive or ``overall_error_rate``
        is missing — the caller must supply them (the result may not carry
        them; pass explicitly).
    """
    if n_total is None or n_total <= 0:
        msg = (
            "to_divexplorer_format(schema='divexplorer') needs a positive n_total "
            "(dataset row count); the result does not carry one. Pass "
            "n_total=<rows> explicitly."
        )
        raise ValueError(msg)
    if overall_error_rate is None:
        msg = (
            "to_divexplorer_format(schema='divexplorer') needs overall_error_rate "
            "(dataset error rate). Pass overall_error_rate=<rate> explicitly."
        )
        raise ValueError(msg)

    records = [
        {
            "support": size / n_total,
            "itemset": itemset,
            "error": float(error_rate),
            "error_div": float(error_rate) - overall_error_rate,
            "error_t": float(significance),
            "length": len(itemset),
            # float to match DivExplorer 0.2.6's dtype (it stores the integer
            # count as float64 = round(support × N)).
            "support_count": float(size),
        }
        for itemset, size, error_rate, significance in rows
    ]
    if not records:
        return empty_divexplorer_frame()
    return pd.DataFrame(records, columns=DIVEXPLORER_COLUMNS)
