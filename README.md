# pycatdap

[![PyPI version](https://img.shields.io/pypi/v/pycatdap.svg)](https://pypi.org/project/pycatdap/)
[![Python versions](https://img.shields.io/pypi/pyversions/pycatdap.svg)](https://pypi.org/project/pycatdap/)
[![CI](https://github.com/nbx-liz/pycatdap/actions/workflows/ci.yml/badge.svg)](https://github.com/nbx-liz/pycatdap/actions/workflows/ci.yml)
[![Docs](https://github.com/nbx-liz/pycatdap/actions/workflows/docs.yml/badge.svg)](https://nbx-liz.github.io/pycatdap/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AIC-based EDA and ML error analysis library for categorical data.**

`pycatdap` is a Python implementation of CATDAP (CATegorical Data Analysis Program), developed by Sakamoto & Katsura (1980) at the Institute of Statistical Mathematics. It extends the classic CATDAP toolkit with modern exploratory data analysis (EDA) and machine learning error analysis workflows.

📖 **Documentation**: <https://nbx-liz.github.io/pycatdap/>

## Why pycatdap?

Unlike general profilers (`ydata-profiling`, `Skrub`) or slice discovery tools (`DivExplorer`, `pysubgroup`), pycatdap uses **AIC** as its core relevance measure. This gives it four unique advantages:

| Feature | Most tools | pycatdap |
|---|---|---|
| Variable relevance | Cramér's V, mutual info | **AIC** — explicit info-vs-complexity trade-off |
| Continuous binning | Equal-width or quantile | **AIC-optimal** binning |
| Subset discovery | Feature importance ranking | **CATDAP-02** combinatorial search |
| Model coupling | Tied to specific frameworks | **Model-agnostic** (works with `y_true`, `y_pred` from anywhere) |

## Installation

```bash
# Core
pip install pycatdap

# With visualization (matplotlib)
pip install "pycatdap[plot]"

# With interactive Plotly figures + HTML reports
pip install "pycatdap[plotly]"
```

Supported: Python 3.10 / 3.11 / 3.12 / 3.13

## Quickstart

### Classic CATDAP

```python
import pycatdap

df = pycatdap.datasets.load_health_data()

# CATDAP-01: pairwise AIC analysis
result = pycatdap.catdap1(df, response_names=["symptoms"])
print(result.aic_order["symptoms"])  # variables ranked by ΔAIC

# CATDAP-02: best explanatory subset
result2 = pycatdap.catdap2(
    df,
    pool=[2, 2, 2, 0, 0, 0, 0, 2],
    response_name="symptoms",
    accuracy=[0., 0., 0., 1., 1., 1., 0.1, 0.],
)
for s in result2.subsets[:3]:
    print(f"AIC={s.aic:.2f}, vars={s.variables}")
```

### EDA (planned, v0.3+)

```python
# Coming in v0.5
profile = pycatdap.profile(df, response="symptoms")
profile.to_html("report.html")
profile.show()  # Jupyter inline
```

### ML error analysis (planned, v0.8+)

```python
# Coming in v0.8
result = pycatdap.error_analysis(
    df=test_df,
    y_true=y_test,
    y_pred=model.predict(X_test),
)
result.show()                       # Jupyter
result.to_html("errors.html")       # standalone report
result.top_slices                   # natural-language cohort descriptions
```

## Status & Roadmap

| Version | Theme |
|---|---|
| v0.2.0 ✅ | Core CATDAP-01/02 (released) |
| v0.3.0 — v0.6.0 | EDA workflow (Plotly backend, profile, target analysis) |
| v0.7.0 — v0.11.0 | ML error analysis (slice discovery, calibration, drift) |
| v0.12.0 | LizyStudio integration |
| v1.0.0 | API stabilization |

Full roadmap: [PLAN.md](PLAN.md) · [Meta Issue #11](https://github.com/nbx-liz/pycatdap/issues/11)

## Development

```bash
git clone https://github.com/nbx-liz/pycatdap.git
cd pycatdap
uv sync --all-groups
uv run pytest                                  # tests (excluding slow R cross-validation)
uv run pytest -m slow                          # slow tests (requires R + catdap package)
uv run python -m mkdocs serve                  # local docs preview
make ci                                        # ruff + mypy + pytest + build
```

Contributing guidelines: [CONTRIBUTING.md](CONTRIBUTING.md)

## Project structure

| Document | Purpose |
|---|---|
| [BLUEPRINT.md](BLUEPRINT.md) | Canonical specification (Japanese) |
| [HISTORY.md](HISTORY.md) | Proposal-to-decision log (Japanese) |
| [PLAN.md](PLAN.md) | Development roadmap (Japanese) |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [docs/](docs/) | Published documentation site |

## Citation

If you use pycatdap in research, please cite the original CATDAP work:

```bibtex
@article{sakamoto1980categorical,
  title={Categorical Data Analysis by AIC},
  author={Sakamoto, Yosiyuki and Katsura, Koichi},
  journal={Mathematical Sciences},
  year={1980}
}
```

## License

[MIT](LICENSE)
