from datetime import datetime

from aiogram_dialog import DialogManager

from app.crud.schedule import get_all_schedule_sorted, get_day_schedule


async def get_schedule(dialog_manager: DialogManager, **kwargs):
    schedule = await get_all_schedule_sorted()
    return {"schedule": schedule}


async def get_schedule_day(dialog_manager: DialogManager, **kwargs):
    day = int(dialog_manager.start_data.get("schedule_day"))
    schedule_day = await get_day_schedule(day)
    lessons = []
    for lesson in schedule_day.get("lessons"):
        if lesson["classroom"] and lesson["building"]:
            lesson.update(place=f'({lesson['classroom']},{lesson['building']} корпус)')
        else:
            lesson.update(place="")
        lesson.update(
            start_time=datetime.fromisoformat(lesson.get("start_time")).strftime(
                "%H:%M"
            )
        )
        lessons.append(lesson)
    schedule_day["lessons"] = lessons
    return schedule_day
