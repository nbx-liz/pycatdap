# Quickstart

This page gets you running CATDAP on real data in five minutes.

## 1. CATDAP-01: pairwise variable relevance

```python
import pycatdap

# Load the bundled HealthData dataset (52 examples, 8 categorical columns)
df = pycatdap.datasets.load_health_data()

# Run CATDAP-01: pairwise AIC for all categorical variable combinations
result = pycatdap.catdap1(df, response_names=["symptoms"])

# AIC matrix (rows = response, columns = explanatory)
print(result.aic)

# Variables ranked by AIC (most informative first)
print(result.aic_order["symptoms"])
```

A negative ΔAIC means the explanatory variable is **informative** about the response; non-negative means it is not.

## 2. CATDAP-02: best explanatory subset

```python
# Find the best subset of explanatory variables for "symptoms"
result = pycatdap.catdap2(
    df,
    pool=[2, 2, 2, 0, 0, 0, 0, 2],          # pooling strategy per column
    response_name="symptoms",
    accuracy=[0., 0., 0., 1., 1., 1., 0.1, 0.],  # precision for continuous vars
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
