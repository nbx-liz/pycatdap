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
from pycatdap._association import association_matrix
from pycatdap._target_pair import (
    RegressionTargetSummary,
    TargetSummary,
    target_summary,
)
from pycatdap._version import (
    __version__,
    __version_tuple__,
)
from pycatdap.catdap1 import Catdap1Result, catdap1
from pycatdap.catdap2 import Catdap2Result, catdap2
from pycatdap.eda import DescribeResult, describe
from pycatdap.plot import (
    aic_heatmap,
    association_plot,
    plot_missing,
    plot_pair,
    plot_target,
    plot_variable,
)
from pycatdap.profile import (
    ProfileResult,
    QualityWarning,
    VariableCard,
    profile,
)
from pycatdap.quality_report import QualityReport, quality_report

__all__ = [
    "__version__",
    "__version_tuple__",
    "Catdap1Result",
    "Catdap2Result",
    "DescribeResult",
    "ProfileResult",
    "QualityReport",
    "QualityWarning",
    "RegressionTargetSummary",
    "TargetSummary",
    "VariableCard",
    "aic_heatmap",
    "association_matrix",
    "association_plot",
    "catdap1",
    "catdap2",
    "datasets",
    "describe",
    "plot_missing",
    "plot_pair",
    "plot_target",
    "plot_variable",
    "profile",
    "quality_report",
    "target_summary",
]
