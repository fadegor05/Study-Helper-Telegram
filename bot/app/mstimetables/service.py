from typing import Any

from app.mstimetables.api import request_mstimetables
from app.mstimetables.utils import parse_classroom

DAYS = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
}

KICK_UUIDS = ("72", "73", "68", "5", "97", "20")


async def get_lessons_from_mstimetables() -> list | None:
    data = await request_mstimetables()
    if not data:
        return None
    lessons_data = data["lessons"]
    lessons = []
    lesson_uuids = []
    for lesson in lessons_data:
        if (
            lesson["subject"]["id"] not in lesson_uuids
            and str(lesson["subject"]["id"]) not in KICK_UUIDS
        ):
            lesson_uuids.append(lesson["subject"]["id"])
            lessons.append(
                {
                    "uuid": str(lesson["subject"]["id"]),
                    "name": lesson["subject"]["name"],
                }
            )
    return lessons


async def get_schedule_from_mstimetables() -> (
    list[dict[str, str | int | list[Any]] | None]
):
    data = await request_mstimetables()
    if not data:
        return None
    lessons_data = sorted(data["lessons"], key=lambda x: x["lesson"])
    week = {}
    for i in range(1, 7):
        week[i] = None
    for lesson in lessons_data:
        if str(lesson["subject"]["id"]) not in KICK_UUIDS:
            if week[lesson["weekday"]] is None:
                week[lesson["weekday"]] = {
                    "day": int(lesson["weekday"]),
                    "name": DAYS[int(lesson["weekday"])],
                    "lessons": [],
                }
            classroom, building = None, None
            if lesson["cabinet"]:
                classroom, building = await parse_classroom(lesson["cabinet"]["name"])
            week[lesson["weekday"]]["lessons"].append(
                {
                    "lesson_uuid": str(lesson["subject"]["id"]),
                    "name": lesson["subject"]["name"],
                    "building": building,
                    "classroom": classroom,
                    "start_time": f'2024-01-01T{lesson['startTime']}:00',
                }
            )
    week = [week[key] for key in sorted(week.keys())]
    return week
