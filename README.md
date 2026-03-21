# pycatdap

Python implementation of CATDAP (CATegorical Data Analysis Program).

CATDAP applies Akaike's Information Criterion (AIC) to categorical data analysis.
Originally developed by Sakamoto & Katsura (1980) at the Institute of Statistical Mathematics, Japan.

## Features

- **CATDAP-01**: Pairwise AIC evaluation of categorical variable associations
- **CATDAP-02**: Optimal explanatory variable subset search with continuous variable binning

## Installation

```bash
pip install pycatdap
```

## Quick Start

```python
import pycatdap

# CATDAP-01: Pairwise AIC analysis
result1 = pycatdap.catdap1(data, response_names=["Survived"])
print(result1.aic)

# CATDAP-02: Optimal subset search
result2 = pycatdap.catdap2(data, response_name="symptoms")
print(result2.subsets)
```

## Development

```bash
git clone https://github.com/rem/pycatdap.git
cd pycatdap
uv venv && source .venv/bin/activate
uv pip install -e ".[all]"
pytest
```

## License

MIT
