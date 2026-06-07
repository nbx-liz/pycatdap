# Quickstart

This page gets you running CATDAP on real data in five minutes.

## 1. CATDAP-01: pairwise variable relevance

```python
import pycatdap

# Load the bundled Heart Disease dataset (303 rows, 14 columns; UCI, permissive)
df = pycatdap.datasets.load_heart_disease()

# CATDAP-01 operates on categorical variables; pick the coded-categorical columns
cat = df[["target", "sex", "cp", "exang", "thal"]]
result = pycatdap.catdap1(cat, response_names=["target"])

# AIC matrix (rows = response, columns = explanatory)
print(result.aic)

# Variables ranked by AIC (most informative first)
print(result.aic_order["target"])
```

A negative ΔAIC means the explanatory variable is **informative** about the response; non-negative means it is not.

## 2. CATDAP-02: best explanatory subset

```python
# Find the best subset of explanatory variables for "target"
result = pycatdap.catdap2(
    df,
    # pooling per column: 1 = pool continuous, 2 = categorical (no pooling)
    pool=[1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2],
    response_name="target",
    nvar=6,  # shortlist top-6 candidates to keep the subset search tractable
)

print(f"Base AIC (no explanatory): {result.base_aic:.2f}")
print(f"Best subsets ranked by AIC:")
for subset in result.subsets[:5]:
    print(f"  AIC={subset.aic:.2f}, vars={subset.variables}")
```

## 3. Plot the result

```python
from pycatdap.plotting import aic_comparison_plot
import matplotlib.pyplot as plt

aic_comparison_plot(result)
plt.show()
```

## What's next?

- **EDA workflow** — see [Tutorials](../tutorials/index.md) for `profile()` and other higher-level EDA APIs (coming in v0.3+)
- **ML error analysis** — `error_analysis(df, y_true, y_pred)` for slice discovery and cohort analysis (coming in v0.7+)
- **Visualization** — Plotly backend, AIC heatmap, association plot (coming in v0.3+)

Track progress on the [roadmap](../project/roadmap.md).
