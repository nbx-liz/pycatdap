# Roadmap

The full development plan lives in **[PLAN.md](https://github.com/nbx-liz/pycatdap/blob/main/PLAN.md)** (Japanese).

This page provides an English summary.

## Vision

`pycatdap` evolves from a CATDAP Python port to a complete **AIC-based EDA and ML error analysis library**, differentiating itself with:

- AIC-driven variable relevance ranking
- AIC-optimal continuous binning
- Subset search (CATDAP-02) as the primary mechanism
- Model-agnostic ML error analysis

## Release milestones

The EDA + ML error-analysis arc (Phases A→M) has all shipped. The latest
release is **v0.12.1**.

| Version | Theme | Status |
|---|---|---|
| v0.2.0 | Core CATDAP-01/02 | ✅ released |
| v0.3.0 | Plotly backend + univariate EDA | ✅ released |
| v0.4.0 | Bivariate EDA (heatmap, association) | ✅ released |
| v0.5.0 | `profile()` + HTML report | ✅ released |
| v0.6.0 | `target_analysis()` + quality suite + measures | ✅ released |
| v0.7.0 | Error labeling utilities + datasets | ✅ released |
| v0.8.0 | `error_analysis()` one-call + datasets | ✅ released |
| v0.9.0 | Classification / regression error visualization | ✅ released |
| v0.10.0 | Calibration with AIC binning | ✅ released |
| v0.11.0 | Slice discovery, cohort comparison, drift | ✅ released |
| v0.12.0 | LizyStudio integration enablement (Plotly JSON contracts) | ✅ released |
| v0.12.1 | `discover_error_slices` candidate cap (OOM guard) | ✅ released |
| v0.12.2 | Housekeeping: quality gates ([#34](https://github.com/nbx-liz/pycatdap/issues/34)), DivExplorer interop docs ([#32](https://github.com/nbx-liz/pycatdap/issues/32)), plan reconciliation | 🟢 in progress (unreleased) |
| v0.13.0 | Datasets D5 + interop (pysubgroup AICMeasure, DivExplorer schema) | 🟢 on develop, unreleased ([#25](https://github.com/nbx-liz/pycatdap/issues/25), [#31](https://github.com/nbx-liz/pycatdap/issues/31), [#32](https://github.com/nbx-liz/pycatdap/issues/32) done; [#47](https://github.com/nbx-liz/pycatdap/issues/47) JNcharacter won't-do — GPL, H-0020) |
| v0.14.0 | R numerical cross-validation + performance benchmarks | 🟡 planned ([#10](https://github.com/nbx-liz/pycatdap/issues/10), [#30](https://github.com/nbx-liz/pycatdap/issues/30), [#29](https://github.com/nbx-liz/pycatdap/issues/29)) |
| v1.0.0 | API stabilization (`plotting.*` → `plot.matplotlib.*`) | 🟡 planned ([#33](https://github.com/nbx-liz/pycatdap/issues/33)) |

## Cross-cutting themes

- **Datasets** — shipped: [#22](https://github.com/nbx-liz/pycatdap/issues/22), [#23](https://github.com/nbx-liz/pycatdap/issues/23), [#24](https://github.com/nbx-liz/pycatdap/issues/24); planned (v0.13.0): [#25](https://github.com/nbx-liz/pycatdap/issues/25), [#47](https://github.com/nbx-liz/pycatdap/issues/47)
- **Documentation** — ✅ all closed: [#26](https://github.com/nbx-liz/pycatdap/issues/26), [#27](https://github.com/nbx-liz/pycatdap/issues/27), [#28](https://github.com/nbx-liz/pycatdap/issues/28)
- **Quality** — ✅ quality gates [#34](https://github.com/nbx-liz/pycatdap/issues/34); planned: benchmarks [#29](https://github.com/nbx-liz/pycatdap/issues/29), R-test CI promotion [#30](https://github.com/nbx-liz/pycatdap/issues/30)
- **Interop** — [#32](https://github.com/nbx-liz/pycatdap/issues/32) DivExplorer: interop guide shipped, full schema fidelity planned (v0.13.0); [#31](https://github.com/nbx-liz/pycatdap/issues/31) pysubgroup planned (v0.13.0)

## Meta issue

Track overall progress on [Issue #11](https://github.com/nbx-liz/pycatdap/issues/11).
