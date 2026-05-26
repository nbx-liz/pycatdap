# AIC Foundations

CATDAP applies Akaike's Information Criterion (AIC) to contingency-table models.

## The two-way AIC

Given a response variable $E$ and an explanatory variable $F$, the AIC for the contingency-table model is:

$$
AIC(E; F) = -2 \sum_{i,j} n_{EF}(i,j) \ln \frac{n_{EF}(i,j)}{n_F(j)} + 2 (C_E - 1) C_F
$$

where:

- $n_{EF}(i, j)$ — cross-tab frequency for response category $i$ and explanatory category $j$
- $n_F(j)$ — marginal frequency of explanatory category $j$
- $C_E$, $C_F$ — number of categories for $E$ and $F$

## Base AIC (no explanatory model)

$$
AIC(E; \phi) = -2 \sum_i n_E(i) \ln \frac{n_E(i)}{n} + 2 (C_E - 1)
$$

## ΔAIC (the value pycatdap reports)

$$
\Delta AIC = AIC(E; F) - AIC(E; \phi)
$$

Interpretation:

- $\Delta AIC < 0$ → $F$ is **informative** about $E$
- $\Delta AIC \geq 0$ → $F$ adds no information beyond model complexity

## Zero-frequency convention

CATDAP follows the convention $0 \cdot \ln(0) = 0$. The internal `_safe_xlogy` helper uses `scipy.special.xlogy` when available and falls back to a vectorized `np.where` implementation otherwise. This guarantees numerical stability even on sparse contingency tables.

## Why AIC over other association measures

Unlike Cramér's V or mutual information, AIC explicitly trades **information gain** against **model complexity** (the $2(C_E - 1)C_F$ penalty). This makes it especially well-suited to:

- Variable selection — you don't need a separate p-value threshold
- Comparing models with different numbers of parameters
- Continuous-variable pooling — the AIC of different bin counts can be directly compared

## References

- Sakamoto, Y., & Katsura, K. (1980). *Categorical Data Analysis by AIC*. Mathematical Sciences.
- Akaike, H. (1973). *Information theory as an extension of the maximum likelihood principle*.
