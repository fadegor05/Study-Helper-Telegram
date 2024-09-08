from datetime import datetime, timedelta
from typing import Dict

import requests

URL = "https://schedule.mstimetables.ru/api/publications/group/lessons"


async def request_mstimetables() -> Dict | None:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://schedule.mstimetables.ru",
        "referer": "https://schedule.mstimetables.ru/publications/97f594ce-2a64-4ca4-815a-494718acd9d3",
        "sec-ch-ua": "'Chromium';v='128', 'Not;A=Brand';v='24', 'Google Chrome';v='128'",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "'Android'",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
    }

    today = datetime.today()
    monday = today - timedelta(days=today.weekday())

    data = {
        "groupId": "58",
        "date": monday.strftime("%Y-%m-%d"),
        "publicationId": "97f594ce-2a64-4ca4-815a-494718acd9d3",
    }
    response = requests.post(URL, headers=headers, json=data)
    data = response.json()
    if not data["bells"]:
        return None
    return data
