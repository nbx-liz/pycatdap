"""Tests for bundled sample datasets."""

from __future__ import annotations

from pycatdap.datasets import load_health_data, load_hello_goodbye


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


class TestHelloGoodbye:
    """Tests for the HelloGoodbye dataset."""

    def test_shape(self) -> None:
        df = load_hello_goodbye()
        assert df.shape == (13954, 56)

    def test_response_column(self) -> None:
        df = load_hello_goodbye()
        assert "Isay" in df.columns
        assert set(df["Isay"].unique()) == {0, 1}

    def test_all_binary(self) -> None:
        df = load_hello_goodbye()
        for col in df.columns:
            assert set(df[col].unique()).issubset({0, 1}), f"{col} is not binary"
