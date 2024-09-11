import datetime
from typing import Dict

import requests

URL = "https://api.open-meteo.com/v1/forecast"

async def request_openmeteo(date: datetime.datetime) -> Dict | None:
    date_str = date.strftime("%Y-%m-%d")
    query = {
        "latitude": "53.2448",
        "longitude": "50.177726",
        "hourly": "temperature_2m,weather_code",
        "timezone": "auto",
        "start_date": date_str,
        "end_date": date_str
    }
    response = requests.get(URL, query)
    data = response.json()
    return data
