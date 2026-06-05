"""pysubgroup interop: AIC as an interestingness measure (H-0018, #31).

:class:`AICMeasure` bridges pycatdap's ΔAIC to pysubgroup's binary-target
quality-function interface, so AIC can drive pysubgroup's subgroup
discovery (``BeamSearch`` / ``SimpleDFS``).

pysubgroup is an **optional** dependency. Importing this module raises a
clear :class:`ImportError` pointing at the ``pycatdap[subgroup]`` extra
when pysubgroup is absent; :mod:`pycatdap.measures` only imports it lazily
(via ``__getattr__``) so the package never hard-depends on pysubgroup.

Scope
-----
``AICMeasure`` implements ``evaluate`` only and deliberately does **not**
provide ``optimistic_estimate`` (it subclasses ``SimplePositivesQF``, not
``BoundedInterestingnessMeasure``). ΔAIC has no sound optimistic upper
bound (HISTORY H-0014 §C), so an estimate would make Apriori / DFS pruning
unsound. The measure is therefore intended for ``BeamSearch`` and
``SimpleDFS``, which evaluate every candidate and need no bound.
"""

from __future__ import annotations

from typing import Any

import numpy as np

try:
    from pysubgroup import SimplePositivesQF
except ImportError as exc:  # pragma: no cover - exercised via sys.modules mask
    # pysubgroup is intentionally NOT a pycatdap extra: it pins ``numpy<2.0.0``,
    # and uv's universal lock would propagate that cap to every install. Users
    # opt in explicitly with ``pip install pysubgroup``. See HISTORY H-0018.
    msg = (
        "pysubgroup is required for AICMeasure. Install it explicitly with: "
        "pip install pysubgroup"
    )
    raise ImportError(msg) from exc

from pycatdap.measures._aic import aic


class AICMeasure(SimplePositivesQF):
    """ΔAIC as a pysubgroup binary-target interestingness measure.

    Reuses pysubgroup's ``SimplePositivesQF`` statistics machinery, which
    supplies the dataset totals ``(N, P)`` (rows, positives) and the
    subgroup counts ``(n, p)``. From those it forms the 2×2 contingency
    table of *target* (positive / negative) against *subgroup membership*
    (in / out) and scores it with :func:`pycatdap.measures.aic`.

    pysubgroup **maximises** quality, whereas ΔAIC is negative for an
    informative split, so the returned quality is ``-ΔAIC`` — higher means
    more informative.

    Notes
    -----
    Use with ``pysubgroup.BeamSearch`` or ``pysubgroup.SimpleDFS``. Apriori
    / DFS are unsupported: they need ``optimistic_estimate``, which ΔAIC
    cannot provide soundly (H-0014 §C).

    Examples
    --------
    >>> import pysubgroup as ps                          # doctest: +SKIP
    >>> import pycatdap                                  # doctest: +SKIP
    >>> task = ps.SubgroupDiscoveryTask(                 # doctest: +SKIP
    ...     df, ps.BinaryTarget("y", True),
    ...     ps.create_selectors(df, ignore=["y"]),
    ...     qf=pycatdap.measures.AICMeasure(),
    ... )
    >>> result = ps.BeamSearch().execute(task)           # doctest: +SKIP
    """

    def evaluate(
        self,
        subgroup: Any,
        target: Any,
        data: Any,
        statistics: Any = None,
    ) -> float:
        """Return ``-ΔAIC`` for the subgroup's target/membership table.

        Parameters
        ----------
        subgroup : Any
            A pysubgroup selector / conjunction, or precomputed cover.
        target : pysubgroup.BinaryTarget
            The binary target definition.
        data : pandas.DataFrame
            The dataset.
        statistics : Any, optional
            Cached statistics tuple; recomputed when ``None``.

        Returns
        -------
        float
            ``-ΔAIC`` (higher = more informative); ``nan`` for an empty
            subgroup (matching pysubgroup's ``StandardQF`` convention).
        """
        statistics = self.ensure_statistics(subgroup, target, data, statistics)
        # ``dataset_statistics`` is the attribute pysubgroup's own
        # ``SimplePositivesQF`` / ``StandardQF`` populate in
        # ``calculate_constant_statistics``; re-check on a pysubgroup upgrade.
        dataset = self.dataset_statistics
        n_total = int(dataset.size_sg)
        pos_total = int(dataset.positives_count)
        n_sg = int(statistics.size_sg)
        pos_sg = int(statistics.positives_count)
        if n_sg == 0:
            return float("nan")
        # Rows = target (positive, negative); columns = subgroup membership
        # (in, out). All cells are non-negative for any 0 < n_sg <= n_total with
        # consistent counts.
        table = np.array(
            [
                [pos_sg, pos_total - pos_sg],
                [n_sg - pos_sg, (n_total - n_sg) - (pos_total - pos_sg)],
            ],
            dtype=np.float64,
        )
        # Defensive: a negative cell means the upstream counts are inconsistent
        # (e.g. positives outside their containing set). `aic` would return a
        # silent garbage value, so treat it like an unusable subgroup instead.
        if np.any(table < 0):
            return float("nan")
        # A whole-dataset / degenerate split has an all-zero column; the
        # 0·ln0=0 convention in `aic` handles it, but numpy's eager divide
        # warns — suppress locally rather than leak a RuntimeWarning.
        with np.errstate(divide="ignore", invalid="ignore"):
            return -aic(table)


__all__ = ["AICMeasure"]
