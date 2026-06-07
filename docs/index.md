# pycatdap

**AIC-based EDA and ML error analysis library for categorical data.**

`pycatdap` is a Python implementation of CATDAP (CATegorical Data Analysis Program), originally developed by Sakamoto & Katsura (1980) at the Institute of Statistical Mathematics. It extends the classic CATDAP toolkit with modern EDA and ML error analysis workflows.

## What makes pycatdap unique

Unlike `ydata-profiling`, `Skrub`, `DivExplorer`, or `pysubgroup`, pycatdap provides:

- **AIC-based variable relevance ranking** — captures the trade-off between information and complexity (unlike Cramér's V or mutual information)
- **AIC-optimal continuous binning** — principled binning of continuous variables (vs. arbitrary equal-width or quantile binning)
- **Subset optimization (CATDAP-02)** — discovers the best combination of explanatory variables (unlike feature importance ranking)
- **Model-agnostic ML error analysis** — works with predictions from any framework (sklearn, LightGBM, XGBoost, PyTorch)

## At a glance

=== "EDA"

    ```python
    import pycatdap

    df = pycatdap.datasets.load_titanic()
    profile = pycatdap.profile(df, response="Survived")
    profile.to_html("titanic_eda.html")
    ```

=== "ML error analysis"

    ```python
    import pycatdap

    result = pycatdap.error_analysis(
        df=test_df,
        y_true=y_test,
        y_pred=model.predict(X_test),
    )
    result.show()  # in Jupyter
    ```

=== "Classic CATDAP"

    ```python
    import pycatdap

    df = pycatdap.datasets.load_heart_disease()
    cat = df[["target", "sex", "cp", "exang", "thal"]]
    r = pycatdap.catdap1(cat, response_names=["target"])
    print(r.aic_order)
    ```

## Navigating these docs

This documentation follows the [Diátaxis framework](https://diataxis.fr/):

- **[Getting Started](getting-started/installation.md)** — install and run your first analysis in 5 minutes
- **[Tutorials](tutorials/index.md)** — step-by-step learning paths for each feature area
- **[How-to Guides](how-to/index.md)** — solutions to specific tasks
- **[API Reference](reference/index.md)** — complete function and class documentation (auto-generated)
- **[Explanation](explanation/index.md)** — concepts, mathematical foundations, design rationale

## Project status

- Version: see [PyPI](https://pypi.org/project/pycatdap/)
- Roadmap: [project/roadmap](project/roadmap.md)
- Issues: [GitHub Issues](https://github.com/nbx-liz/pycatdap/issues)

## Citation

If you use pycatdap in research, please cite:

```bibtex
@article{sakamoto1980categorical,
  title={Categorical Data Analysis by AIC},
  author={Sakamoto, Yosiyuki and Katsura, Koichi},
  journal={Mathematical Sciences},
  year={1980}
}
```
