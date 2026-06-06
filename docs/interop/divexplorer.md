# DivExplorer interoperability

[DivExplorer](https://github.com/divexplorer/divexplorer) is the closest direct
competitor to pycatdap's error-analysis layer: both surface **subgroups
(itemsets / slices) where a model's error behaviour diverges from the dataset as
a whole**. This page explains how to move data between the two tools.

!!! info "Status (what this page covers)"
    `ErrorAnalysisResult.to_divexplorer_format()` and
    `SliceDiscoveryResult.to_divexplorer_format()` (since v0.8.0) return
    **pycatdap-native columns** by default. As of H-0019 (#32) they also accept
    **`schema="divexplorer"`**, which emits DivExplorer's real 0.2.x column layout
    natively — see [Native DivExplorer schema](#native-divexplorer-schema) below.
    This page documents (a) what each tool emits, (b) how the metrics correspond,
    and (c) the native `schema=` switch (plus the equivalent manual adapter).

## Native DivExplorer schema

Pass `schema="divexplorer"` to get DivExplorer-0.2.x-compatible columns
(`support / itemset / error / error_div / error_t / length / support_count`)
directly — no manual reshaping:

```python
import numpy as np
from pycatdap.datasets import load_titanic
from pycatdap.error import discover_error_slices

df = load_titanic()
y_true = df["Survived"]
y_pred = np.where(df["Sex"].eq("Female"), "Yes", "No")

result = discover_error_slices(df[["Class", "Sex", "Age"]], y_true, y_pred, max_vars=2)
dx = result.to_divexplorer_format(schema="divexplorer")
# columns: support, itemset, error, error_div, error_t, length, support_count
```

`SliceDiscoveryResult` carries `n_total` and `base_error_rate`, so `support` and
`error_div` are computed automatically; pass `n_total=` / `overall_error_rate=`
to override. For `ErrorAnalysisResult` they default to `n_rows` and
`n_incorrect / n_rows` (classification); pass `overall_error_rate=` for
regression. `schema="native"` (the default) is unchanged.

!!! warning "`error_t` is not DivExplorer's t-value"
    `error_t` carries pycatdap's own statistic (`measure_value` for multivariable
    slices, `pearson_residual` for single-variable cells), **not** DivExplorer's
    Bayesian/Welch t-value. Use it for *ranking*, not as an equivalent
    significance score. pycatdap also surfaces only the top error-concentrated
    slices, so (unlike DivExplorer) the frame omits the all-dataset **root row**.

## pycatdap's `to_divexplorer_format()` output

`to_divexplorer_format()` returns one row per surfaced slice as a flat
`DataFrame`. The two result types share `description / size / error_rate /
delta_aic` and differ in the trailing columns:

| Column | `ErrorAnalysisResult` | `SliceDiscoveryResult` | Meaning |
| --- | :---: | :---: | --- |
| `description` | ✓ | ✓ | Human-readable slice, e.g. `Sex = Female` (single) or `Class = 3rd × Sex = Female` (multivariable) |
| `size` | ✓ | ✓ | Number of rows in the slice |
| `error_rate` | ✓ | ✓ | Error rate within the slice |
| `delta_aic` | ✓ | ✓ | ΔAIC of the slice's error concentration (more negative = stronger signal) |
| `pearson_residual` | ✓ | — | Standardised residual of the single-variable cell |
| `error_category` | ✓ | — | Which error type concentrates (e.g. `FP` / `FN`) |
| `variable` / `category` | ✓ | — | The single `(variable, category)` cell |
| `measure_value` | — | ✓ | The association measure (default AIC) for the multivariable slice |
| `n_error_in_slice` | — | ✓ | Count of errors inside the slice |

```python
import pycatdap as pc
from pycatdap.error import discover_error_slices

result = discover_error_slices(features_df, y_true, y_pred, max_vars=2)
flat = result.to_divexplorer_format()
# columns: description, size, error_rate, delta_aic, measure_value, n_error_in_slice
```

## DivExplorer's output schema

DivExplorer's pattern-divergence call returns one row per frequent itemset. **The
exact column names depend on the package generation** — this is the single
biggest interop gotcha:

### New generation — DivExplorer 0.2.x (latest 0.2.6)

`DivergenceExplorer.get_pattern_divergence(...)`:

| Column | dtype | Meaning |
| --- | --- | --- |
| `itemset` | `frozenset[str]` | The pattern as a frozenset of `"attr=value"` strings; the all-dataset root row is `frozenset()` |
| `support` | `float` | Fraction of rows matching the itemset (root row = `1.0`) |
| `<metric>` | `float` | Subgroup mean of the outcome, named after the bare outcome (e.g. `fp`) |
| `<metric>_div` | `float` | **Divergence** = subgroup mean − overall mean (root row = `0`) |
| `<metric>_t` | `float` | Significance (Bayesian/Welch t-value) of the divergence |
| `length` | `int` | Number of items in the itemset (root = `0`) |
| `support_count` | `float` | Absolute row count = `round(support × N)` |

The frame is sorted by descending `support` and **includes the all-dataset root
row** (empty itemset). Verbose mode (`show_coincise=False`) adds boolean-only
`<metric>_positive` / `_negative` / `_bottom` count columns that are dropped by
default.

### Old generation — DivExplorer 0.1.x

`FP_DivergenceExplorer.getFrequentPatternDivergence(...)` is the SIGMOD-paper-era
API and **does not exist in the 0.2.x line**. If you target it, note the
different names: the itemset column is `itemsets` (**plural**), divergence is
`d_<metric>` (default `d_fpr` / `d_fnr` / `d_accuracy`), and the significance
column is named after the metric's confusion cells — `t_value_fp`, `t_value_fn`,
`t_value_tp_tn` — **not** after the metric. It also exposes the raw confusion
cells `tn / fp / fn / tp`.

## Metric correspondence: AIC ↔ divergence

The two tools answer the same question with different statistics. Map them
conceptually as follows:

| Concept | DivExplorer | pycatdap |
| --- | --- | --- |
| Subgroup definition | `itemset` (frozenset of `attr=value`) | `description` (`var = cat` joined by `×`) |
| Subgroup size | `support` / `support_count` | `size` |
| Error level in subgroup | `<metric>` (e.g. `fp` = false-positive rate) | `error_rate` |
| **Divergence** (subgroup − overall) | `<metric>_div` | `error_rate − overall_error_rate` |
| **Significance** of the divergence | `<metric>_t` (beta/Welch t-value) | `pearson_residual` (single cell) or `delta_aic` / `measure_value` (multivariable) |

The key semantic difference: DivExplorer ranks by a **statistical t-value** of a
chosen classification metric's divergence, whereas pycatdap ranks by an
**AIC-based** measure of error concentration (with a Pearson residual for
single-variable cells). They are correlated — both elevate the same egregious
subgroups — but the numbers are **not** interchangeable. Treat the pycatdap
statistic as a *rank-compatible analogue*, not a drop-in replacement for
DivExplorer's t-value.

## Adapter: reshape a native frame toward DivExplorer 0.2.x

!!! tip "Prefer the native `schema="divexplorer"`"
    Since H-0019 (#32), `to_divexplorer_format(schema="divexplorer")` produces
    this exact layout for you — see [Native DivExplorer schema](#native-divexplorer-schema).
    The manual adapter below is kept only for reshaping a frame you already
    captured in the native schema (or from an older pycatdap).

The helper below converts a `to_divexplorer_format()` (native) frame into a
DivExplorer-0.2.x-*shaped* frame (`itemset / support / error / error_div /
error_t / length / support_count`). It works for both result types — for
`ErrorAnalysisResult` it uses `pearson_residual` as the significance column, for
`SliceDiscoveryResult` it uses `measure_value`.

```python
import pandas as pd


def to_divexplorer_like(
    flat: pd.DataFrame,
    *,
    n_total: int,
    overall_error_rate: float,
    significance_col: str | None = None,
) -> pd.DataFrame:
    """Reshape a pycatdap ``to_divexplorer_format()`` frame toward DivExplorer 0.2.x.

    Produces: itemset, support, error, error_div, error_t, length, support_count.

    Note
    ----
    ``error_t`` carries pycatdap's own statistic (Pearson residual or AIC
    measure), NOT DivExplorer's Bayesian beta t-value — see the caveat below.
    """
    def parse_itemset(desc: str) -> frozenset:
        items = []
        for part in desc.split("×"):
            part = part.strip()
            if " = " in part:
                var, cat = part.split(" = ", 1)
                items.append(f"{var.strip()}={cat.strip()}")
            else:
                items.append(part)
        return frozenset(items)

    if significance_col is None:
        significance_col = (
            "pearson_residual" if "pearson_residual" in flat.columns else "measure_value"
        )
    itemset = flat["description"].map(parse_itemset)
    out = pd.DataFrame(
        {
            "itemset": itemset,
            "support": flat["size"] / n_total,
            "error": flat["error_rate"],
            "error_div": flat["error_rate"] - overall_error_rate,
            "error_t": flat[significance_col],
            "length": itemset.map(len),
            "support_count": flat["size"].astype(int),
        }
    )
    return out.sort_values("support", ascending=False).reset_index(drop=True)
```

Usage:

```python
import numpy as np
from pycatdap.datasets import load_titanic
from pycatdap.error import discover_error_slices

df = load_titanic()
features = df[["Class", "Sex", "Age"]]
y_true = df["Survived"]
y_pred = np.where(df["Sex"].eq("Female"), "Yes", "No")

result = discover_error_slices(features, y_true, y_pred, max_vars=2, top_k=5)
flat = result.to_divexplorer_format()

overall_error_rate = float((y_true.astype(str).to_numpy() != y_pred.astype(str)).mean())
dx = to_divexplorer_like(flat, n_total=len(df), overall_error_rate=overall_error_rate)
print(dx)
#                               itemset   support     error  error_div     error_t  length  support_count
# 0   frozenset({Age=Adult, Class=3rd})  0.284871  0.261563   0.037574   47.063486       2            627
# 1  frozenset({Sex=Female, Class=3rd})  0.089050  0.540816   0.316827  163.737731       2            196
# ...
```

## Caveats

- **`error_div` needs the overall error rate**, which is not carried in the
  flat frame — pass it explicitly (compute it once from your `y_true`/`y_pred`).
- **`error_t` is not DivExplorer's t-value.** It is pycatdap's Pearson residual
  (single-variable) or AIC measure (multivariable). Use it for *ranking*, not as
  a statistically equivalent significance score.
- DivExplorer emits **one column triple per metric** (e.g. `fpr`, `fnr`,
  `accuracy`) and includes the **root row**; pycatdap surfaces only the
  top error-concentrated slices for a single error notion. Slice sets will
  therefore overlap but not match one-to-one.
- Column names differ by DivExplorer generation (`itemset` vs `itemsets`,
  `<metric>_div` vs `d_<metric>`, `<metric>_t` vs `t_value_<cells>`). The adapter
  above targets the **0.2.x** names.
- The adapter emits `support_count` as `int` (an absolute row count); DivExplorer
  0.2.x natively stores it as `float` (`round(support × N)`). Cast with
  `.astype(float)` if exact dtype parity matters to your downstream consumer.

## Status

Native, drop-in column compatibility with DivExplorer 0.2.x — so that
`to_divexplorer_format(schema="divexplorer")` emits the real schema — **shipped**
in the v0.13.0 interop track ([issue #32](https://github.com/nbx-liz/pycatdap/issues/32),
HISTORY H-0019). The additive `schema=` switch went through the Change Gate; the
default `schema="native"` output is unchanged.

The cross-test that validates column compatibility against real `divexplorer`
runs only when divexplorer is installed (`pip install divexplorer`); it is **not**
a pycatdap extra because it pulls scikit-learn / mlxtend / igraph (it would bloat
the dependency lock — see HISTORY H-0019 §B).
