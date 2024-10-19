from datetime import datetime, timedelta

from aiogram_dialog import DialogManager

from app.crud.hometask import (
    get_hometask_by_uuid,
    get_hometasks_all_sorted,
    get_amount_hometasks_uncompleted,
    get_tomorrow_amount_hometasks_uncompleted,
)
from app.crud.lesson import get_lesson_by_uuid, get_lessons_all
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram.enums.content_type import ContentType

from app.crud.material import get_materials_by_lesson_uuid
from app.crud.schedule import get_lesson_weekdays_by_uuid
from app.crud.user import is_user_editor_by_telegram_id, get_user_by_telegram_id


async def get_hometasks(dialog_manager: DialogManager, **kwargs):
    user_id = int(dialog_manager.middleware_data.get("event_chat").id)
    is_editor = await is_user_editor_by_telegram_id(user_id)
    uncompleted_tasks_amount = await get_amount_hometasks_uncompleted(user_id)
    tomorrow_uncompleted_tasks_amount = await get_tomorrow_amount_hometasks_uncompleted(
        user_id
    )
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    hometasks = []
    for hometask in await get_hometasks_all_sorted(user_id):
        hometask_date = hometask.get("date")
        status_id = hometask.get("statuses").get(str(user_id))
        status = "⏳"
        if status_id is None and hometask_date.date() == tomorrow:
            status = "⭐"
        elif status_id == 0:
            status = "📦"
        elif status_id == 1:
            status = "✅"
        hometask.update(
            date=hometask_date.strftime("%d.%m"),
            status=status
        )
        hometasks.append(hometask)
    return {
        "hometasks": hometasks,
        "title_uncompleted_str": "📋 *Невыполненных заданий*\n"
        if uncompleted_tasks_amount
        else "*Вы выполнили все задания* 🎉\n",
        "tomorrow_uncompleted_amount_str": f"На завтра: {tomorrow_uncompleted_tasks_amount}\n"
        if tomorrow_uncompleted_tasks_amount > 0
        else "",
        "uncompleted_amount_str": f"Всего: {uncompleted_tasks_amount}\n"
        if uncompleted_tasks_amount > 0
        else "",
        "is_editor": is_editor,
    }


async def get_hometask(dialog_manager: DialogManager, **kwargs):
    hometask_uuid = dialog_manager.start_data.get("hometask_uuid")
    hometask = await get_hometask_by_uuid(hometask_uuid)
    user_id = dialog_manager.middleware_data.get("event_chat").id
    user = await get_user_by_telegram_id(user_id)
    author = await get_user_by_telegram_id(hometask.get("author_id"))
    is_editor = await is_user_editor_by_telegram_id(user_id)
    lesson = await get_lesson_by_uuid(hometask.get("lesson_uuid"))
    image_last = None
    if hometask.get("images") and len(hometask.get("images")) > 0:
        image_last = MediaAttachment(
            ContentType.PHOTO, file_id=MediaId(hometask.get("images")[-1])
        )
    completed_by_amount = sum(1 for v in hometask.get("statuses").values() if v == 1)
    editor_id = hometask.get("editor_id")
    edited_at = hometask.get("edited_at")
    edited_at_str = None
    editor = None
    if editor_id and edited_at:
        edited_at_str = edited_at.strftime("%d.%m %H:%M")
        editor = await get_user_by_telegram_id(editor_id)
    hometask_date = hometask.get("date").date()
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    is_completed = False
    status_id = hometask.get("statuses").get(str(user_id))
    status = "Не выполнено ⏳"
    status_button = "✅ Выполнено"
    skip_button = "📦 Пропустить"
    if status_id is None and hometask_date == tomorrow:
        status = "Рекомендуется ⭐"
    elif status_id == 0:
        status = "Пропущено 📦"
        skip_button = "⏳ Вернуть задание"
    elif status_id == 1:
        status = "Выполнено ✅"
        status_button = "❌ Отменить выполнение"
        is_completed = True

    materials = await get_materials_by_lesson_uuid(lesson.get("uuid"))
    materials_str = f"\n\n*Материалы* 📚\n" + "\n".join([f"[{material.get('name')}]({material.get('link')})" for material in materials]) if len(materials) > 0 else ""
    return {
        "lesson": hometask.get("lesson"),
        "status_str": status,
        "is_completed": is_completed,
        "status_button": status_button,
        "skip_button": skip_button,
        "task": hometask.get("task"),
        "date": hometask.get("date").strftime("%d.%m"),
        "image_last": image_last,
        "author_username": author.get("username"),
        "is_editor": is_editor,
        "completed_by_str": f"\n\n🏁 *Выполнили* {completed_by_amount}"
        if completed_by_amount > 0
        else "",
        "edited_str": f"\n✏️ *Изменено {edited_at_str}* @{editor.get('username')}"
        if editor_id and edited_at
        else "",
        "materials_str": materials_str,
    }


async def get_lessons(dialog_manager: DialogManager, **kwargs):
    lessons = await get_lessons_all()
    return {"lessons": lessons}


async def get_dates(dialog_manager: DialogManager, **kwargs):
    hometask_uuid = None
    if dialog_manager.start_data:
        hometask_uuid = dialog_manager.start_data.get("hometask_uuid")
    lesson_uuid = None
    if hometask_uuid:
        hometask = await get_hometask_by_uuid(hometask_uuid)
        lesson_uuid = hometask.get("lesson_uuid")
    else:
        lesson_uuid = dialog_manager.dialog_data.get("lesson_uuid")
    lesson_weekdays = await get_lesson_weekdays_by_uuid(lesson_uuid)
    dates = []
    now = datetime.now()
    start_datetime = datetime.combine(datetime.today(), datetime.min.time())
    end_datetime = start_datetime + timedelta(days=10)
    in_schedule = True
    if len(lesson_weekdays) == 0:
        in_schedule = False
    current_datetime = start_datetime
    while current_datetime <= end_datetime:
        if current_datetime.isoweekday() in lesson_weekdays or not in_schedule:
            dates.append(
                {
                    "date": current_datetime,
                    "date_iso": current_datetime.isoformat(),
                    "date_str": current_datetime.strftime("%d.%m"),
                }
            )
        current_datetime += timedelta(days=1)

    return {
        "dates": dates,
        "in_schedule": in_schedule,
    }


async def get_hometask_task(dialog_manager: DialogManager, **kwargs):
    hometask_uuid = dialog_manager.start_data.get("hometask_uuid")
    hometask = await get_hometask_by_uuid(hometask_uuid)
    return {"task": hometask.get("task")}


async def get_hometask_edited(dialog_manager: DialogManager, **kwargs):
    task = dialog_manager.dialog_data.get("task")
    return {"task": task}
