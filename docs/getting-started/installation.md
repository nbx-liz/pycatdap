# Installation

## Standard installation

```bash
pip install pycatdap
```

This installs the core CATDAP-01 / CATDAP-02 functionality with `numpy` and `pandas` as the only required dependencies.

## With visualization support

```bash
pip install "pycatdap[plot]"
```

Adds `matplotlib` and `statsmodels` for the existing v0.2 plotting API.

## With Plotly backend (recommended for interactive use)

```bash
pip install "pycatdap[plotly]"
```

Adds `plotly` and `jinja2` for interactive figures and HTML reports. Required for the modern EDA workflow (`profile()`, `aic_heatmap()`, `error_analysis()`).

!!! note "Future extras"
    The following extras will become available as the roadmap progresses:

    - `pycatdap[widget]` — anywidget for interactive Jupyter widgets
    - `pycatdap[data]` — `requests` and `scikit-learn` for `fetch_*` data loaders
    - `pycatdap[all]` — everything

## Supported Python versions

- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

## Verifying the installation

```python
import pycatdap
print(pycatdap.__version__)
```

## Development install (from source)

```bash
git clone https://github.com/nbx-liz/pycatdap
cd pycatdap
uv sync --all-groups
```

This installs all development dependencies, including documentation tooling (`docs` group).

## Optional: R `catdap` for cross-validation

If you want to run the R cross-validation suite (`pytest -m slow`), you'll need R with the `catdap` package:

```r
install.packages("catdap")
```

These tests are excluded from default CI but required before release tags.
