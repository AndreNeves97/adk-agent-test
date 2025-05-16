import datetime
import os
import requests
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenWeatherMap configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"


def get_weather(lat: float, long: float) -> dict:
    """Retrieves the current weather report for a specified latitude and longitude of some location. If only a location name is provided, use your knowledge to convert it to a latitude and longitude.

    Args:
        lat (float): The latitude of the location for which to retrieve the weather report.
        long (float): The longitude of the location for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if not OPENWEATHER_API_KEY:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key not configured. Please set OPENWEATHER_API_KEY environment variable."
        }

    try:
        params = {
            'lat': lat,
            'lon': long,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status()

        weather_data = response.json()
        temp_celsius = weather_data['main']['temp']
        temp_fahrenheit = (temp_celsius * 9/5) + 32
        weather_desc = weather_data['weather'][0]['description']

        return {
            "status": "success",
            "report": (
                f"The weather is {weather_desc} with a temperature of "
                f"{temp_celsius:.1f} degrees Celsius ({temp_fahrenheit:.1f} degrees Fahrenheit)."
            )
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {str(e)}"
        }


def get_coordinates(location: str) -> Dict[str, Any]:
    """Retrieves the latitude and longitude for a given location name using Nominatim API.

    Args:
        location (str): The name of the location to geocode.

    Returns:
        dict: status and result containing latitude and longitude or error message.
    """
    try:
        params = {
            'q': location,
            'format': 'json',
            'limit': 1,
            'accept-language': 'en'
        }
        headers = {
            'User-Agent': 'weather_time_agent/1.0'  # Required by Nominatim ToS
        }

        response = requests.get(
            NOMINATIM_BASE_URL, params=params, headers=headers)
        response.raise_for_status()

        results = response.json()

        if not results:
            return {
                "status": "error",
                "error_message": f"Could not find coordinates for location: {location}"
            }

        lat = float(results[0]['lat'])
        lon = float(results[0]['lon'])
        display_name = results[0]['display_name']

        return {
            "status": "success",
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "display_name": display_name
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch coordinates: {str(e)}"
        }


def get_location_from_coordinates(lat: float, long: float) -> Dict[str, Any]:
    """Retrieves the location name and details for given coordinates using Nominatim's reverse geocoding API.

    Args:
        lat (float): The latitude of the location.
        long (float): The longitude of the location.

    Returns:
        dict: status and result containing location details or error message.
    """
    try:
        params = {
            'lat': lat,
            'lon': long,
            'format': 'json',
            'accept-language': 'en'
        }
        headers = {
            'User-Agent': 'weather_time_agent/1.0'  # Required by Nominatim ToS
        }

        response = requests.get(
            NOMINATIM_REVERSE_URL, params=params, headers=headers)
        response.raise_for_status()

        result = response.json()

        if not result or 'error' in result:
            return {
                "status": "error",
                "error_message": f"Could not find location for coordinates: {lat}, {long}"
            }

        return {
            "status": "success",
            "location": {
                "display_name": result['display_name'],
                "address": result.get('address', {}),
                "type": result.get('type'),
                "class": result.get('class')
            }
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch location data: {str(e)}"
        }


def calculate_average_temperature(temperatures: list[float]) -> Dict[str, Any]:
    """Calculates the average temperature from a list of temperatures in Celsius.

    Args:
        temperatures (list[float]): List of temperatures in Celsius.

    Returns:
        dict: status and result containing average temperature in both Celsius and Fahrenheit.
    """
    if len(temperatures) < 2:
        return {
            "status": "error",
            "error_message": "At least two temperatures are required to calculate an average."
        }

    try:
        avg_temp_celsius = sum(temperatures) / len(temperatures)
        avg_temp_fahrenheit = (avg_temp_celsius * 9/5) + 32

        return {
            "status": "success",
            "result": {
                "average_temperature_celsius": round(avg_temp_celsius, 1),
                "average_temperature_fahrenheit": round(avg_temp_fahrenheit, 1),
                "number_of_temperatures": len(temperatures)
            }
        }
    except (TypeError, ValueError):
        return {
            "status": "error",
            "error_message": "All values in the list must be valid numbers."
        }


# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the current time.

#     Returns:
#         dict: status and result or error msg.
#     """

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the weather in a location."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the weather in a location."
    ),
    tools=[get_weather, get_coordinates,
           get_location_from_coordinates, calculate_average_temperature],
)
