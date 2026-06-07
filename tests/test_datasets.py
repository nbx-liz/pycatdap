"""Tests for bundled sample datasets."""

from __future__ import annotations

from pycatdap.datasets import (
    load_german_credit,
    load_health_data,
    load_heart_disease,
    load_iris,
    load_penguins,
    load_titanic,
)


class TestHealthData:
    """Tests for the HealthData dataset."""

    def test_shape(self) -> None:
        df = load_health_data()
        assert df.shape == (52, 8)

    def test_columns(self) -> None:
        df = load_health_data()
        expected = [
            "opthalmo.",
            "ecg",
            "symptoms",
            "age",
            "max.press",
            "min.press",
            "aortic.wav",
            "cholesterol",
        ]
        assert list(df.columns) == expected

    def test_symptoms_values(self) -> None:
        df = load_health_data()
        assert set(df["symptoms"].unique()) == {"A", "B"}

    def test_cholesterol_values(self) -> None:
        df = load_health_data()
        assert set(df["cholesterol"].unique()) == {"low", "high"}

    def test_no_missing_values(self) -> None:
        df = load_health_data()
        assert not df.isnull().any().any()

    def test_returns_copy(self) -> None:
        """Each call should return a fresh DataFrame."""
        df1 = load_health_data()
        df2 = load_health_data()
        assert df1 is not df2


class TestTitanic:
    """Tests for the Titanic dataset (R datasets::Titanic expanded form)."""

    def test_shape(self) -> None:
        df = load_titanic()
        assert df.shape == (2201, 4)

    def test_columns(self) -> None:
        df = load_titanic()
        assert list(df.columns) == ["Class", "Sex", "Age", "Survived"]

    def test_class_values(self) -> None:
        df = load_titanic()
        assert set(df["Class"].unique()) == {"1st", "2nd", "3rd", "Crew"}

    def test_sex_values(self) -> None:
        df = load_titanic()
        assert set(df["Sex"].unique()) == {"Male", "Female"}

    def test_age_values(self) -> None:
        df = load_titanic()
        assert set(df["Age"].unique()) == {"Adult", "Child"}

    def test_survived_values(self) -> None:
        df = load_titanic()
        assert set(df["Survived"].unique()) == {"Yes", "No"}

    def test_class_counts_match_r(self) -> None:
        """Marginal counts must match R datasets::Titanic margin sums."""
        df = load_titanic()
        counts = df["Class"].value_counts().to_dict()
        # From R: 1st=325, 2nd=285, 3rd=706, Crew=885
        assert counts == {"1st": 325, "2nd": 285, "3rd": 706, "Crew": 885}

    def test_no_missing_values(self) -> None:
        df = load_titanic()
        assert not df.isnull().any().any()


class TestIris:
    """Tests for Fisher's iris dataset."""

    def test_shape(self) -> None:
        df = load_iris()
        assert df.shape == (150, 5)

    def test_columns(self) -> None:
        df = load_iris()
        assert list(df.columns) == [
            "Sepal.Length",
            "Sepal.Width",
            "Petal.Length",
            "Petal.Width",
            "Species",
        ]

    def test_species_balanced(self) -> None:
        df = load_iris()
        counts = df["Species"].value_counts().to_dict()
        assert counts == {"setosa": 50, "versicolor": 50, "virginica": 50}

    def test_continuous_columns_are_float(self) -> None:
        df = load_iris()
        for col in ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"]:
            assert df[col].dtype.kind == "f", f"{col} is not float"

    def test_no_missing_values(self) -> None:
        df = load_iris()
        assert not df.isnull().any().any()

    def test_sepal_length_range(self) -> None:
        """Known canonical range: 4.3 to 7.9 cm."""
        df = load_iris()
        assert df["Sepal.Length"].min() == 4.3
        assert df["Sepal.Length"].max() == 7.9


class TestGermanCredit:
    """Tests for the Statlog German Credit dataset (D3, v0.7.0 H-0010)."""

    def test_shape(self) -> None:
        df = load_german_credit()
        assert df.shape == (1000, 21)

    def test_class_column(self) -> None:
        df = load_german_credit()
        assert "class" in df.columns
        assert set(df["class"].unique()) == {"good", "bad"}

    def test_class_balance(self) -> None:
        df = load_german_credit()
        counts = df["class"].value_counts().to_dict()
        assert counts == {"good": 700, "bad": 300}

    def test_mixed_dtypes(self) -> None:
        import pandas as pd

        df = load_german_credit()
        n_str = sum(pd.api.types.is_string_dtype(df[c]) for c in df.columns)
        n_num = sum(df[c].dtype.kind in ("i", "f") for c in df.columns)
        assert n_str >= 10
        assert n_num >= 4


class TestHeartDisease:
    """Tests for the Cleveland Heart Disease dataset (D3, v0.7.0 H-0010)."""

    def test_shape(self) -> None:
        df = load_heart_disease()
        assert df.shape == (303, 14)

    def test_target_column(self) -> None:
        df = load_heart_disease()
        assert "target" in df.columns
        assert set(df["target"].dropna().unique()).issubset({0.0, 1.0})

    def test_all_numeric_columns(self) -> None:
        df = load_heart_disease()
        for col in df.columns:
            assert df[col].dtype.kind in ("i", "f"), f"{col} is not numeric"


class TestPenguins:
    """Tests for the Palmer Penguins dataset (D3, v0.7.0 H-0010)."""

    def test_shape(self) -> None:
        df = load_penguins()
        assert df.shape == (344, 7)

    def test_species_three_classes(self) -> None:
        df = load_penguins()
        assert set(df["species"].unique()) == {"Adelie", "Chinstrap", "Gentoo"}

    def test_island_categorical(self) -> None:
        df = load_penguins()
        assert set(df["island"].unique()) == {"Torgersen", "Biscoe", "Dream"}

    def test_morphological_columns_are_float(self) -> None:
        df = load_penguins()
        for col in (
            "culmen_length_mm",
            "culmen_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ):
            assert df[col].dtype.kind == "f", f"{col} is not float"
