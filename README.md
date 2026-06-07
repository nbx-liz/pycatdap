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

df = pycatdap.datasets.load_heart_disease()

# CATDAP-01: pairwise AIC on the coded-categorical columns
cat = df[["target", "sex", "cp", "exang", "thal"]]
result = pycatdap.catdap1(cat, response_names=["target"])
print(result.aic_order["target"])  # variables ranked by ΔAIC

# CATDAP-02: best explanatory subset (continuous columns auto-pooled)
result2 = pycatdap.catdap2(
    df,
    #     age sex cp trestbps chol fbs restecg thalach exang oldpeak slope ca thal target
    pool=[1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2],
    response_name="target",
    nvar=6,
)
for s in result2.subsets[:3]:
    print(f"AIC={s.aic:.2f}, vars={s.variables}")
```

### One-call EDA report (v0.5+)

```python
report = pycatdap.profile(df, response="target")
report.show()                       # Jupyter inline
report.to_html("report.html")       # self-contained HTML, inline Plotly
report.to_dict()                    # JSON-friendly
report.to_plotly_json()             # react-plotly.js / LizyStudio
```

`ProfileResult` exposes `overview`, `variables` (one `VariableCard` per
column, including ΔAIC vs the response), `association` (m × m ΔAIC
matrix), `top_subsets` (CATDAP-02 result when `response` is given), and
`quality_warnings` (`high_cardinality` / `constant` / `id_candidate` /
`high_missing` with overridable thresholds). See
[`docs/tutorials/08-profile-titanic.ipynb`](docs/tutorials/08-profile-titanic.ipynb)
for an end-to-end walkthrough.

### Target analysis and CI-integrable suite (v0.6+)

```python
# Target-driven: rank every column by ΔAIC vs `response`, keep top-K cross-tabs
ta = pycatdap.target_analysis(df, response="symptoms", top_k=5)
ta.ranking                         # variable / delta_aic / kind / n_obs
ta.top_summaries["cholesterol"]    # full TargetSummary for drill-down

# Quality scan only (fast — no catdap2 / association_matrix)
qr = pycatdap.quality_report(df)
assert qr.passed, qr.show()

# CI gate: one-line data contract
suite = pycatdap.suite.AICIndependenceSuite(df, response="symptoms")
result = suite.run()
assert result.passed, result.summary()

# Non-AIC association measures (pure-numpy, no scipy)
m = pycatdap.association_matrix(df, measure="cramers_v")
pycatdap.measures.register("my_measure", my_fn)  # pluggable per pysubgroup convention
```

See [`docs/tutorials/09-target-analysis-and-quality-suite.ipynb`](docs/tutorials/09-target-analysis-and-quality-suite.ipynb).

### ML error labelling (v0.7.0)

```python
from pycatdap.datasets import load_german_credit

df = load_german_credit()
y_true = df["class"]
y_pred = my_model.predict(df.drop(columns=["class"]))

# Label every prediction "correct" / "incorrect"
labels = pycatdap.error.error_label(y_true, y_pred)

# Or get fine-grained TP / FP / FN / TN (binary classification only)
conf = pycatdap.error.confusion_label(y_true, y_pred, positive="bad")

# Feed the error label back into target_analysis to discover which columns
# explain the errors — foundation for v0.8.0 `error_analysis()`
ta = pycatdap.target_analysis(df.assign(was_correct=labels), response="was_correct")
```

See [`docs/tutorials/10-ml-error-labeling.ipynb`](docs/tutorials/10-ml-error-labeling.ipynb).

### One-call ML error analysis (v0.8.0)

```python
# task auto-detected from y_true / y_pred dtypes
result = pycatdap.error_analysis(
    df=test_df,
    y_true=y_test,                                  # str column name or array
    y_pred=model.predict(X_test),                   # str column name or array
    top_k=5,
)
result.show()                                       # Jupyter / stdout summary
result.to_html("errors.html")                       # self-contained Plotly report
result.feature_ranking                              # ΔAIC ranking of explanatories
result.top_slices                                   # single-variable cohort slices
result.confusion                                    # canonical TP/FP/FN/TN (binary)
result.to_divexplorer_format()                      # DivExplorer-compatible DataFrame

# Larger fairness-relevant benchmarks (needs `pip install 'pycatdap[data]'`)
df = pycatdap.datasets.fetch_california_housing()   # regression
df = pycatdap.datasets.fetch_adult_income()         # fairness demo
df = pycatdap.datasets.fetch_compas()               # fairness demo
```

See [`docs/tutorials/11-ml-error-analysis-one-call.ipynb`](docs/tutorials/11-ml-error-analysis-one-call.ipynb).

### ML error visualisation (v0.9.0)

```python
r = pycatdap.error_analysis(df, y_true, y_pred)

# Result delegation — visualise straight off the result
r.plot_confusion()                                  # binary OR multi-class
r.plot_confusion(backend="plotly", normalize="true")
r.residual_plot()                                   # regression

# Or call the standalone functions
pycatdap.error.plot_confusion(y_true, y_pred, labels=[0, 1], normalize="true")
pycatdap.error.plot_confusion_by_slice(df, y_true, y_pred, var="age_group")
pycatdap.error.confusion_aic(y_true, y_pred)        # ΔAIC, negative = informative

pycatdap.error.residual_plot(y_true, y_pred, kind="histogram")
pycatdap.error.residual_by_category(df, y_true, y_pred, "feature")
pycatdap.error.residual_pool_plot(y_true, y_pred, n_bins=4)
```

See [`docs/tutorials/12-ml-error-visualization.ipynb`](docs/tutorials/12-ml-error-visualization.ipynb).

### ML calibration (v0.10.0)

```python
r = pycatdap.error_analysis(df, y_true, y_pred, y_proba=proba)  # binary classification
r.calibration_curve(strategy="aic")                 # reliability diagram (AIC-binned)

# Or call the standalone functions
pycatdap.error.calibration_curve(y_true, proba, strategy="aic", backend="plotly")
pycatdap.error.brier_score(y_true, proba)
pycatdap.error.expected_calibration_error(y_true, proba)   # ECE
pycatdap.error.maximum_calibration_error(y_true, proba)    # MCE
```

`strategy="aic"` bins the probability axis where the observed positive-rate shifts — sharper than equal-width / quantile bins on skewed predictions. See [`docs/tutorials/13-ml-calibration.ipynb`](docs/tutorials/13-ml-calibration.ipynb).

### ML slice discovery, cohort comparison & drift (v0.11.0)

```python
# Auto-discover the multivariable cohorts where the model fails most
result = pycatdap.error.discover_error_slices(
    df, y_true, y_pred, max_vars=3, measure="aic", top_k=10, min_support=30
)
for s in result.slices:
    print(s.error_metric, s.description)   # e.g. "age ∈ [60, 78] × plan = basic"
result.to_divexplorer_format()             # DivExplorer-compatible flat table

# Compare two cohorts (distribution + ΔAIC), Sweetviz-style HTML report
pycatdap.error.compare_cohorts(df_a, df_b).to_html("comparison.html")

# Detect train→prod drift, ranked by ΔAIC magnitude
pycatdap.error.detect_drift(df_train, df_prod, y_true=y, y_pred=yhat)

# Calibration beyond binary classification
pycatdap.error.regression_calibration_table(y_true, y_pred)          # regression
pycatdap.error.multiclass_calibration_table(y_true, y_proba)         # one-vs-rest
```

Slice discovery prunes the search space on **support** (Apriori, anti-monotone) rather than ΔAIC — sound, and >50% reduction on wide datasets. The interestingness measure is pluggable (`"aic"`, `"cramers_v"`, `"mutual_info"`, or any registered callable). See [`docs/tutorials/14-ml-slice-discovery-and-drift.ipynb`](docs/tutorials/14-ml-slice-discovery-and-drift.ipynb).

## Status & Roadmap

| Version | Theme |
|---|---|
| v0.2.0 ✅ | Core CATDAP-01/02 (released) |
| v0.3.0 — v0.6.0 ✅ | EDA workflow (Plotly backend, profile, target analysis) |
| v0.7.0 ✅ | error labelling building blocks |
| v0.8.0 ✅ | one-call `error_analysis()` + benchmark datasets |
| v0.9.0 ✅ | error visualisation (confusion + residual) |
| v0.10.0 ✅ | calibration (AIC-binned reliability diagram + Brier/ECE/MCE) |
| v0.11.0 ✅ | slice discovery + cohort comparison + drift + regression/multi-class calibration |
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
