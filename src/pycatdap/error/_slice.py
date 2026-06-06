"""Result containers for multivariable error-slice discovery (H-0014 PR-L2).

Introduces :class:`ErrorSlice` (a multivariable subgroup where an error
category concentrates) and :class:`SliceDiscoveryResult` (the immutable
container returned by :func:`pycatdap.error.discover_error_slices`,
shipped in PR-L3).

These are the *multivariable* analogue of the single-variable
:class:`pycatdap.error.Slice` (in :mod:`pycatdap.error._result`). ``Slice``
is intentionally left unchanged — Phase H surfaces single-variable cells,
Phase L composes conditions across variables. Both coexist.

Immutability follows the H-0009 discipline: frozen dataclasses, tuple
fields (already immutable), and DataFrames are produced fresh on each
``to_*`` call rather than stored mutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd

from pycatdap.error._describe import build_description
from pycatdap.error._divexplorer import build_divexplorer_frame


@dataclass(frozen=True)
class ErrorSlice:
    """A multivariable subgroup where one error category concentrates.

    Attributes
    ----------
    conditions : tuple[tuple[str, str], ...]
        The AND-ed ``(column, value)`` conditions defining the subgroup,
        e.g. ``(("age", "[45, 60]"), ("marital_status", "Never-married"))``.
        Each ``value`` is a category label or an interval label (see
        :mod:`pycatdap.error._describe`). Stored as a tuple-of-tuples so
        the slice stays hashable and frozen.
    size : int
        Number of rows matching all conditions (the slice support).
    error_metric : float
        Error rate within the slice (``n_error_in_slice / size``).
    delta_aic : float
        ΔAIC of the variable subset against the error-label response.
        Shared by all cells of the same subset.
    measure_value : float
        The chosen interestingness score (ΔAIC, Cramér's V, mutual
        information, or a custom measure).
    n_error_in_slice : int
        Count of rows in the slice that fall under the error category.
    description : str
        Human-readable rendering of ``conditions``, e.g.
        ``"age ∈ [45, 60] × marital_status = Never-married"``. Derived
        automatically in ``__post_init__`` (``init=False``) so it can
        never drift from ``conditions``, regardless of how the instance
        is built.
    """

    conditions: tuple[tuple[str, str], ...]
    size: int
    error_metric: float
    delta_aic: float
    measure_value: float
    n_error_in_slice: int
    description: str = field(init=False)

    def __post_init__(self) -> None:
        # Derive description from conditions on a frozen dataclass via
        # object.__setattr__. Single source of truth — there is no way
        # for a caller to pass a mismatched description.
        object.__setattr__(self, "description", build_description(self.conditions))

    @classmethod
    def from_conditions(
        cls,
        conditions: tuple[tuple[str, str], ...],
        *,
        size: int,
        error_metric: float,
        delta_aic: float,
        measure_value: float,
        n_error_in_slice: int,
    ) -> ErrorSlice:
        """Build an ErrorSlice with keyword-only metrics + numeric coercion.

        ``description`` is always derived from ``conditions`` (see
        ``__post_init__``); callers never supply it.

        Parameters
        ----------
        conditions : tuple[tuple[str, str], ...]
            ``(column, value)`` pairs.
        size, error_metric, delta_aic, measure_value, n_error_in_slice
            See the class attributes.

        Returns
        -------
        ErrorSlice
        """
        return cls(
            conditions=tuple(conditions),
            size=int(size),
            error_metric=float(error_metric),
            delta_aic=float(delta_aic),
            measure_value=float(measure_value),
            n_error_in_slice=int(n_error_in_slice),
        )


@dataclass(frozen=True)
class SliceDiscoveryResult:
    """Immutable result of :func:`pycatdap.error.discover_error_slices`.

    Attributes
    ----------
    slices : tuple[ErrorSlice, ...]
        Top-``k`` discovered slices, sorted descending by
        ``measure_value``.
    measure : str
        Name of the interestingness measure used (``"aic"`` /
        ``"cramers_v"`` / ``"mutual_info"`` / ``"<callable>"``).
    max_vars : int
        Maximum number of variables combined per slice.
    base_aic : float
        AIC of the null model (error label with no explanatory variable).
    n_evaluated : int
        Number of variable-subset combinations actually scored.
    n_pruned : int
        Number of combinations skipped by support pruning. The pruning
        ratio ``n_pruned / (n_evaluated + n_pruned)`` quantifies the
        search-space reduction (Issue #20 acceptance criterion).
    label_kind : str
        Which Phase G labeller produced the synthetic response
        (``"error_label"`` etc.).
    truncated : bool
        ``True`` if the search hit ``max_candidates`` and stopped early.
        The returned slices are still a sound subset (real frequent cells
        with correct support), just not exhaustive (H-0016).
    n_total : int
        Total dataset row count. Denominator of DivExplorer ``support``
        (H-0019). ``0`` only when built outside ``discover_error_slices``
        (then ``schema="divexplorer"`` raises unless ``n_total=`` is passed).
    base_error_rate : float
        Dataset-wide error rate. Subtracted to form DivExplorer
        ``error_div`` (H-0019). The ``0.0`` default is a sentinel for
        "built outside ``discover_error_slices``", **not** a reliable
        overall rate — when constructing manually, pass
        ``overall_error_rate=`` to ``to_divexplorer_format(schema="divexplorer")``.
    """

    slices: tuple[ErrorSlice, ...]
    measure: str
    max_vars: int
    base_aic: float
    n_evaluated: int
    n_pruned: int
    label_kind: str = field(default="error_label")
    truncated: bool = field(default=False)
    n_total: int = field(default=0)
    base_error_rate: float = field(default=0.0)

    # ------------------------------------------------------------------
    # to_divexplorer_format()
    # ------------------------------------------------------------------

    def to_divexplorer_format(
        self,
        *,
        schema: Literal["native", "divexplorer"] = "native",
        n_total: int | None = None,
        overall_error_rate: float | None = None,
    ) -> pd.DataFrame:
        """Return a flat DataFrame of slices in the requested schema.

        Parameters
        ----------
        schema : {"native", "divexplorer"}, default "native"
            ``"native"`` (default, unchanged since v0.8.0): columns
            ``description / size / error_rate / delta_aic / measure_value
            / n_error_in_slice``. ``"divexplorer"``: the DivExplorer 0.2.x
            layout ``support / itemset / error / error_div / error_t /
            length / support_count`` (H-0019, #32).
        n_total : int or None
            DivExplorer ``support`` denominator. Defaults to
            :attr:`n_total`; pass to override. Ignored for ``"native"``.
        overall_error_rate : float or None
            Dataset error rate for ``error_div``. Defaults to
            :attr:`base_error_rate`; pass to override. Ignored for
            ``"native"``.

        Returns
        -------
        DataFrame
            One row per :class:`ErrorSlice`; a well-typed empty frame when
            no slice was found.

        Raises
        ------
        ValueError
            If ``schema`` is unknown, or ``schema="divexplorer"`` and no
            positive ``n_total`` is available.

        Notes
        -----
        For ``"divexplorer"``, ``error_t`` carries ``measure_value`` (this
        multivariable container's statistic), **not** DivExplorer's
        t-value. See ``docs/interop/divexplorer.md``.
        """
        if schema == "divexplorer":
            rows = (
                (
                    frozenset(f"{var}={val}" for var, val in s.conditions),
                    int(s.size),
                    float(s.error_metric),
                    float(s.measure_value),
                )
                for s in self.slices
            )
            return build_divexplorer_frame(
                rows,
                n_total=self.n_total if n_total is None else n_total,
                overall_error_rate=(
                    self.base_error_rate
                    if overall_error_rate is None
                    else overall_error_rate
                ),
            )
        if schema != "native":
            msg = f"schema must be 'native' or 'divexplorer'; got {schema!r}"
            raise ValueError(msg)
        if not self.slices:
            # Preserve column dtypes on the empty frame so downstream
            # numeric consumers don't trip over all-object columns.
            return pd.DataFrame(
                {
                    "description": pd.Series([], dtype="object"),
                    "size": pd.Series([], dtype="int64"),
                    "error_rate": pd.Series([], dtype="float64"),
                    "delta_aic": pd.Series([], dtype="float64"),
                    "measure_value": pd.Series([], dtype="float64"),
                    "n_error_in_slice": pd.Series([], dtype="int64"),
                }
            )
        records = [
            {
                "description": s.description,
                "size": int(s.size),
                "error_rate": float(s.error_metric),
                "delta_aic": float(s.delta_aic),
                "measure_value": float(s.measure_value),
                "n_error_in_slice": int(s.n_error_in_slice),
            }
            for s in self.slices
        ]
        return pd.DataFrame(
            records,
            columns=[
                "description",
                "size",
                "error_rate",
                "delta_aic",
                "measure_value",
                "n_error_in_slice",
            ],
        )

    # ------------------------------------------------------------------
    # to_dict()
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable summary of the discovery result.

        Returns
        -------
        dict
            Scalar metadata plus a ``slices`` list of per-slice dicts
            (``conditions`` rendered as a list of ``[column, value]``
            pairs).
        """
        return {
            "measure": self.measure,
            "max_vars": int(self.max_vars),
            "base_aic": float(self.base_aic),
            "n_evaluated": int(self.n_evaluated),
            "n_pruned": int(self.n_pruned),
            "label_kind": self.label_kind,
            "truncated": bool(self.truncated),
            "n_total": int(self.n_total),
            "base_error_rate": float(self.base_error_rate),
            "slices": [
                {
                    "conditions": [list(c) for c in s.conditions],
                    "description": s.description,
                    "size": int(s.size),
                    "error_rate": float(s.error_metric),
                    "delta_aic": float(s.delta_aic),
                    "measure_value": float(s.measure_value),
                    "n_error_in_slice": int(s.n_error_in_slice),
                }
                for s in self.slices
            ],
        }
