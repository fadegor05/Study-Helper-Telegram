from datetime import datetime

from aiogram_dialog import DialogManager

from app.crud.hometask import get_hometask_by_lesson_uuid_and_date
from app.crud.schedule import get_day_schedule


async def get_schedule_day(dialog_manager: DialogManager, **kwargs):
    current_date = datetime.fromisoformat(dialog_manager.start_data.get("current_date"))
    schedule_day = await get_day_schedule(current_date.isoweekday())
    lessons = []
    for _, lesson in schedule_day.get("lessons").items():
        if lesson["lesson_uuid"] is None:
            lesson["lesson_str"] = "🚫"
            lessons.append(lesson)
        else:
            user_id = int(dialog_manager.middleware_data.get("event_chat").id)
            hometask_str = ""
            hometask = await get_hometask_by_lesson_uuid_and_date(lesson["lesson_uuid"], current_date.date())
            if hometask:
                status_id = hometask.get("statuses").get(str(user_id))
                hometask_str = "⏳"
                if status_id == 0:
                    hometask_str = "📦"
                elif status_id == 1:
                    hometask_str = "✅"
            place_str = ""
            if lesson["classroom"] and lesson["building"]:
                place_str = f"({lesson['classroom']})"
            start_time = lesson.get("start_time").strftime(
                "%H:%M"
            )
            lesson["lesson_str"] = f"{hometask_str} {start_time} {lesson['name']} {place_str}"
            lessons.append(lesson)
    schedule_day["lessons"] = lessons
    schedule_day["date_str"] = current_date.strftime("%d.%m")
    return schedule_day
