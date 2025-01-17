import requests
import datetime
import json

# Your WeatherAPI key
API_KEY = "29e3a4b1eef545bcb45194903243011"  # Replace with your actual API key
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_current_weather(location):

    params = {
        "key": API_KEY,
        "q": location,  # Location query (city name, zip code, or latitude/longitude)
    }   
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    location = "Lagos"
    weather = get_current_weather(location)
    
    if weather:
        print("\nCurrent Weather Statistics:")
        print(f"Location: {weather['location']['name']}, {weather['location']['country']}")
        print(f"Temperature: {weather['current']['temp_c']}°C / {weather['current']['temp_f']}°F")
        print(f"Condition: {weather['current']['condition']['text']}")
        print(f"Humidity: {weather['current']['humidity']}%")
        print(f"Wind Speed: {weather['current']['wind_kph']} kph / {weather['current']['wind_mph']} mph")
        print(f"Last Updated: {weather['current']['last_updated']}")
    else:
        print("Failed to retrieve weather data.")

    with open("new.json") as f:
        json.dumps(f, weather, indent = 1)
