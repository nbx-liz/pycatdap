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

| Version | Theme | Status |
|---|---|---|
| v0.2.0 | Core CATDAP-01/02 | ✅ released |
| v0.2.x | R numerical cross-validation | 🟡 planned ([#10](https://github.com/nbx-liz/pycatdap/issues/10)) |
| v0.3.0 | Plotly backend + univariate EDA | 🟡 planned ([#12](https://github.com/nbx-liz/pycatdap/issues/12)) |
| v0.4.0 | Bivariate EDA | 🟡 planned ([#13](https://github.com/nbx-liz/pycatdap/issues/13)) |
| v0.5.0 | `profile()` + HTML report | 🟡 planned ([#14](https://github.com/nbx-liz/pycatdap/issues/14)) |
| v0.6.0 | `target_analysis()` + Suite API | 🟡 planned ([#15](https://github.com/nbx-liz/pycatdap/issues/15)) |
| v0.7.0 | Error labeling utilities | 🟡 planned ([#16](https://github.com/nbx-liz/pycatdap/issues/16)) |
| v0.8.0 | `error_analysis()` one-call | 🟡 planned ([#17](https://github.com/nbx-liz/pycatdap/issues/17)) |
| v0.9.0 | Error visualization | 🟡 planned ([#18](https://github.com/nbx-liz/pycatdap/issues/18)) |
| v0.10.0 | Calibration with AIC binning | 🟡 planned ([#19](https://github.com/nbx-liz/pycatdap/issues/19)) |
| v0.11.0 | Slice discovery, cohort comparison, drift | 🟡 planned ([#20](https://github.com/nbx-liz/pycatdap/issues/20)) |
| v0.12.0 | LizyStudio integration | 🟡 planned ([#21](https://github.com/nbx-liz/pycatdap/issues/21)) |
| v1.0.0 | API stabilization | 🟡 planned ([#33](https://github.com/nbx-liz/pycatdap/issues/33)) |

## Cross-cutting themes

- **Datasets** — [#22](https://github.com/nbx-liz/pycatdap/issues/22), [#23](https://github.com/nbx-liz/pycatdap/issues/23), [#24](https://github.com/nbx-liz/pycatdap/issues/24), [#25](https://github.com/nbx-liz/pycatdap/issues/25)
- **Documentation** — [#26](https://github.com/nbx-liz/pycatdap/issues/26), [#27](https://github.com/nbx-liz/pycatdap/issues/27), [#28](https://github.com/nbx-liz/pycatdap/issues/28)
- **Quality** — [#29](https://github.com/nbx-liz/pycatdap/issues/29), [#30](https://github.com/nbx-liz/pycatdap/issues/30), [#34](https://github.com/nbx-liz/pycatdap/issues/34)
- **Interop** — [#31](https://github.com/nbx-liz/pycatdap/issues/31), [#32](https://github.com/nbx-liz/pycatdap/issues/32)

## Meta issue

Track overall progress on [Issue #11](https://github.com/nbx-liz/pycatdap/issues/11).
