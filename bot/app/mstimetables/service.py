from typing import Dict, List, Any

from app.mstimetables.api import request_mstimetables
from app.mstimetables.utils import parse_classroom

days = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота'
}


async def get_schedule_from_mstimetables() -> list[dict[str, str | int | list[Any]] | None]:
    data = await request_mstimetables()
    if not data:
        return None
    kick_uuids = ('72', '73', '68', '5', '97', '20')
    lessons_data = sorted(data['lessons'], key=lambda x: x['lesson'])
    week = {}
    for i in range(1, 7):
        week[i] = None
    for lesson in lessons_data:
        if str(lesson['subject']['id']) not in kick_uuids:
            if week[lesson['weekday']] is None:
                week[lesson['weekday']] = {
                    'day': int(lesson['weekday']),
                    'name': days[int(lesson['weekday'])],
                    'lessons': []
                }
            classroom, building = '-', '-'
            if lesson['cabinet']:
                classroom, building = await parse_classroom(lesson['cabinet']['name'])
            week[lesson['weekday']]['lessons'].append({
                'lesson_uuid': str(lesson['subject']['id']),
                'name': lesson['subject']['name'],
                'building': building,
                'classroom': classroom,
                'start_time': f'2024-01-01T{lesson['startTime']}:00'
            })
    week = [week[key] for key in sorted(week.keys())]
    return week
