"""Sample datasets for CATDAP analysis.

Bundled datasets from the R ``catdap`` package for testing and examples.
"""

from __future__ import annotations

import gzip
from importlib import resources
from pathlib import Path

import pandas as pd


def _data_path(filename: str) -> Path:
    """Resolve path to a bundled data file."""
    ref = resources.files("pycatdap") / "data" / filename
    # resources.files returns a Traversable; convert to concrete path
    with resources.as_file(ref) as p:
        return Path(p)


def load_health_data() -> pd.DataFrame:
    """Load the HealthData dataset (52 observations, 8 variables).

    Medical data with mixed categorical and continuous variables,
    originally used in the CATDAP-02 example by Sakamoto & Katsura.

    Variables
    ---------
    opthalmo. : int (1, 2)
        Ophthalmic examination result.
    ecg : int (1, 2)
        Electrocardiogram result.
    symptoms : str ('A', 'B')
        Symptom classification (response variable).
    age : int
        Patient age.
    max.press : int
        Maximum blood pressure.
    min.press : int
        Minimum blood pressure.
    aortic.wav : float
        Aortic wave measurement.
    cholesterol : str ('low', 'high')
        Cholesterol level.

    Returns
    -------
    DataFrame
        52 rows, 8 columns.

    Examples
    --------
    >>> from pycatdap.datasets import load_health_data
    >>> df = load_health_data()
    >>> df.shape
    (52, 8)
    """
    path = _data_path("health_data.csv")
    return pd.read_csv(path)


def load_hello_goodbye() -> pd.DataFrame:
    """Load the HelloGoodbye dataset (13954 observations, 56 binary variables).

    Anonymous binary data used to demonstrate CATDAP-02 with large
    multivariate datasets.  All variables are binary (0/1).

    Variables
    ---------
    Isay : int (0, 1)
        Response variable.
    You1say .. You55say : int (0, 1)
        Explanatory binary variables.

    Returns
    -------
    DataFrame
        13954 rows, 56 columns.

    Examples
    --------
    >>> from pycatdap.datasets import load_hello_goodbye
    >>> df = load_hello_goodbye()
    >>> df.shape
    (13954, 56)
    """
    path = _data_path("hello_goodbye.csv.gz")
    with gzip.open(path, "rt") as f:
        return pd.read_csv(f)
