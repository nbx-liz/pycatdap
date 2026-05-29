# Tutorials

Learning-oriented walkthroughs that guide you from zero to confident usage.

## Available

- **[Basic CATDAP](01-basic-catdap.ipynb)** — The original v0.2 tutorial walkthrough using HealthData
- **[EDA on Titanic](02-eda-titanic.ipynb)** — v0.3+ univariate EDA APIs (`describe`, `plot_variable`, `plot_missing`) demonstrated on the Titanic dataset
- **[AIC-optimal binning on iris](03-iris-pooling.ipynb)** — Why CATDAP-02's pooling search beats equal-width binning, with cut points visualized against species histograms
- **[Multivariate HelloGoodbye](04-hellogoodbye-multivariate.ipynb)** — Scale to 56 binary variables, use `catdap1` to rank candidates and `catdap2(nvar=k)` to keep the subset search tractable
- **[Real-world EDA on seaborn Titanic](05-real-world-eda.ipynb)** — End-to-end workflow on messy data: missingness inspection, cleanup, mixed-pooling CATDAP-02, and HTML/Plotly export. Requires `pycatdap[tutorial]`.
- **[Target-pair analysis](06-target-pair-titanic.ipynb)** — Drill into a single (target, explanatory) pair with `target_summary` and `plot_target`: four-perspective tables, AIC-optimal binning for continuous explanatories, ΔAIC ranking, Plotly export, and **continuous-target regression mode** via `RegressionTargetSummary` (H-0005). Requires `pycatdap[tutorial]`.
- **[Bivariate Phase B APIs](07-bivariate-phase-b.ipynb)** — Step beyond a single pair: `plot_pair` for symmetric two-column plots, `aic_heatmap` for one-glance ΔAIC matrices, `association_matrix` for the full m × m ΔAIC sweep, and `association_plot` for vcd-style Pearson residuals (H-0006). Requires `pycatdap[tutorial]`.
- **[One-call profile() report](08-profile-titanic.ipynb)** — The v0.5.0 flagship API: `pycatdap.profile(df, response=...)` bundles overview, variable cards, ΔAIC association matrix, CATDAP-02 top subsets, and quality warnings into a single call, then renders a self-contained HTML report with inline Plotly figures (H-0007). Requires `pycatdap[plotly]` and `pycatdap[tutorial]`.
- **[Phase D APIs — target_analysis, quality_report, measures, suite](09-phase-d-target-analysis-and-suite.ipynb)** — The v0.6.0 target-driven additions: `quality_report(df)` for a fast CI-friendly quality scan, `target_analysis(df, response)` for ΔAIC ranking + top-K cross-tabs, `pycatdap.measures.*` (aic / cramers_v / mutual_info + register), `association_matrix(measure=...)` extension, and `pycatdap.suite.AICIndependenceSuite` for the `assert suite_result.passed, suite_result.summary()` CI idiom (H-0008). Requires `pycatdap[plotly]` and `pycatdap[tutorial]`.
- **[Phase G error labelling](10-phase-g-error-labeling.ipynb)** — The v0.7.0 ML-error building blocks: `error_label`, `confusion_label`, `residual_label`, and `abs_residual_pool` turn predictions into CATDAP-ready categorical responses (H-0010).
- **[Phase H error_analysis() one-call](11-phase-h-error-analysis.ipynb)** — The v0.8.0 wrapper: `error_analysis(df, y_true, y_pred)` returns an `ErrorAnalysisResult` with ΔAIC feature ranking, single-variable slices, and confusion/residual summaries (H-0011).
- **[Phase I+J error visualisation](12-phase-i-j-error-visualization.ipynb)** — The v0.9.0 visualisation layer: `plot_confusion` / `plot_confusion_by_slice` / `confusion_aic` (classification) and `residual_plot` / `residual_by_category` / `residual_pool_plot` (regression), plus `ErrorAnalysisResult` delegation methods on both backends (H-0012).
- **[Phase K calibration](13-phase-k-calibration.ipynb)** — The v0.10.0 calibration toolkit: `calibration_curve` reliability diagram with **AIC-optimal probability binning** + Wilson CIs, `brier_score` / `expected_calibration_error` / `maximum_calibration_error`, and the `ErrorAnalysisResult.calibration_curve` delegation (binary classification, H-0013). Requires `pycatdap[plotly]` and `pycatdap[tutorial]`.

## Planned

As Phases land on the [roadmap](../project/roadmap.md), additional tutorials will appear here:

| Tutorial | Phase | Status |
|---|---|---|
| Slice discovery on Adult Income / COMPAS | L | 🟡 v0.11 |
| Cohort comparison + drift detection | L | 🟡 v0.12 |

The original tracking issue [#27](https://github.com/nbx-liz/pycatdap/issues/27) (basic tutorial set) was closed in v0.3+; the table above lists tutorials still pending against future phases.
