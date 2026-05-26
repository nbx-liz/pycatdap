"""pycatdap: Python implementation of CATDAP (CATegorical Data Analysis Program).

CATDAP applies Akaike's Information Criterion (AIC) to categorical data analysis.
Originally developed by Sakamoto & Katsura (1980) at the Institute of Statistical
Mathematics, Japan.

Main functions:
    catdap1 -- Pairwise AIC evaluation of categorical variable
               associations
    catdap2 -- Optimal explanatory variable subset search
               with continuous variable binning
"""

from __future__ import annotations

from pycatdap import datasets
from pycatdap._version import (
    __version__,
    __version_tuple__,
)
from pycatdap.catdap1 import Catdap1Result, catdap1
from pycatdap.catdap2 import Catdap2Result, catdap2
from pycatdap.eda import DescribeResult, describe
from pycatdap.plot import plot_missing, plot_variable

__all__ = [
    "__version__",
    "__version_tuple__",
    "Catdap1Result",
    "Catdap2Result",
    "DescribeResult",
    "catdap1",
    "catdap2",
    "datasets",
    "describe",
    "plot_missing",
    "plot_variable",
]
