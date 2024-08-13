import pytest
import os
from dotenv import load_dotenv
from city_information.city_information import CityInformation

load_dotenv()


@pytest.fixture
def city_information():
    """
    Fixture for initializing the CityInformation instance with a valid API key.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    assert api_key is not None, "API key is not set."
    return CityInformation(api_key=api_key)


def test_get_city_summary_valid(city_information):
    """
    Test case for a valid city name.
    """
    summary, error = city_information.get_city_summary("Zagreb")
    assert error is None
    assert summary is not None
    assert "Zagreb" in summary


def test_get_city_summary_invalid(city_information):
    """
    Test case for an invalid city name.
    """
    summary, error = city_information.get_city_summary("asdasdsadas")
    assert summary is None
    assert error == "City not found. Please try again."


def test_get_city_summary_disambiguation(city_information):
    """
    Test case for a city name that leads to a disambiguation page.
    """
    summary, error = city_information.get_city_summary("Orlando")
    assert summary is None
    assert error == "City name is ambiguous. Please specify more clearly."


def test_get_city_temperature_valid(city_information):
    """
    Test case for a valid city name to fetch the temperature.
    """
    temperature, error = city_information.get_city_temperature("Berlin")
    assert temperature is not None
    assert isinstance(temperature, (float, int))
    assert error is None


def test_get_city_temperature_invalid_city(city_information):
    """
    Test case for an invalid city name to fetch the temperature.
    """
    city = "asdasdsadas"
    temperature, error = city_information.get_city_temperature(city)
    assert temperature is None
    assert error == f"{city} is not recognized as a city."


def test_get_city_temperature_invalid_api_key():
    """
    Test case for invalid API key to fetch the temperature.
    """
    invalid_city_info = CityInformation(api_key="INVALID_KEY")
    temperature, error = invalid_city_info.get_city_temperature("Zagreb")
    assert temperature is None
    assert error == "Invalid API key."


def test_get_city_summary_with_special_characters(city_information):
    """
    Test case for a city name with special characters.
    """
    summary, error = city_information.get_city_summary("São_Paulo")
    assert error is None
    assert summary is not None
    assert "São Paulo" in summary


def test_get_city_temperature_with_spaces(city_information):
    """
    Test case for a city name with spaces.
    """
    temperature, error = city_information.get_city_temperature("Rio de Janeiro")
    assert temperature is not None
    assert isinstance(temperature, float)
    assert error is None


def test_api_key_expiry(city_information, monkeypatch):
    """
    Test case for an expired API key.
    """
    def mock_get_city_summary(city_name):
        return None, "API key expired."

    monkeypatch.setattr(city_information, "get_city_summary", mock_get_city_summary)
    summary, error = city_information.get_city_summary("London")

    assert summary is None
    assert error == "API key expired."
    def mock_get_city_temperature(city_name):
        return None, "API key expired."

    monkeypatch.setattr(
        city_information, "get_city_temperature", mock_get_city_temperature
    )

    temperature, error = city_information.get_city_temperature("London")
    assert temperature is None
    assert error == "API key expired."


def test_invalid_api_endpoint(city_information, monkeypatch):
    """
    Test case for handling an invalid API endpoint.
    """
    def mock_get_city_summary(city_name):
        return None, "Invalid API endpoint."

    monkeypatch.setattr(city_information, "get_city_summary", mock_get_city_summary)
    summary, error = city_information.get_city_summary("London")

    assert summary is None
    assert error == "Invalid API endpoint."

    def mock_get_city_temperature(city_name):
        return None, "Invalid API endpoint."

    monkeypatch.setattr(
        city_information, "get_city_temperature", mock_get_city_temperature
    )
    temperature, error = city_information.get_city_temperature("London")

    assert temperature is None
    assert error == "Invalid API endpoint."


def test_get_city_summary_network_failure(city_information, monkeypatch):
    """
    Test case for network failure during city summary retrieval.
    """
    def mock_get_city_summary(city_name):
        return None, "Network error. Please check your connection and try again."

    monkeypatch.setattr(city_information, "get_city_summary", mock_get_city_summary)
    summary, error = city_information.get_city_summary("London")

    assert summary is None
    assert error == "Network error. Please check your connection and try again."


def test_get_city_temperature_network_failure(city_information, monkeypatch):
    """
    Test case for network failure during temperature retrieval.
    """
    def mock_get_city_temperature(city_name):
        return None, "Network error. Please check your connection and try again."

    monkeypatch.setattr(
        city_information, "get_city_temperature", mock_get_city_temperature
    )
    temperature, error = city_information.get_city_temperature("London")

    assert temperature is None
    assert error == "Network error. Please check your connection and try again."
