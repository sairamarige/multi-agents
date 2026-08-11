"""Tool 6 (new): weather — current weather for a place name, via Open-Meteo
(open-meteo.com), a free API that needs no key. Two hops: geocode the place
name to lat/lon, then fetch current conditions for those coordinates.
Uses only the stdlib (urllib) so it adds no new dependency.

Note: this makes a real outbound network call, unlike every other tool in
this project. It's wrapped in the same timeout pattern as web_search for
the same reason — a stalled network call should degrade cleanly, not hang
the whole agent turn.
"""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# https://open-meteo.com/en/docs — WMO weather interpretation codes
_WEATHER_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "depositing rime fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    71: "slight snow", 73: "moderate snow", 75: "heavy snow",
    80: "slight rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    95: "thunderstorm", 96: "thunderstorm with slight hail", 99: "thunderstorm with heavy hail",
}


def _get_json(url: str, params: Dict[str, Any], timeout: int) -> dict:
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(full_url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_current_weather(location: str, timeout: int = 8) -> str:
    geo = _get_json(GEOCODE_URL, {"name": location, "count": 1}, timeout)
    results = geo.get("results") or []
    if not results:
        raise ValueError(f"Could not find a location matching '{location}'.")
    place = results[0]
    lat, lon = place["latitude"], place["longitude"]
    label = ", ".join(
        p for p in (place.get("name"), place.get("admin1"), place.get("country")) if p
    )

    forecast = _get_json(
        FORECAST_URL,
        {"latitude": lat, "longitude": lon, "current_weather": "true"},
        timeout,
    )
    current = forecast.get("current_weather")
    if not current:
        raise ValueError(f"No current weather data available for '{location}'.")

    condition = _WEATHER_CODES.get(current.get("weathercode"), "unknown conditions")
    return (
        f"{label}: {current['temperature']}°C, {condition}, "
        f"wind {current['windspeed']} km/h."
    )


def tool_weather(tool_input: Dict[str, Any], timeout: int = 8) -> str:
    location = tool_input.get("location", "")
    if not location:
        return "Weather error: no location given."
    try:
        return get_current_weather(location, timeout=timeout)
    except urllib.error.URLError as e:
        return f"Weather lookup failed (network error): {e}"
    except Exception as e:
        return f"Weather error: {e}"


SCHEMA = {
    "name": "weather",
    "description": (
        "Get the current weather for a named location (city, region, or "
        "country). Always use this for current weather instead of guessing."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "Place name, e.g. 'Hyderabad' or 'Tokyo, Japan'"}
        },
        "required": ["location"],
    },
}
