from datetime import datetime

from aiogram_dialog import DialogManager

from app.crud.schedule import get_all_schedule_sorted, get_day_schedule


async def get_schedule_day(dialog_manager: DialogManager, **kwargs):
    current_date = datetime.fromisoformat(dialog_manager.start_data.get("current_date"))
    schedule_day = await get_day_schedule(current_date.isoweekday())
    lessons = []
    for lesson in schedule_day.get("lessons"):
        if lesson["classroom"] and lesson["building"]:
            lesson.update(place=f'({lesson['classroom']})')
        else:
            lesson.update(place="")
        lesson.update(
            start_time=datetime.fromisoformat(lesson.get("start_time")).strftime(
                "%H:%M"
            )
        )
        lessons.append(lesson)
    schedule_day["lessons"] = lessons
    schedule_day["date_str"] = current_date.strftime("%d.%m")
    return schedule_day
