# pysubgroup interoperability

[pysubgroup](https://github.com/flemmerich/pysubgroup) is a popular Python library
for **subgroup discovery** — finding interpretable conditions (conjunctions of
selectors) under which a target behaves unusually. pycatdap exposes its
AIC-based interestingness as a pysubgroup-compatible quality function,
`pycatdap.measures.AICMeasure`, so you can drive pysubgroup's search with the
same ΔAIC criterion pycatdap's native `discover_error_slices` uses.

!!! info "Status (what this page covers)"
    `AICMeasure` ships as of this release (H-0018, [issue #31](https://github.com/nbx-liz/pycatdap/issues/31)).
    pysubgroup is an **optional** dependency — install it with the `subgroup`
    extra. The measure is designed for pysubgroup's `BeamSearch` / `SimpleDFS`;
    see [Scope](#scope-beamsearch--simpledfs-not-apriori) for why Apriori / DFS
    are out of scope.

## Install

```bash
pip install 'pycatdap[subgroup]'   # pulls in pysubgroup
```

Importing `pycatdap.measures` never requires pysubgroup; only
`pycatdap.measures.AICMeasure` does. Accessing it without pysubgroup installed
raises a clear `ImportError` pointing at the extra.

## Side-by-side example

```python
import numpy as np
import pandas as pd
import pysubgroup as ps
import pycatdap

# A dataset where column `a` is informative about the binary target and
# column `b` is noise.
rng = np.random.RandomState(0)
n = 600
a = rng.choice(["x", "y"], n)
b = rng.choice(["p", "q"], n)
target = ((a == "x") & (rng.rand(n) < 0.85)) | ((a == "y") & (rng.rand(n) < 0.15))
df = pd.DataFrame({"a": a, "b": b, "target": target})

# --- pysubgroup search driven by AIC ---
task = ps.SubgroupDiscoveryTask(
    df,
    ps.BinaryTarget("target", True),
    ps.create_selectors(df, ignore=["target"]),
    result_set_size=5,
    depth=2,
    qf=pycatdap.measures.AICMeasure(),     # <-- AIC as the quality function
)
result = ps.BeamSearch().execute(task)
for quality, subgroup in result.to_descriptions():
    print(f"{quality:8.3f}  {subgroup}")
# The informative column `a` tops the ranking; `b` only appears (weakly)
# in conjunctions.
```

The same signal, via pycatdap's native API:

```python
from pycatdap.error import discover_error_slices

# Treat the binary outcome as an "error" label and discover the slices that
# concentrate it — driven by the same ΔAIC.
y_pred = np.zeros(n, dtype=int)
native = discover_error_slices(
    df.drop(columns="target"), target.astype(int), y_pred, max_vars=1
)
for s in native.slices:
    print(s.description, s.delta_aic)
```

Both routes surface column `a` as the most informative variable, because both
score candidate subgroups by ΔAIC.

## How the bridge works

pysubgroup's binary-target quality functions receive, per candidate subgroup,
the dataset totals `(N, P)` (rows, positives) and the subgroup counts `(n, p)`.
`AICMeasure` turns those into the 2×2 contingency table of **target** against
**subgroup membership**

|              | target = positive | target = negative      |
| ------------ | :---------------: | :--------------------: |
| in subgroup  | `p`               | `n − p`                |
| out subgroup | `P − p`           | `(N − n) − (P − p)`    |

and scores it with `pycatdap.measures.aic` (ΔAIC of the two-way model against
the null model).

pysubgroup **maximises** quality, while ΔAIC is **negative** for an informative
split, so the returned quality is `-ΔAIC` — higher means more informative. An
empty subgroup yields `nan` (matching pysubgroup's own `StandardQF`).

## Scope: BeamSearch / SimpleDFS, not Apriori

`AICMeasure` implements `evaluate` only; it deliberately does **not** provide
`optimistic_estimate`. ΔAIC has no sound optimistic upper bound (pycatdap's own
slice discovery prunes by support, not ΔAIC — see HISTORY `H-0014 §C`), so an
estimate would make pruning-based algorithms unsound.

| pysubgroup algorithm | uses `optimistic_estimate`? | works with `AICMeasure`? |
| -------------------- | :-------------------------: | :----------------------: |
| `BeamSearch`         | no                          | ✅ yes                   |
| `SimpleDFS`          | no                          | ✅ yes                   |
| `Apriori`            | yes                         | ❌ no                    |
| `DFS`                | yes                         | ❌ no                    |

Use `BeamSearch` (or `SimpleDFS`) — they evaluate every candidate and need no
bound.
