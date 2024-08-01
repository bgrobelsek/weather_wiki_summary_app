import os
from city_information.city_information import CityInformation
from city_information.utils import style_summary
from dotenv import load_dotenv


def main():
    """
    This is the main entry point for the application.

    - Loads environment variables from .env file.
    - Retrieves the OpenWeather API key.
    - Prompts the user for a city name.
    - Fetches and displays a city summary and current temperature.
    - Saves the data to a file named <city_name>.txt.
    """

    load_dotenv()
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

    if not openweather_api_key:
        print(
            "Error: OpenWeather API key not found. Please set the OPENWEATHER_API_KEY environment variable."
        )
        return

    input_city_name = input("Enter the city name: ").strip()
    city_name = input_city_name.lower()
    city_info = CityInformation(api_key=openweather_api_key)

    # First, check the temperature to validate the city name
    temperature, temp_error = city_info.get_city_temperature(city_name)
    if temp_error:
        print(temp_error)
        return

    # Fetch city summary only if temperature check passed
    summary, summary_error = city_info.get_city_summary(city_name)
    if summary_error:
        print(summary_error)
        return

    styled_summary = style_summary(summary) if summary else None

    if styled_summary and temperature is not None:
        city_name_capitalized = (input_city_name).capitalize()
        output_text = (
            f"{styled_summary}\n\n"
            f"Current temperature in {city_name_capitalized} is {temperature:.2f} degrees Celsius."
        )
        file_name = f"{city_name}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(output_text)
        print(f"Data successfully written to {file_name}")
    else:
        print("Failed to retrieve complete city data.")


if __name__ == "__main__":
    main()
