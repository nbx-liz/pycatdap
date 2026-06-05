"""Sample datasets for CATDAP analysis.

Bundled datasets from the R ``catdap`` package for testing and examples.
"""

from __future__ import annotations

import gzip
import warnings
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


def fetch_california_housing() -> pd.DataFrame:
    """Fetch the California Housing regression dataset (H-0011 D4).

    Thin wrapper over :func:`sklearn.datasets.fetch_california_housing`
    with ``as_frame=True``. The target column ``MedHouseVal`` is
    concatenated into the returned DataFrame so it can be passed
    straight to :func:`pycatdap.error_analysis` as the regression
    response.

    Returns
    -------
    DataFrame
        20,640 rows × 9 columns (8 features + ``MedHouseVal`` target).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Notes
    -----
    - First call downloads the dataset to the sklearn cache
      (``~/scikit_learn_data/`` by default; override with
      ``SCIKIT_LEARN_DATA`` env var).
    - Subsequent calls are offline.

    Examples
    --------
    >>> import pycatdap                                # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_california_housing()  # doctest: +SKIP
    >>> df.shape                                       # doctest: +SKIP
    (20640, 9)
    """
    try:
        from sklearn.datasets import fetch_california_housing as _fetch
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_california_housing. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    bundle = _fetch(as_frame=True)
    df: pd.DataFrame = bundle.frame
    return df


def fetch_adult_income() -> pd.DataFrame:
    """Fetch the Adult Income (Census) classification dataset (H-0011 D4).

    Wrapper over :func:`sklearn.datasets.fetch_openml` with
    ``name="adult"``, ``version=2``, ``as_frame=True``. Binary target
    ``class`` (``<=50K`` / ``>50K``) is concatenated into the
    DataFrame.

    Returns
    -------
    DataFrame
        ~48,842 rows × 15 columns (14 features + ``class`` target).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Notes
    -----
    - First call downloads from OpenML to the sklearn cache.
    - Useful for demonstrating fairness-aware error analysis (the
      dataset has known protected-attribute associations on
      ``sex`` / ``race``).

    Examples
    --------
    >>> import pycatdap                              # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_adult_income()  # doctest: +SKIP
    >>> "class" in df.columns                        # doctest: +SKIP
    True
    """
    try:
        from sklearn.datasets import fetch_openml
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_adult_income. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    bundle = fetch_openml(name="adult", version=2, as_frame=True)
    df: pd.DataFrame = bundle.frame
    return df


def fetch_compas() -> pd.DataFrame:
    """Fetch the COMPAS Two-Year Recidivism dataset (H-0011 D4).

    Wrapper over :func:`sklearn.datasets.fetch_openml` with
    ``name="compas-two-years"`` (ProPublica re-release on OpenML).
    Target ``two_year_recid`` predicts whether a defendant was rearrested
    within two years.

    .. warning::
        COMPAS is a **fairness-critical** dataset originally analysed
        by ProPublica to expose racial bias in pre-trial risk scoring.
        It is included here as a *demonstration dataset for fairness
        analysis*, NOT as a model-evaluation benchmark for
        recidivism-prediction systems intended for real-world use.
        See ProPublica's original methodology and discussion:
        <https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm>.

    Returns
    -------
    DataFrame
        ~5,278 rows × 14 columns (features + target).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Examples
    --------
    >>> import pycatdap                          # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_compas()    # doctest: +SKIP
    """
    try:
        from sklearn.datasets import fetch_openml
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_compas. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    bundle = fetch_openml(name="compas-two-years", version=4, as_frame=True)
    df: pd.DataFrame = bundle.frame
    return df


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


#: UCI column order for the Bank Marketing dataset (``bank-full.csv``).
#: OpenML ``bank-marketing`` (data_id 1461) ships these 16 features as
#: generic ``V1``..``V16``; the loader renames them positionally so the
#: frame has interpretable column names (#25 acceptance criterion).
_BANK_MARKETING_COLUMNS: tuple[str, ...] = (
    "age",
    "job",
    "marital",
    "education",
    "default",
    "balance",
    "housing",
    "loan",
    "contact",
    "day",
    "month",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
)


def fetch_wine_quality() -> pd.DataFrame:
    """Fetch the UCI Wine Quality dataset (red + white combined, H-0017 D5).

    Wrapper over :func:`sklearn.datasets.fetch_openml` that downloads the
    ``wine-quality-red`` (1,599 rows) and ``wine-quality-white`` (4,898
    rows) datasets, tags each with a ``color`` column, and concatenates
    them into a single frame (6,497 rows). The target column is
    normalised to ``quality`` regardless of the OpenML attribute name.

    Returns
    -------
    DataFrame
        6,497 rows × 13 columns (11 physicochemical features +
        ``quality`` target + ``color``).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Notes
    -----
    - First call downloads from OpenML to the sklearn cache.
    - ``color`` (``red`` / ``white``) is a useful explanatory variable
      for AIC-based EDA and a natural grouping for slice discovery.

    Examples
    --------
    >>> import pycatdap                              # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_wine_quality()  # doctest: +SKIP
    >>> df.shape                                     # doctest: +SKIP
    (6497, 13)
    """
    try:
        from sklearn.datasets import fetch_openml
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_wine_quality. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    frames = []
    for name, color in (("wine-quality-red", "red"), ("wine-quality-white", "white")):
        bundle = fetch_openml(name=name, version=1, as_frame=True)
        frame: pd.DataFrame = bundle.data.copy()
        frame["quality"] = bundle.target.to_numpy()
        frame["color"] = color
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def fetch_bank_marketing() -> pd.DataFrame:
    """Fetch the UCI Bank Marketing dataset (H-0017 D5).

    Wrapper over :func:`sklearn.datasets.fetch_openml` with
    ``name="bank-marketing"``. The OpenML release exposes the 16 features
    as generic ``V1``..``V16``; this loader renames them to the UCI names
    (``age``, ``job``, ``marital``, ...) and names the target ``y``. If a
    future OpenML version already ships interpretable names, the rename
    is skipped.

    Returns
    -------
    DataFrame
        45,211 rows × 17 columns (16 features + ``y`` target).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Notes
    -----
    - First call downloads from OpenML to the sklearn cache.
    - Classification target ``y`` (term-deposit subscription) makes this
      a good slice-discovery showcase.

    Examples
    --------
    >>> import pycatdap                                # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_bank_marketing()  # doctest: +SKIP
    >>> "age" in df.columns                            # doctest: +SKIP
    True
    """
    try:
        from sklearn.datasets import fetch_openml
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_bank_marketing. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    bundle = fetch_openml(name="bank-marketing", version=1, as_frame=True)
    frame: pd.DataFrame = bundle.data.copy()
    # Rename the generic OpenML V1..V16 columns positionally to UCI names.
    # A future OpenML version that already ships interpretable names is left
    # untouched (silent no-op). If the names are still generic but the count
    # no longer matches 16, we cannot rename safely — warn instead of
    # silently returning ``V1..V16`` (#25 wants interpretable columns).
    columns_are_generic = all(
        str(c).startswith("V") and str(c)[1:].isdigit() for c in frame.columns
    )
    if columns_are_generic and len(frame.columns) == len(_BANK_MARKETING_COLUMNS):
        frame.columns = pd.Index(_BANK_MARKETING_COLUMNS)
    elif columns_are_generic:
        warnings.warn(
            "fetch_bank_marketing: OpenML returned generic column names "
            f"({list(frame.columns)[:3]}...) but the count "
            f"({len(frame.columns)}) does not match the expected "
            f"{len(_BANK_MARKETING_COLUMNS)} UCI features; returning generic "
            "names unchanged.",
            stacklevel=2,
        )
    frame["y"] = bundle.target.to_numpy()
    return frame


def fetch_mushroom() -> pd.DataFrame:
    """Fetch the UCI Mushroom dataset (H-0017 D5).

    Wrapper over :func:`sklearn.datasets.fetch_openml` with
    ``name="mushroom"``. All 22 features and the ``class`` target
    (``e`` = edible / ``p`` = poisonous) are categorical, making this the
    canonical fully-categorical CATDAP demonstration dataset.

    Returns
    -------
    DataFrame
        8,124 rows × 23 columns (22 categorical features + ``class``
        target).

    Raises
    ------
    ImportError
        When ``scikit-learn`` is not installed. Install via
        ``pip install pycatdap[data]``.

    Notes
    -----
    - First call downloads from OpenML to the sklearn cache.
    - Every column is categorical, so ``catdap2`` can run with the
      default (all-categorical) pooling.

    Examples
    --------
    >>> import pycatdap                          # doctest: +SKIP
    >>> df = pycatdap.datasets.fetch_mushroom()  # doctest: +SKIP
    >>> "class" in df.columns                    # doctest: +SKIP
    True
    """
    try:
        from sklearn.datasets import fetch_openml
    except ImportError as exc:
        msg = (
            "scikit-learn is required for fetch_mushroom. "
            "Install with: pip install 'pycatdap[data]'"
        )
        raise ImportError(msg) from exc

    bundle = fetch_openml(name="mushroom", version=1, as_frame=True)
    df: pd.DataFrame = bundle.frame.copy()
    return df
