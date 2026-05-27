# H-0005 Research: Continuous-Target Support in `target_summary` / `plot_target`

> **Status**: in-progress research — not yet a Proposal.
> **Tracks**: [Issue #56](https://github.com/nbx-liz/pycatdap/issues/56)
> **Outcome target**: HISTORY.md Proposal `H-0005` with `Decision` block based on the findings here.

This document is the working notebook for the research phase. It will be summarized into HISTORY.md once the algorithm choice is made.

---

## 1. Context (recap)

`pycatdap.target_summary` / `plot_target` (H-0004) currently raise `ValueError` for continuous targets. The original CATDAP framework (Sakamoto & Katsura, 1980) treats the response as categorical by design and provides no algorithm to discretize a continuous target. Extending to a continuous target therefore requires either (i) a Y-discretization rule beyond the 1980 paper, or (ii) **a different AIC formulation that does not bin Y at all**.

The candidates under evaluation:

| ID | Approach |
|---|---|
| (a) | **Symmetric pooling** — run `optimal_binning(Y, X)` per (Y, X) pair |
| (b) | **Joint AIC binning** — jointly optimize Y bins and X bins |
| (c) | **Marginal binning** — Sturges / Freedman-Diaconis / unsupervised MDL on Y alone |
| (d) | **Aggregate AIC** — bin Y once against the union of all candidate explanatories |
| (e) | **User-specified only** — require explicit `target_bins` |
| **(f)** | **Gaussian regression AIC** — Y stays continuous, X binned; AIC of piecewise-constant regression model. *Added 2026-05-27 after discovery of AdvancedCATDAP precedent.* |

---

## 2. Theoretical analysis of pycatdap's AIC formula

### 2.1 The exact formula

`_bin_aic` ([`_pooling.py:101-111`](../../src/pycatdap/_pooling.py)) computes, for a frequency table of shape `(C_E, C_F)`:

```
AIC(E; F) = -2 * Σ_ij n_ij * ln(n_ij / n_·j)  +  2 * (C_E - 1) * C_F
```

- **Conditional direction**: `n_ij / n_·j` is the MLE of `P(E = i | F = j)`. The model fitted is `P(response | bin)`, with the bin marginal `n_·j` treated as ancillary (one multinomial per column).
- **Penalty / DOF**: each of the `C_F` columns has `(C_E − 1)` free probabilities → total `(C_E − 1) · C_F` parameters; the penalty is `2k`.
- **Implicit null**: `compute_base_aic` ([`_aic.py:116-153`](../../src/pycatdap/_aic.py)) gives `AIC(E; φ) = −2 Σ n_E(i) ln(n_E(i)/n) + 2(C_E − 1)`.

### 2.2 Asymmetry of `_bin_aic`

Response side (`E`) is fixed and contributes only `C_E − 1` to the per-column DOF; bin side (`F`) contributes a *factor of `C_F`*. The likelihood treats the column marginal as conditioning, not as data — `_bin_aic` is **not invariant under transpose**.

Concrete 2×3 example confirms: same cells transposed give different log-likelihood (`−38.19` vs `−58.71`) and different penalty (`6` vs `8`).

### 2.3 Algebraic symmetry of `compute_delta_aic` (with caveats)

[`compute_delta_aic`](../../src/pycatdap/_aic.py) returns `AIC(E; F) − AIC(E; φ)`. Algebraic expansion gives:

```
ΔAIC = −2 · n · Î(E; F)  +  2 · (C_E − 1) · (C_F − 1)
```

where `Î(E; F)` is the plug-in mutual information. Mathematically both terms are symmetric in `E ↔ F`. **Once both axes are discretized, the numerical ΔAIC value is the same whether you call it (E given F) or (F given E)** — provided you correctly transpose the contingency table when swapping.

**Implementation caveat**: `compute_delta_aic(cross_freq, marginal_e, marginal_f, n)` has an asymmetric *interface*. The null model uses only `marginal_e` (`compute_base_aic(marginal_e, n)` at [`_aic.py:193`](../../src/pycatdap/_aic.py)), while the joint model uses `cross_freq` and `marginal_f`. To swap roles correctly at the call site, you must transpose `cross_freq` AND swap `marginal_e ↔ marginal_f`. Simply swapping the marginals without transposing produces wrong results.

**Net implication for H-0005**: the *final* score is direction-agnostic *after* discretization, so the only design choice that materially affects the value is **how each axis is binned**. Asymmetry of the formula lives entirely in the pooling step, not in the final score.

### 2.4 What candidate (a) symmetric pooling actually minimizes

Calling `optimal_binning(Y_cont, X_cat)` plugs `X` into `resp_codes` and `Y` into `bin_codes` → `_bin_aic` minimizes

```
−2 Σ n_ij ln(n_ij / n_·j_Y)  +  2 · (C_X − 1) · n_Y_bins
```

This is the AIC of `P(X | Y_bin)` vs `P(X)`. Pooling stops where adding a Y-cut costs more than `(C_X − 1)` bits of conditional log-likelihood. **The Y bins produced therefore depend on `C_X`**.

### 2.5 Cross-pair comparability of ΔAIC under (a) — definitive verdict: **NO**

If we run candidate (a) over multiple explanatories `X_1, ..., X_k`, the resulting `ΔAIC_i = −2n · Î(X_i; Y_binned_i) + 2(C_X_i − 1)(C_Y(i) − 1)` is **not directly comparable** because:

1. **Baseline mismatch** — `compute_delta_aic` compares against `AIC(X_i; φ)`. Each pair's null is "X_i independent of (the adaptively chosen Y partition for this pair)", which is not the same model across pairs.
2. **C_X-dependent granularity** — pooling stopping threshold scales linearly with `C_X_i`. A `C_X = 2` explanatory gets coarser Y bins than `C_X = 10` at the same `n · Î` level → systematic bias toward larger-`C_X` explanatories.
3. **Post-selection penalty** — `C_Y(i)` is *chosen to minimize* AIC, not held fixed. ΔAIC is the post-selection minimum → selective-inference bias of `C_X`-dependent magnitude.

**Two `X_i` with identical true `I(X; Y)` will produce different ΔAIC because pooling stops at different granularities and the penalty depends on the data-driven `C_Y(i)`.** Ranking by `ΔAIC` is invalid.

### 2.6 The principled fix is candidate (d)

The only path that preserves both "AIC-grounded" and "cross-pair comparable" is to **fix Y's discretization once** before the per-pair loop, then run `target_summary` with that frozen Y on each `X_i`. This guarantees:

- Every pair shares the same null `AIC(Y_binned; φ)`
- The `C_Y` penalty factor is constant
- Standard AIC comparability holds

Candidate (d) "aggregate AIC" achieves this with a discriminative criterion (bin Y to maximize total `Σ ΔAIC` over candidate explanatories). Candidate (c) achieves it with a non-discriminative criterion (Sturges / Freedman-Diaconis / unsupervised MDL on Y alone). Both restore comparability; (d) preserves more signal at the cost of coupling to the candidate set.

### 2.7 Partial salvage for (a) via normalization (NOT RECOMMENDED)

If per-pair Y binning is retained for some other reason, two normalizations partially restore comparability:

- **`ΔAIC / [2(C_X_i − 1)]`** — AIC-equivalent per-cut penalty rate
- **`Î(X_i; Y_binned_i)`** with held-out estimate — drops the AIC penalty entirely

Neither restores the strict Sakamoto-Katsura interpretation. Documented for completeness, but the recommended path is candidate (d).

---

## 3. Algorithm literature survey

### 3.1 Foundational supervised discretization (categorical class only)

| Method | Citation | Mechanism | Complexity |
|---|---|---|---|
| **MDLP** | Fayyad & Irani, *IJCAI-93*, 1022-1027 | Recursive binary splits; MDL gate `Gain > log₂(N-1)/N + Δ/N`. Used in C4.5. | O(N log N) |
| **Kononenko MDL** | Kononenko, *IJCAI-95*, 1034-1040 | MDLP machinery with multinomial-coding cost to remove multi-class bias | O(N log N) |
| **ChiMerge** | Kerber, *AAAI-92*, 123-128 | Bottom-up: merge adjacent bins with smallest χ² until threshold | O(N · K) |
| **CAIM** | Kurgan & Cios, *IEEE TKDE 16(2)*, 2004 | Top-down greedy maximizing class-attribute interdependence | O(N · K · M) |
| **CACC** | Tsai, Lee & Yang, *Information Sciences 178*, 2008 | Top-down using class-attribute contingency coefficient | O(N · K · M) |

**All five assume a categorical class / response.** None directly addresses binning a continuous *target* against a continuous explanatory.

### 3.2 Symmetric / joint discretization — confirmed literature gap

- **Joint 2-D histograms for MI estimation** (Ross 2014 PLOS ONE; R `entropy::discretize2d`) — bin (X, Y) jointly but use Sturges/equal-frequency, **not** optimized under AIC.
- **AIC for 1-D histogram density** (Hall 1990, *Probab. Theory Relat. Fields*) — single-variable density estimation, **not supervised, not joint**.
- **Optimal binning with continuous target** (Navas-Palencia 2020, arXiv:2001.08025) — MILP formulation that bins **only X**; Y stays raw and continuous.

**No published method jointly and symmetrically discretizes two continuous variables under AIC.** Candidates (a) symmetric pooling and (b) joint AIC binning would be **novel methodological contributions** requiring their own theoretical justification.

### 3.3 AIC-based discretization beyond CATDAP

- **Akaike 1973** — foundational AIC paper; says nothing about discretization specifically.
- **Solvang et al. 2024** (*Environmetrics*, doi:10.1002/env.2867) *(primary-source quote verification pending)* — secondary references describe the CATDAP workflow with the caveat: **"If the response is numerical, categorize the response by pooling, [reducing the problem] to the categorical response case."** This is reported as a published acknowledgment that the original framework requires the response to be pre-categorized but provides **no method** for doing so. The quoted wording needs primary-source confirmation before the H-0005 Proposal cites it as authoritative; the framework-level gap holds independently from this quote.
- **Hannig & Bickel on contingency-table AIC** — *(citation needed)*; closest verified work is Tarumi et al. 2024 (PMC11754365) but it concerns hypothesis-restricted log-linear models, not binning.

### 3.4 Per-candidate published-basis check

| Candidate | Published precedent? | Theoretical foundation |
|---|---|---|
| (a) Symmetric pooling | **No.** Novel contribution | Borrows pycatdap pooling machinery in unintended direction |
| (b) Joint AIC binning | **No.** Novel contribution | Closest: Navas-Palencia 2020 MILP, but binds only X |
| (c) Marginal binning | **Yes.** Sturges 1926, Freedman-Diaconis 1981, Hall 1990 (AIC histograms), Rissanen MDL | Well-grounded — but loses CATDAP's "AIC-driven" selling point |
| (d) Aggregate AIC | **No.** Conceptually close to multi-criterion discretization but no standard precedent | Novel; sum-of-ΔAIC objective has no rigorous IT justification |
| (e) User-specified | **Yes.** Standard practice for ordinal recoding | No discretization theory required |

### 3.5 What the literature recommends

The published record supports **(c) as a safe default** (well-grounded, comparable ΔAIC, single global Y partition) and **(e) as an explicit power-user override**. (a), (b), (d) are intellectually appealing but would require their own theoretical work to justify — should ship as experimental opt-in flags with explicit "ΔAIC may not be comparable" warnings if at all.

**However**, §3.6 below introduces candidate (f), which superseded the (a)-(e) framing entirely.

### 3.6 Prior art in the same problem domain — `AdvancedCATDAP`

The sibling repository [`nbx-liz/AdvancedCATDAP`](https://github.com/nbx-liz/AdvancedCATDAP) (private) is an AIC-based automated feature engineering library that **already supports regression (continuous target) tasks**. Reading its source resolves the H-0005 design question with a single insight:

> **Don't bin Y. Use the Gaussian regression AIC instead.**

#### The AdvancedCATDAP regression AIC formula

For a continuous target `y` and a binned explanatory `X` (`k` bins, `n_i` observations per bin), the AIC is:

```
AIC_reg = n · ln(RSS / n)  +  2 · k

where  RSS = Σ_i Σ_{j in bin i} (y_j − ȳ_i)²    (within-bin sum of squares)
       k   = (#non-empty bins) + 1               (the +1 is the variance parameter)
```

Implementation: [`advanced_catdap/components/scoring.py:Scorer.calc_score_reg_bincount_idx`](https://github.com/nbx-liz/AdvancedCATDAP/blob/main/advanced_catdap/components/scoring.py). For each X bin, it computes the within-bin RSS using `np.bincount(indices, weights=target)` and `np.bincount(indices, weights=target ** 2)` — vectorized and O(N).

The null model is `y = constant (mean)`:
```
AIC_null = n · ln(TSS / n)  +  2 · 2     where TSS = Σ (y_j − ȳ)²
```

ΔAIC = `n · ln(RSS / TSS)  +  2 · (k − 2)` = **`n · ln(1 − R²) + 2 · (k − 2)`**.

This is **textbook Gaussian-AIC for piecewise-constant regression**.

#### Why this is the right answer for H-0005

1. **No novel methodology** — AIC for piecewise-constant regression is standard (e.g., Yao 1988 changepoint regression; Davis, Lee & Rodriguez-Yam 2006 *Structural Break Estimation for Nonstationary Time Series Models* (JASA), MARS in Friedman 1991, etc.).
2. **Cross-pair comparability is automatic** — the null model AIC depends only on `Y`'s marginal, not on `X`. Every `ΔAIC(Y, X_i)` is computed against the same `AIC_null`. No post-selection bias because Y is never partitioned.
3. **Y stays continuous** — no information loss from discretization, no `target_bins` parameter, no user choice that distorts rankings.
4. **It already works in a sibling pycatdap-family library** — `AdvancedCATDAP` ships this in production. We have a reference implementation.
5. **Per-bin output is a `Target_Mean` table**, not a contingency table — [`discretizer.py:get_feature_details:660-750`](https://github.com/nbx-liz/AdvancedCATDAP/blob/main/advanced_catdap/components/discretizer.py) returns `{Feature, Bin_Idx, Bin_Label, Count, Target_Mean}` per X bin for regression mode. This is the natural analog of pycatdap's `col_prop` for the regression case.

#### Implication: candidate (f) supersedes candidates (a)–(e)

Candidates (a)-(e) all assumed the problem was "how to discretize Y." That framing was wrong. The actual problem is "how to extend AIC to a continuous response," and Gaussian regression AIC solves it directly. Y discretization (candidate c/d/e) is at best a *fallback* for users who specifically need a contingency-table view.

#### Caveat: API return shape differs

`AdvancedCATDAP`'s regression mode returns per-bin `{Count, Target_Mean}` — NOT a `(C_E × C_F)` contingency table with `row_prop`, `col_prop`, `pearson_residuals`. Those categorical-table fields don't generalize to a continuous response. The pycatdap `TargetSummary` will need either:

- **Two-mode return**: `TargetSummary` for categorical target (existing 4 tables + ΔAIC), `TargetSummaryRegression` for continuous target (per-bin `{count, target_mean, target_std}` + ΔAIC), OR
- **Polymorphic single class**: `TargetSummary` with `mode: Literal["classification", "regression"]` and conditional fields (some `pd.DataFrame`s become `pd.Series` in regression mode, some are `None`).

The two-mode design is cleaner and more honest about what the regression view is — see §7.

---

## 4. Competitor tool survey

Surveyed 5 major EDA / error-analysis / drift tools for their continuous-target handling.

### 4.1 Per-tool findings

| Tool | Continuous-target approach | Discretization | Statistic |
|---|---|---|---|
| **ydata-profiling** | Target treated as one variable in the correlation matrix; user picks the row | None (numeric-numeric); Cramér's V on discretized numeric for mixed | Pearson / Spearman / Kendall + Phi_k / Cramér's V |
| **MS RAI — Error Analysis** | Analyzes `y_pred − y_true` (error signal), not the raw target | LightGBM surrogate (depth-limited) splits continuous features on error | MAE / MSE / R² per cohort |
| **Evidently AI** | Plots feature vs. target, reports correlation; KS test for target drift | None | **Pearson** correlation per feature |
| **Manifold (Uber)** | Segments instances by per-instance squared error via k-Means | No target binning; compares feature distributions between high/low-error segments | **KL divergence** between segment-conditional feature distributions |
| **Sweetviz** | Supports boolean and numeric targets | None | Pearson (num-num); **correlation ratio η** (cat-num) |

### 4.2 Two emerging paradigms

The survey reveals two structurally different ways to analyze "continuous target × feature":

**Paradigm A: Discretize the target → use categorical-style statistics**
- No mainstream tool does this. **A pycatdap H-0005 implementation would be the unique entry.**
- Closest precedent: ydata-profiling's Cramér's V path, but it discretizes the *feature*, not the target.

**Paradigm B: Use residuals / error as the signal → segment instances by error**
- Manifold (KL across high/low-error segments), RAI Error Analysis (LightGBM on errors), Evidently (regression performance per slice).
- This is structurally what pycatdap's planned **Phase J `error.residual_by_category`** ([Issue #18](https://github.com/nbx-liz/pycatdap/issues/18)) intends.

### 4.3 Implication for H-0005 scope

These paradigms answer **different questions**:

- **A**: "Which features explain *the target itself* (e.g., raw residual magnitude treated as the response)?"
- **B**: "Where in feature space does the model fail (cohort-level error analysis)?"

H-0005 should focus on **paradigm A** (extending `target_summary` to a continuous response). **Phase J / Issue #18 remains valuable** for paradigm B, not redundant with H-0005. They are siblings, not duplicates.

### 4.4 Comparability across competitors

- **Manifold (KL)**: single scalar per feature, fully cross-feature comparable. Structurally closest to CATDAP's "rank by ΔAIC" intent — except using residual segments, not direct target.
- **Evidently (Pearson)**: comparable for numeric features only; breaks down across dtypes.
- **Sweetviz**: Pearson vs. correlation ratio mixes scales — loose ranking.
- **ydata-profiling**: matrix view, no single ranking.
- **RAI**: per-cohort metric, ranks cohorts not features per se.

**Lesson for H-0005**: aim for **a single ΔAIC per feature, dtype-agnostic, AIC-grounded** — would dominate the field. Candidate (d) gives this; candidate (a) does not (see §2.5).

---

## 5. Formal requirements

For the chosen algorithm to be usable in pycatdap's `target_summary` / `plot_target` (and downstream Phase J residual analysis), it must satisfy:

### R-1: Cross-pair comparability **(critical)**

When ranking explanatories `X_1, X_2, ..., X_k` against a continuous target `Y`, the resulting `delta_aic(Y, X_i)` values must be **directly comparable** across pairs. A bigger `|delta_aic|` should mean "more informative" regardless of `X_i`'s dtype or cardinality.

A symmetric-pooling candidate where each `(Y, X_i)` pair produces a different Y binning **fails this requirement by default** — the implicit "null baseline" shifts per pair. Mitigation requires either a fixed Y binning across all pairs, or an explicit normalization (e.g., divide by entropy `H(Y)` or by `N`).

### R-2: Reproducibility

Given the same `(df, target, explanatory, target_bins)` arguments, the output must be deterministic. No randomized initialization without a seed.

### R-3: Documentable theoretical foundation

Either:
- (i) cites a published method with the same semantics, or
- (ii) explicitly states that the method is a pycatdap-original extension of CATDAP, with the assumptions made spelled out

This is required for academic credibility and for users who want to compare against R `catdap`. "Symmetric pooling," for example, has no published precedent — fine, but the documentation must say so.

### R-4: Computational complexity ≤ O(N · K log K)

The Phase J residual analysis use case implies repeated calls (one per explanatory, often dozens). Joint optimization candidates (b) that scale `O(K^2 · N^2)` are prohibitive on N > 10k.

### R-5: Robustness to outliers and heavy tails

Continuous targets in error-analysis contexts are typically residuals — heavy-tailed, possibly skewed. A method that places bin boundaries strictly at quantiles or at the data extremes (rather than at AIC-optimal cut points) handles tails gracefully.

### R-6: No mutation of user data

Required by pycatdap's general invariants. Binning must operate on a copy.

### R-7: Backward compatible with existing `target_summary`

- Categorical / boolean target: unchanged behavior.
- Continuous target: a new opt-in parameter `target_bins=...` enables the support.
- `bins=None` for continuous target should either default to a sensible auto-discretization OR raise a clear error pointing the user at `target_bins`.

### R-8: Honest reporting of binning artefacts

The returned `TargetSummary` must expose the actual Y bin boundaries (analogous to the existing `intervals` for the explanatory). A new field `target_intervals: list[float] | None` is the minimum.

---

## 6. Candidate scorecard

Synthesizing §2 (formula analysis), §3 (literature), §4 (competitors), and §5 (requirements):

| Candidate | R-1 Comparability | R-2 Repro | R-3 Theory | R-4 Compute | R-5 Robust | R-7 BC | Verdict |
|---|---|---|---|---|---|---|---|
| **(a) Symmetric pooling** | **✗ no** (§2.5: C_X-dependent granularity + post-selection bias) | ✓ | ✗ no precedent | ✓ O(N · K) | depends on data | ✓ | **reject** |
| **(b) Joint AIC** | ✗ no (per-pair Y bins) | ✓ | ✗ no precedent | ✗ O(K² · N²) | depends | ✓ | **reject** (compute infeasible) |
| **(c) Marginal binning** | ✓ yes (global Y partition) | ✓ | ✓ strong: Sturges, FD, Hall 1990, Rissanen | ✓ O(N log N) | ✓ quantile/FD robust | ✓ | **fallback** for contingency-table view |
| **(d) Aggregate AIC** | ✓ yes (global Y partition) | ✓ | ✗ novel; sum-ΔAIC not IT-grounded | ⚠ O(N · K · J) per refresh | depends | ✓ | **reject** (no longer needed given (f)) |
| **(e) User-specified** | ✓ yes | ✓ | ✓ standard practice | ✓ O(N) | ✓ (user choice) | ✓ | **accept** as override |
| **(f) Gaussian regression AIC** | **✓ yes** (shared `AIC_null` from Y marginal) | ✓ | **✓ strong**: textbook Gaussian-AIC, Yao 1988, Davis-Lee-RY 2006; **already in production** in `AdvancedCATDAP` | ✓ O(N · K) | ✓ (Y not partitioned → no boundary artefacts) | ✓ | **accept as primary**: supersedes (a)–(d) |

### Key findings driving the scorecard

1. **(f) is the answer.** Discovering AdvancedCATDAP's regression mode resolves H-0005: don't bin Y, use Gaussian regression AIC. The original (a)-(e) framing of "how to discretize Y" was a false premise. (f) is theoretically textbook, computationally light, has cross-pair comparability built into the null model, and is already in production in a sibling library.

2. **R-1 makes or breaks (a) and (b).** Per-pair Y binning introduces a C_X-dependent post-selection bias (§2.5) that invalidates ranking. No salvage via normalization preserves the strict AIC interpretation. **Both rejected.**

3. **(c) survives as a fallback.** If a user specifically needs a `(C_E × C_F)` contingency-table view (counts, row_prop, col_prop, pearson_residuals) for a continuous target, the only way to provide it is by binning Y first. (c) does this with published basis. But this is a **secondary** use case — the primary path is (f).

4. **(d) is no longer needed.** It was the "AIC-optimal Y binning" experimental path. (f) provides AIC-grounded ranking without binning Y at all — (d)'s motivation disappears.

5. **(e) remains the escape hatch.** Domain experts often *already know* the right binning (e.g., quartiles of |residual|, signed error sign, calibration deciles). Allow them to opt into the (c)-style contingency view.

---

## 7. Recommendation for H-0005 Proposal *(REVISED 2026-05-27)*

> **Major revision**: After §3.6 (AdvancedCATDAP review), the recommendation pivots from candidate (c) to **candidate (f) Gaussian regression AIC** as the primary path. Y is no longer discretized in the default workflow. (c) survives only as an explicit fallback when the user requests a contingency-table view.

### 7.1 Primary path — candidate (f) Gaussian regression AIC

For a continuous target, `target_summary` returns a **regression-mode result** containing per-X-bin `{count, target_mean, target_std}` and a Gaussian ΔAIC (no `target_bins` parameter; Y is not partitioned):

```python
target_summary(df, target, explanatory, *, bins=None) -> TargetSummary
```

Internally the function dispatches on `target` dtype:

- **Categorical / boolean target**: existing H-0004 logic — returns full contingency tables (counts / row_prop / col_prop / expected / pearson_residuals) + multinomial ΔAIC.
- **Continuous target**: **new logic** — bins `X` per existing `optimal_binning` (or user `bins`), then computes Gaussian regression AIC `n · ln(RSS/n) + 2k` against the null `n · ln(TSS/n) + 4`. Returns per-bin `{count, target_mean, target_std}` and ΔAIC. The contingency-table fields become `None` (or are absent in a `RegressionTargetSummary` variant).

The choice between **two-class hierarchy** and **polymorphic single class** is an API-design decision:

- **Option A (two-class)**: `TargetSummary` (categorical) and `RegressionTargetSummary` (continuous), both with `.show / .to_html / .to_dict / .to_plotly_json`. Types tell the user which mode they're in.
- **Option B (single class with mode discriminant)**: `TargetSummary(mode: Literal["classification", "regression"], ...)` with conditional fields.

Recommend **Option A** — clearer types, less Optional-field handling, matches `AdvancedCATDAP`'s pattern of returning different feature_details schemas for each task type. Defer to the Proposal stage for final naming.

### 7.2 Fallback path — candidate (c) `target_bins=` opt-in

For users who specifically need a `(C_E × C_F)` contingency table view on a continuous target (e.g., calibration analysis with quartiles of predicted probability), expose:

```python
target_summary(df, target, explanatory, *, bins=None, target_bins=None)
```

Where `target_bins` accepts `int | Sequence[float] | "quantile" | "equal_width" | "fd" | None`. The semantics:

- `target_bins=None` AND target categorical → existing behavior.
- `target_bins=None` AND target continuous → **regression mode** (candidate (f), per §7.1).
- `target_bins=<not None>` AND target continuous → **forced contingency-table mode** with explicit Y binning (candidate (c) / (e)).
- `target_bins=<not None>` AND target categorical → **error or warning** — Y is already discrete.

This satisfies both use cases without one polluting the other.

### 7.3 What we do NOT ship

- **(a) symmetric pooling** — fails R-1 (§2.5)
- **(b) joint AIC** — fails R-1 and R-4
- **(d) aggregate AIC** — superseded by (f); no longer motivated
- "Magic" continuous-target support without dispatching on dtype — would conflate two semantically different outputs

### 7.4 Prototype + benchmark plan (next phase, separate Issue)

1. **Port the Gaussian regression AIC** from `AdvancedCATDAP/scoring.py:calc_score_reg_bincount_idx` into pycatdap's `_aic.py` (or a new `_aic_regression.py`). Implementation is ~20 LOC using `np.bincount` with weights — vectorized and O(N) per pair.
2. **Decide on Option A vs Option B** for the return type (per §7.1).
3. **Benchmark on**:
   - **Synthetic**: known feature importance (3 informative, 5 noise); check ranking accuracy of Gaussian ΔAIC against ground truth.
   - **California Housing**: regression target, exercise on cleaned features.
   - **Titanic-as-regression**: `Fare` as continuous target.
4. **Sanity checks**:
   - When the explanatory is constant, ΔAIC ≥ 0 (penalized null beats over-parameterized model).
   - When the explanatory is a perfect predictor (RSS → 0), ΔAIC → −∞ (clipped at `n · ln(EPSILON_RSS / n)`).
   - The R² implicit in ΔAIC (`1 − exp((ΔAIC − 2(k−2)) / n)`) recovers `sklearn.metrics.r2_score` on the same X-binning.

### 7.5 Relationship to Phase J (Issue #18)

§4 found H-0005 and Phase J answer different questions (paradigm A: discretize target / paradigm B: residual segmentation). With (f) as the primary path, the H-0005 / Phase J relationship is even cleaner:

- **H-0005 (f)**: AIC-grounded ranking of features against a continuous response. Applies to raw target, residuals (when treated as the target), calibration scores.
- **Phase J `residual_*`**: model-error diagnostics with `(y_true, y_pred)` inputs — confusion-matrix-style for classification, residual plots for regression.

`residual_by_category` in Phase J becomes: compute `_resid = y_pred - y_true`, then call `target_summary(df_aug, "_resid", var)` which dispatches to regression mode via (f). The API mismatch noted in cross-check still requires Phase J to do the residual computation + defensive copy, but the **statistic** is the (f) Gaussian regression AIC throughout.

---

## 10. Detailed theoretical analysis of candidate (f) Gaussian regression AIC

> Added after the user requested rigorous theoretical scrutiny of (f). All claims numerically verified on synthetic data; verdict subject to independent cross-check (§11).

### 10.1 Derivation from the Gaussian log-likelihood

Model: `y_j = ȳ_{bin(j)} + ε_j` with `ε_j ~ N(0, σ²)` iid (shared variance across bins).

The log-likelihood at the MLE `(ȳ̂_i, σ̂²)` is:

```
ℓ(θ̂) = -n/2 · log(2π) − n/2 · log(σ̂²) − n/2

where  σ̂² = RSS / n
       RSS = Σ_i Σ_{j∈bin i} (y_j − ȳ̂_i)²    (within-bin residual sum)
```

Substituting and applying AIC = -2ℓ + 2k:

```
AIC_full = n · log(2π) + n · log(RSS/n) + n + 2k
```

Drop the model-independent constant `n · log(2π) + n` (it cancels in ΔAIC) → **AdvancedCATDAP form**:

```
AIC' = n · log(RSS/n) + 2k
```

Numerical confirmation: AdvancedCATDAP form's `delta_aic` matches full Gaussian form's `delta_aic` to floating-point precision (`5.33e-14`).

### 10.2 Parameter count

The model has:
- `k_means` parameters: one mean per non-empty bin
- `1` parameter: shared variance σ²

Total: `k = k_means + 1`. This matches `calc_score_reg_bincount_idx` line 39:
```python
k = np.count_nonzero(valid_mask) + 1  # +1 for variance param
```

For the null model: `k_null = 2` (global mean + variance). ✓ matches AdvancedCATDAP `task_detector.py:65-66`.

### 10.3 Cross-pair comparability (R-1) — proof, and the missing-data confounder

For a fixed Y and J candidate explanatories `X_1, ..., X_J` with X-bin partitions, **assuming a common observation set across all pairs**:

```
AIC_i      = n · log(RSS_i / n)  +  2 · (k_i_means + 1)
AIC_null   = n · log(TSS / n)    +  2 · 2
ΔAIC_i     = AIC_i − AIC_null
           = n · log(RSS_i / TSS)  +  2 · (k_i_means − 1)
           = n · log(1 − R²_i)    +  2 · (k_i_means − 1)
```

Under the common-observation-set assumption, three properties hold:

1. **Shared null model**. `AIC_null` depends only on `(n, TSS)`, both functions of Y — identical for every X candidate.
2. **No post-selection on Y**. Y is never partitioned, so there is no `C_Y(i)` chosen to minimize AIC; the penalty `2 · (k_i_means − 1)` depends only on `X_i`'s partition.
3. **Scale stability**. `n · log(1 − R²)` is bounded above by 0; explanatories with stronger explanatory power produce more-negative ΔAIC monotonically.

**Critical confounder identified by cross-check (2026-05-27)**: the common-observation-set assumption **does NOT hold under pycatdap's current `_target_pair.py:328` design**:

```python
work = df[[target, explanatory]].dropna()    # per-pair drop
```

Each `(Y, X_i)` pair drops rows missing either Y or X_i. If `X_1` has 200 missing rows and `X_2` has 50, the effective `n_1 ≠ n_2` → `AIC_null` differs per pair → ranking is corrupted. Numerical demo: same Y, `n=800` vs `n=950` gives `AIC_null = 1106.23 vs 1368.58` — a 262-unit drift that swamps real signal.

**Design implication for H-0005**: the Proposal must commit to one of the following strategies, and document the choice:

| Strategy | Effect | Trade-off |
|---|---|---|
| **(M1) Complete-case across the whole candidate set** | Drop rows missing in *any* X candidate before evaluating any pair. Same n for all i. | Aggressive data loss when many candidates have missing values; the candidate set must be known up-front. |
| **(M2) Y-only dropna; tolerate per-bin missing** | Drop only rows missing Y. For each X candidate, an "is_missing" pseudo-bin captures the rest. Same n for all i. | Adds a "missing" bin to every X, which inflates `k_i_means` by 1 when missing-rate is positive. Pearson-residuals-style interpretation of the missing bin requires careful documentation. |
| **(M3) Per-pair dropna + report n_effective; warn user** | Existing behavior. `TargetSummary` carries `n_effective`; users must check it before cross-pair ranking. | Comparability is the user's responsibility; the API silently violates R-1 by default. |

**Recommended for H-0005**: **(M2) Y-only dropna with explicit missing pseudo-bin**, mirroring how `_aic.py` partial-statistics functions (`calc_score_regression_partial` in AdvancedCATDAP) already handle missing data on X. This preserves data, keeps n constant across pairs, and exposes missingness as a first-class signal. Strategy must be a stated Acceptance Criterion in the H-0005 Proposal.

### 10.4 Consistency with the Sakamoto-Katsura framework

The categorical CATDAP framework uses **multinomial-product log-likelihood**:
```
AIC_cat = -2 · Σ_ij n_ij · log(n_ij / n_·j) + 2 · (C_E − 1) · C_F
```

The continuous extension uses **Gaussian log-likelihood with shared σ²**:
```
AIC_gauss = n · log(RSS/n) + 2 · (k_means + 1)
```

Both:
- Are derived from `AIC = -2·log-likelihood + 2·parameter_count`
- Compare a structured model against an independence/null baseline via `ΔAIC`
- Rank explanatories by `|ΔAIC|` after penalty
- Apply post-selection on X (CATDAP-02's pooling AIC-optimizes X bins; same post-selection structure as the proposed Gaussian path)

This is a **likelihood-family extension** (multinomial → Gaussian), analogous to GLMs generalizing from logistic to Gaussian. **It does not violate the AIC philosophy of pycatdap**; it generalizes the response-side likelihood while preserving the explanatory-side machinery.

### 10.5 Edge cases and numerical guards

| Edge case | Behavior in AdvancedCATDAP | Verified |
|---|---|---|
| `n ≤ k + 1` | Returns `float('inf')` (`scoring.py:18`) | ✓ AICc would diverge at `n - k - 1 ≤ 0`; non-AICc AIC is finite via `EPSILON_RSS` clip but unreliable |
| Perfect predictor (RSS → 0) | `rss = max(rss, EPSILON_RSS)`, AIC → very negative but bounded | ✓ Numerical check [4]: n=50, k=51, AIC=-1244.89 — bounded |
| Empty bins | `valid_mask = counts > 0` excludes them from `k_means` | ✓ Code line 38: `k = np.count_nonzero(valid_mask) + 1` |
| Constant X (1 bin) | `k_means = 1`, model = null model | ✓ Numerical check [3]: ΔAIC = 0 exactly |

### 10.6 Known limitations

| Limitation | Severity | Mitigation |
|---|---|---|
| **Gaussian assumption misspecified for heavy-tailed Y** (e.g., income, prices, log-normal) | Moderate. ΔAIC is still a valid *ranking* statistic under misspecification (Sin & White 1996; White 1982 quasi-MLE theory), but the absolute interpretation as "model probability" weakens. | Document. Optionally support log-transform of Y as a preprocessing step. |
| **Shared-variance assumption (homoscedasticity)** | Moderate. Heteroscedasticity is not detected by AIC under shared-σ² model; an X that shifts variance but not mean appears uninformative. Cross-check verification with multiple seeds and splits found this is **effectively a complete blind spot under equal partitions**, with only artefactual noise contaminating unequal-partition results. | Document. Note that pycatdap-cat is also blind to variance under contingency models; this is parity. If variance-detection becomes a use case, extend to a heteroscedastic Gaussian likelihood (separate Proposal). |
| **AIC over-selects K in piecewise-constant regression** (Cherkassky & Mulier 2007; Yao 1988 *Estimating the Number of Change-Points via Schwarz Criterion*). | Low—Moderate. AIC tends to choose too many bins. Yao 1988 specifically recommends **BIC** (Schwarz criterion) as the remedy, not AICc. AICc (Hurvich-Tsai 1989) was derived for continuous-X autoregressive Gaussian models; its theoretical support for piecewise-constant changepoint settings is weaker. | Expose `criterion="aic" \| "aicc" \| "bic"` and default to **`"bic"`** (matches Yao 1988's recommendation for the changepoint structure most similar to our setting). Document the distinction explicitly. |
| **Post-selection inference on X** | Low. Same problem categorical CATDAP-02 already has and accepts. | No additional mitigation needed. |
| **Reverse problem (ΔAIC scale differs from categorical mode)** | Low. ΔAIC=−250 in categorical mode and ΔAIC=−250 in regression mode are NOT directly comparable — they live in different likelihood families. | Document. Add a section to BLUEPRINT.md §5.7. Users running mixed-target studies must compare within-mode only. |

### 10.7 Numerical verification summary

Synthetic checks (`uv run python` script, see git log for full output):

| Check | Result | Implication |
|---|---|---|
| Formula vs manual RSS / AIC | match to `5.7e-14` | Implementation correct |
| AdvancedCATDAP form vs full Gaussian AIC | ΔAIC match to `5.3e-14` | Constant-cancellation is rigorous |
| AIC_null invariance across X_1, X_2, X_3 | exact same value (37.0108) | R-1 cross-pair comparability holds in code |
| informative > noise > constant ranking | ΔAIC = -2253 << +1.35 < 0 | Correct directional behavior |
| AICc-style correction at n=30, k=6 | matches `2k(k+1)/(n-k-1) = 3.6522` exactly | AdvancedCATDAP's internal AICc formula is self-consistent. **Caveat**: this uses `k = k_means + 1` (variance counted as a parameter), whereas strict Hurvich-Tsai 1989 uses `K = k_means` (variance ancillary). Difference at this n: 3.65 vs 2.50. AdvancedCATDAP's convention is internally consistent but the citation to Hurvich-Tsai should be qualified. |
| Edge: per-row bins, n=50, k=51 | non-AICc AIC finite (bounded by EPSILON_RSS); AICc diverges | Edge guards work; AICc requires `n > k+1` |
| Variance-only shift | ΔAIC = -3.12 on N=1000, seed=42, 75/25 split, σ ∈ {0.5, 2.0} | **Not reproducible across seeds / splits.** At 50/50 equal split, ΔAIC was +1.55 (null beats model); at seed=5, -8.06; at seed=0, +0.41. The "-3.12" value is artefactual from unequal-split-induced sampling drift in the within-bin means, not a stable variance-detection signal. **Corrected interpretation**: Gaussian AIC is effectively blind to pure variance shifts under equal partitions; unequal-partition artefacts contaminate any apparent signal. Documented limit. Tests should NOT use this value as a baseline. |

**Verdict from theoretical analysis alone (PRE-cross-check)**: candidate (f) is theoretically sound with documented Gaussian / homoscedasticity assumptions. Verified against AdvancedCATDAP's production implementation. The cross-check (§11) refined the verdict — see below.

---

## 11. Third-party verification — cross-check-reviewer verdict (2026-05-27)

Independent agent verified the 7 claims in §10 against the AdvancedCATDAP source code and the pycatdap implementation. The Chain holds **partially**. Direction (adopt (f)) is unchanged; **three implementation-spec corrections required** before the H-0005 Proposal.

### Per-claim verdicts

| Claim | Verdict | Action taken |
|---|---|---|
| **A** Derivation correctness (§10.1) | TRUE | None needed |
| **B** Parameter count `k = k_means + 1` (§10.2) | PARTIALLY-TRUE | §10.7 caveat added: AdvancedCATDAP's K-count includes variance; strict Hurvich-Tsai uses K = k_means. Internally consistent but citation tightened. |
| **C** Cross-pair comparability (§10.3) | **PARTIALLY-TRUE** — **critical confounder** | §10.3 rewritten: shared-`AIC_null` assumes a common observation set, which fails under current `_target_pair.py:328` per-pair dropna. Three mitigation strategies (M1/M2/M3) added; **M2 (Y-only dropna + missing pseudo-bin) recommended for H-0005**. |
| **D** Variance-shift "moderate severity" (§10.6) | PARTIALLY-TRUE | §10.6 rewritten: heteroscedasticity blind-spot is effectively complete under equal partitions; non-zero ΔAIC at unequal splits is artefactual. |
| **E** AIC over-selects bins → AICc default (§10.6) | PARTIALLY-TRUE | §10.6 rewritten: Yao 1988 actually recommends **BIC** (Schwarz), not AICc. Default changed from AICc to BIC; `criterion="aic" \| "aicc" \| "bic"` exposed. |
| **F** GLM analogy / IT-interpretation parity (§10.4) | UNCERTAIN | The Gaussian `n·log(1−R²)` does NOT have the same information-theoretic mutual-information interpretation as the categorical `−2n·Î(E;F)` form. The two paths are AIC-aligned but not IT-aligned. To be noted in H-0005 Proposal under "Alternatives Considered." |
| **G** Numerical verification reproducibility (§10.7) | PARTIALLY-TRUE | §10.7 table updated to flag the variance-shift result as non-reproducible (split- and seed-dependent). |

### Final verdict — what changes in the H-0005 Proposal

1. **Adopt candidate (f) Gaussian regression AIC as primary path** — direction unchanged.
2. **Specify missing-value handling explicitly** (Strategy M2, Y-only dropna with missing pseudo-bin). This is an Acceptance Criterion. Without it, R-1 is silently violated.
3. **Default `criterion="bic"`** (Yao 1988 recommendation for changepoint structure), with `aic` / `aicc` as user-selectable alternatives.
4. **Cite Hurvich-Tsai 1989 carefully** — note that the K-count convention varies (AdvancedCATDAP includes σ² in K; strict Hurvich-Tsai does not). pycatdap will document the convention used.
5. **Remove the variance-shift "ΔAIC ≈ -3 on N=1000" claim** from any docs; replace with "effectively blind under equal partitions; unequal-partition results are artefactual."
6. **Document the IT-interpretation gap** (categorical mode = mutual-information ranking; regression mode = R²-based ranking) in BLUEPRINT.md and the Proposal's "Alternatives Considered."

The Chain holds for the **direction**; the spec needs the corrections above. No deal-breakers were identified — Gaussian regression AIC is theoretically sound and AdvancedCATDAP-tested. The H-0005 Proposal can be drafted on this foundation.

---

## 8. Out-of-scope reminders

Tracked in the Issue #56 "Out of scope" section. Not addressed here:

- Implementation (deferred until after H-0005 Proposal is accepted)
- Phase J reorganization (re-evaluated after algorithm choice)
- Continuous-continuous explanatory (`bins` + `target_bins` simultaneously)
- `plot_target` dispatch updates for continuous-target plot kinds

---

## 9. Change log

- `2026-05-27` — Initial scaffold created; three parallel research tracks launched (literature, competitors, formula analysis).
- `2026-05-27` — All three tracks merged. §2 formula analysis: candidate (a) symmetric pooling fails cross-pair comparability (R-1) due to C_X-dependent post-selection bias. §3 literature: candidate (c) marginal binning has strong published basis (Sturges, FD, Hall 1990 AIC histograms); (a), (b), (d) have no precedent; Solvang et al. 2024 (Environmetrics) reportedly confirms the framework-level gap. §4 competitors: no mainstream tool quantile-bins continuous target for categorical-style analysis; Manifold and MS RAI use residual-based segmentation (paradigm B, complementary to H-0005). **Recommendation: (c) marginal binning with explicit `target_bins ∈ {int, list, "quantile", "equal_width", "fd"}`; (d) deferred to experimental opt-in; (a), (b) rejected.**
- `2026-05-27` — Independent cross-check (cross-check-reviewer agent). Verdicts on 4 key claims: (1) algebraic ΔAIC symmetry PARTIALLY-TRUE — held algebraically, but `compute_delta_aic` interface is asymmetric and the doc wording "direction-agnostic" was tightened to clarify the transpose-and-swap requirement; (2) candidate (a) failure-of-R-1 TRUE — all three sub-claims verified against [_pooling.py:101-111](../../src/pycatdap/_pooling.py), [_pooling.py:285-291](../../src/pycatdap/_pooling.py); (3) Solvang 2024 quote UNCERTAIN — marked `(primary-source quote verification pending)` in §3.3; the framework-level gap holds independently; (4) "Phase J residual_by_category as thin wrapper" PARTIALLY-TRUE — rewritten in §7.5 to acknowledge the signature mismatch and immutable-data constraint; integration shape deferred to Phase J implementation. **Direction unchanged at that point**; precision improved.
- `2026-05-27` — **Major revision**: discovered `nbx-liz/AdvancedCATDAP` (sibling private library) already implements continuous-target support via **Gaussian regression AIC** (`n · ln(RSS/n) + 2k`) with no Y discretization. This is candidate (f), added retroactively. (f) supersedes the original recommendation: it has stronger theoretical basis (textbook Gaussian-AIC; Yao 1988, Davis et al 2006), is already in production, is cross-pair comparable by construction (shared null), and avoids the entire "how to discretize Y" debate. **Recommendation revised**: (f) Gaussian regression AIC as **primary**; (c) marginal binning retained as **opt-in fallback** for users wanting a contingency-table view; (a), (b), (d) **rejected**; (e) user-specified bins available as alias for (c). API return type splits: existing `TargetSummary` for categorical, new `RegressionTargetSummary` for continuous. The original recommendation (c-as-default) was based on the false premise that Y must be discretized — false because Gaussian AIC is well-defined on continuous Y.
- `2026-05-27` — **Theoretical scrutiny + cross-check**: detailed analysis added in §10 (derivation, parameter count, cross-pair comparability proof, edge cases, known limitations, numerical verification). Cross-check-reviewer agent verified 7 claims; chain holds **partially**, direction unchanged, three implementation-spec corrections required: (i) **missing-value handling** — current `_target_pair.py:328` per-pair dropna silently violates R-1 by varying `n` across pairs; spec must adopt strategy M2 (Y-only dropna + missing pseudo-bin); (ii) **default criterion** — Yao 1988 recommends BIC for changepoint structures; default changed from AICc to BIC, with AIC/AICc as user-selectable alternatives; (iii) **citations tightened** — AdvancedCATDAP's K-count includes σ² (differs from strict Hurvich-Tsai 1989); variance-shift numerical result was non-reproducible and is now flagged. **No deal-breakers**; (f) Gaussian regression AIC remains adopted as primary path with the three corrections above. The H-0005 Proposal can be drafted on this foundation.
