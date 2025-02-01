# weather_utils.py
import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=36.175&longitude=-115.1372&current=temperature_2m&hourly=temperature_2m&temperature_unit=fahrenheit&wind_speed_unit=ms&precipitation_unit=inch&forecast_days=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['current']['temperature_2m']}°F"
    return "Weather data unavailable"