import pytest
import requests
import os
from main import main
from dotenv import load_dotenv
from unittest.mock import patch, mock_open
from city_information.city_information import CityInformation

load_dotenv()


@pytest.fixture
def city_information():
    """
    Loading the api key as a fixture for tests.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    assert api_key is not None, "API key is not set."
    return CityInformation(api_key=api_key)


@patch("requests.get")
def test_get_city_summary_unexpected_error(mock_get, city_information):
    """
    This test handles the 500 status code return.
    """
    city_name = "TestCity1"

    mock_response = requests.Response()
    mock_response.status_code = 500
    mock_response._content = b'{"detail": "Something went wrong."}'
    mock_get.return_value = mock_response

    summary, error = city_information.get_city_summary(city_name)

    assert summary is None
    assert error == "Unexpected error: Something went wrong."


@patch("requests.get")
def test_get_city_summary_unexpected_error_without_detail(mock_get, city_information):
    """
    This test handles the 403 status code return.
    """
    city_name = "TestCity2"

    mock_response = requests.Response()
    mock_response.status_code = 403
    mock_response._content = b"{}"  # This is an empty JSON bytes response
    mock_get.return_value = mock_response

    summary, error = city_information.get_city_summary(city_name)

    assert summary is None
    assert error == "Unexpected error: Unknown error"


@patch("builtins.input", return_value="InvalidCity")
@patch("city_information.city_information.CityInformation.get_city_temperature")
@patch("builtins.print")
def test_main_invalid_city(mock_print, mock_get_city_temperature, mock_input):
    """
    Test handling of invalid city name with temperature check.
    """
    mock_get_city_temperature.return_value = (
        None,
        "Input is not recognized as a city..",
    )

    main()

    mock_print.assert_called_once_with("Input is not recognized as a city..")


@patch("builtins.input", return_value="DisambiguationCity")
@patch("city_information.city_information.CityInformation.get_city_temperature")
@patch("city_information.city_information.CityInformation.get_city_summary")
@patch("builtins.print")
def test_main_ambiguous_city(
    mock_print, mock_get_city_summary, mock_get_city_temperature, mock_input
):
    """
    Test handling of ambiguous city name with summary check.
    """
    mock_get_city_temperature.return_value = (20.0, None)

    mock_get_city_summary.return_value = (
        None,
        "City name is ambiguous. Please specify more clearly.",
    )

    main()

    mock_print.assert_called_once_with(
        "City name is ambiguous. Please specify more clearly."
    )


@patch("builtins.input", return_value="London")
@patch("city_information.city_information.CityInformation.get_city_temperature")
@patch("city_information.city_information.CityInformation.get_city_summary")
@patch("builtins.open", new_callable=mock_open)
@patch("builtins.print")
def test_main_valid_city(
    mock_print,
    mock_open_file,
    mock_get_city_summary,
    mock_get_city_temperature,
    mock_input,
):
    """
    Positive test for valid city name.
    """
    mock_get_city_temperature.return_value = (15.0, None)

    mock_get_city_summary.return_value = (
        "London is the capital city of England.",
        None,
    )

    main()

    expected_output = (
        "London is the capital city of England.\n\n"
        "Current temperature in London is 15.00 degrees Celsius."
    )

    # Verify that the open function was called twice (once for .env, once for the file)
    assert mock_open_file.call_count == 2

    # Assert that the second call to open was for writing the file
    mock_open_file.assert_any_call("london.txt", "w", encoding="utf-8")

    # Assert that the output is written to a file correctly
    handle = mock_open_file()
    handle.write.assert_called_once_with(expected_output)

    # Assert that success message is printed
    mock_print.assert_called_once_with("Data successfully written to london.txt")


@patch("requests.get")
def test_get_city_summary_valid_city(mock_get, city_information):
    """
    Positive test for valid city summary fetch.
    """
    city_name = "New York"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"extract": "New York is a major city in the USA."}'
    mock_get.return_value = mock_response

    summary, error = city_information.get_city_summary(city_name)

    assert summary == "New York is a major city in the USA."
    assert error is None


@patch("requests.get")
def test_get_city_temperature_valid_city(mock_get, city_information):
    """
    Positive test for valid city temperature fetch.
    """
    city_name = "Tokyo"

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"main": {"temp": 26.5}, "sys": {"country": "JP"}}'
    mock_get.return_value = mock_response

    temperature, error = city_information.get_city_temperature(city_name)

    assert temperature == 26.5
    assert error is None
