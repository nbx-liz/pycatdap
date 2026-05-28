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


def load_titanic() -> pd.DataFrame:
    """Load the Titanic dataset (2201 observations, 4 categorical variables).

    Long-form expansion of R ``datasets::Titanic`` (4-way contingency table
    of Class × Sex × Age × Survived). Each cell of the original table is
    expanded to its frequency in row-level form.

    Variables
    ---------
    Class : str ('1st', '2nd', '3rd', 'Crew')
        Passenger or crew class.
    Sex : str ('Male', 'Female')
        Passenger sex.
    Age : str ('Adult', 'Child')
        Passenger age category.
    Survived : str ('Yes', 'No')
        Whether the passenger survived.

    Returns
    -------
    DataFrame
        2201 rows, 4 columns. All columns are categorical strings.

    References
    ----------
    R Core Team (R `datasets::Titanic`): contingency table of survival on
    the Titanic. Public domain.

    Examples
    --------
    >>> from pycatdap.datasets import load_titanic
    >>> df = load_titanic()
    >>> df.shape
    (2201, 4)
    >>> int(df["Survived"].value_counts()["Yes"])
    711
    """
    path = _data_path("titanic.csv")
    return pd.read_csv(path)


def load_iris() -> pd.DataFrame:
    """Load Fisher's iris dataset (150 observations, 5 variables).

    Classic dataset with three iris species and four continuous
    morphological measurements. Useful for demonstrating CATDAP-02 with
    continuous variable pooling.

    Variables
    ---------
    Sepal.Length : float
        Sepal length in cm.
    Sepal.Width : float
        Sepal width in cm.
    Petal.Length : float
        Petal length in cm.
    Petal.Width : float
        Petal width in cm.
    Species : str ('setosa', 'versicolor', 'virginica')
        Iris species (response variable).

    Returns
    -------
    DataFrame
        150 rows, 5 columns. Continuous variables for the 4 features
        and a categorical Species column.

    References
    ----------
    Fisher, R. A. (1936). The use of multiple measurements in taxonomic
    problems. Public domain.

    Examples
    --------
    >>> from pycatdap.datasets import load_iris
    >>> df = load_iris()
    >>> df.shape
    (150, 5)
    >>> sorted(df["Species"].unique().tolist())
    ['setosa', 'versicolor', 'virginica']
    """
    path = _data_path("iris.csv")
    return pd.read_csv(path)


def load_german_credit() -> pd.DataFrame:
    """Load the Statlog German Credit dataset (1000 observations, 21 variables).

    Binary classification benchmark used across the fairness / ML
    error analysis literature. Each row represents a credit applicant
    with mixed categorical and continuous attributes; the ``class``
    column is the label (``"good"`` / ``"bad"`` credit risk).

    Variables
    ---------
    checking_status, savings_status, employment, ... : str
        Categorical attributes describing the applicant's banking,
        employment, housing, and demographic profile.
    duration, credit_amount, age, installment_commitment, ... : int
        Continuous attributes.
    class : str ('good', 'bad')
        Binary credit risk label.

    Returns
    -------
    DataFrame
        1000 rows, 21 columns. 17 categorical columns and 4 integer
        columns including the binary ``class`` label.

    References
    ----------
    Hofmann, H. (1994). Statlog (German Credit Data) Data Set.
    UCI Machine Learning Repository.
    https://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29
    Bundled here via OpenML id ``credit-g`` v1. Public domain.

    Examples
    --------
    >>> from pycatdap.datasets import load_german_credit
    >>> df = load_german_credit()
    >>> df.shape
    (1000, 21)
    >>> df["class"].value_counts().to_dict()
    {'good': 700, 'bad': 300}
    """
    path = _data_path("german_credit.csv")
    return pd.read_csv(path)


def load_heart_disease() -> pd.DataFrame:
    """Load the Cleveland Heart Disease dataset (303 observations, 14 variables).

    Binary classification benchmark from the UCI Machine Learning
    Repository (the processed Cleveland subset). Used widely in
    fairness and interpretability research.

    Variables
    ---------
    age, trestbps, chol, thalach, oldpeak : float
        Continuous clinical measurements.
    sex, cp, fbs, restecg, exang, slope, ca, thal : float
        Encoded categorical clinical attributes.
    target : float (0, 1)
        Binary indicator of heart disease presence.

    Returns
    -------
    DataFrame
        303 rows, 14 columns. All numeric columns; ``target`` is the
        binary label.

    References
    ----------
    Detrano, R., et al. (1989). Heart Disease Data Set.
    UCI Machine Learning Repository.
    https://archive.ics.uci.edu/ml/datasets/heart+disease
    Bundled here via OpenML id ``heart-disease`` v1. CC BY 4.0.

    Examples
    --------
    >>> from pycatdap.datasets import load_heart_disease
    >>> df = load_heart_disease()
    >>> df.shape
    (303, 14)
    """
    path = _data_path("heart_disease.csv")
    return pd.read_csv(path)


def load_penguins() -> pd.DataFrame:
    """Load the Palmer Penguins dataset (344 observations, 7 variables).

    Three-class classification dataset based on observations of
    Adelie, Chinstrap, and Gentoo penguins from the Palmer Station
    Long Term Ecological Research program. Popular replacement for
    iris in classification tutorials.

    Variables
    ---------
    species : str ('Adelie', 'Chinstrap', 'Gentoo')
        Three-class species label.
    island : str ('Torgersen', 'Biscoe', 'Dream')
        Island on which the penguin was observed.
    culmen_length_mm, culmen_depth_mm, flipper_length_mm, body_mass_g : float
        Morphological measurements (may contain NaN).
    sex : str ('MALE', 'FEMALE')
        Reported sex (may contain NaN).

    Returns
    -------
    DataFrame
        344 rows, 7 columns. 3 string columns and 4 float columns.

    References
    ----------
    Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). palmerpenguins.
    https://allisonhorst.github.io/palmerpenguins/
    Bundled here via OpenML id ``penguins`` v1. CC0 1.0 Universal.

    Examples
    --------
    >>> from pycatdap.datasets import load_penguins
    >>> df = load_penguins()
    >>> df.shape
    (344, 7)
    >>> sorted(df["species"].unique().tolist())
    ['Adelie', 'Chinstrap', 'Gentoo']
    """
    path = _data_path("penguins.csv")
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
