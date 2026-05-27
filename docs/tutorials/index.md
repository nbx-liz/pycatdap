# Tutorials

Learning-oriented walkthroughs that guide you from zero to confident usage.

## Available

- **[Basic CATDAP](01-basic-catdap.ipynb)** — The original v0.2 tutorial walkthrough using HealthData
- **[EDA on Titanic](02-eda-titanic.ipynb)** — v0.3+ univariate EDA APIs (`describe`, `plot_variable`, `plot_missing`) demonstrated on the Titanic dataset
- **[AIC-optimal binning on iris](03-iris-pooling.ipynb)** — Why CATDAP-02's pooling search beats equal-width binning, with cut points visualized against species histograms
- **[Multivariate HelloGoodbye](04-hellogoodbye-multivariate.ipynb)** — Scale to 56 binary variables, use `catdap1` to rank candidates and `catdap2(nvar=k)` to keep the subset search tractable
- **[Real-world EDA on seaborn Titanic](05-real-world-eda.ipynb)** — End-to-end workflow on messy data: missingness inspection, cleanup, mixed-pooling CATDAP-02, and HTML/Plotly export. Requires `pycatdap[tutorial]`.
- **[Target-pair analysis](06-target-pair-titanic.ipynb)** — Drill into a single (target, explanatory) pair with `target_summary` and `plot_target`: four-perspective tables, AIC-optimal binning for continuous explanatories, ΔAIC ranking, and Plotly export. Requires `pycatdap[tutorial]`.

## Planned

As Phases land on the [roadmap](../project/roadmap.md), additional tutorials will appear here:

| Tutorial | Phase | Status |
|---|---|---|
| Continuous-target analysis (regression residuals) | H-0005 | 🟡 research ([#56](https://github.com/nbx-liz/pycatdap/issues/56)) |
| Target analysis on Penguins | D | 🟡 v0.6 |
| Classification error analysis on Titanic predictions | G/H/I | 🟡 v0.7-v0.9 |
| Regression error analysis on California Housing | J | 🟡 v0.9 |
| Calibration with AIC binning | K | 🟡 v0.10 |
| Slice discovery on Adult Income / COMPAS | L | 🟡 v0.11 |

The original tracking issue [#27](https://github.com/nbx-liz/pycatdap/issues/27) (basic tutorial set) was closed in v0.3+; the table above lists tutorials still pending against future phases.
