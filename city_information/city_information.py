import requests
import os


class CityInformation:
    """
    This class retrieves city information, including a summary and current temperature.
    """

    def __init__(self, api_key):
        """
        Initializes the CityInformation instance with an API key.

        Args:
            api_key (str): The API key for accessing the weather data.
        """
        if not api_key:
            raise ValueError("API key must be provided.")
        self.api_key = api_key

    def get_city_summary(self, city_name):
        """
        Fetches a summary of the specified city from Wikipedia.

        Args:
            city_name (str): The name of the city to retrieve the summary for.

        Returns:
            tuple: A tuple containing the city summary (str) and an error message (str) if any.
        """
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city_name}"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200 and "extract" in data:
                if data.get("type") == "disambiguation":
                    return None, "City name is ambiguous. Please specify more clearly."
                return data["extract"], None
            elif response.status_code == 404:
                return None, "City not found. Please try again."
            else:
                return None, f"Unexpected error: {data.get('detail', 'Unknown error')}"
        except Exception as e:
            return None, f"Error fetching city summary: {e}"

    def get_city_temperature(self, city_name):
        """
        Retrieves the current temperature for a given city using OpenWeatherMap API.

        Args:
            city_name (str): The name of the city to get the temperature for.

        Returns:
            tuple: A tuple containing the temperature (float) and an error message, if any.
        """
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city_name, "appid": self.api_key, "units": "metric"}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if response.status_code == 200:
                if data["sys"]["country"]:
                    return data["main"]["temp"], None
                else:
                    return None, "No temperature found."
            elif response.status_code == 401:
                return None, "Invalid API key."
            elif response.status_code == 404:
                return None, f"{city_name} is not recognized as a city."
            else:
                return None, f"Error: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return None, f"Error fetching temperature data: {e}"
