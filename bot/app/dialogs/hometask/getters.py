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

from app.crud.schedule import get_lesson_weekdays_by_uuid
from app.crud.user import is_user_editor_by_telegram_id, get_user_by_telegram_id


async def get_hometasks(dialog_manager: DialogManager, **kwargs):
    user_id = int(dialog_manager.middleware_data.get("event_chat").id)
    is_editor = await is_user_editor_by_telegram_id(user_id)
    uncompleted_tasks_amount = await get_amount_hometasks_uncompleted(user_id)
    tomorrow_uncompleted_tasks_amount = await get_tomorrow_amount_hometasks_uncompleted(
        user_id
    )
    hometasks = []
    for hometask in await get_hometasks_all_sorted(user_id):
        hometask.update(
            date=datetime.fromisoformat(hometask.get("date")).strftime("%d.%m"),
            is_completed="✅" if user_id in hometask.get("completed_by") else "⏳",
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
    books_list = lesson.get("books")
    books = (
        "\n".join([f"{book} - {books_list.get(book)}" for book in books_list])
        if books_list
        else "..."
    )
    is_completed = True if user_id in hometask.get("completed_by") else False
    image_last = None
    if hometask.get("images") and len(hometask.get("images")) > 0:
        image_last = MediaAttachment(
            ContentType.PHOTO, file_id=MediaId(hometask.get("images")[-1])
        )
    return {
        "lesson": hometask.get("lesson"),
        "is_completed": "Выполнено ✅" if is_completed else "Не выполнено ⏳",
        "is_completed_button": "✅ Выполнено"
        if not is_completed
        else "❌ Отменить выполнение",
        "task": hometask.get("task"),
        "date": datetime.fromisoformat(hometask.get("date")).strftime("%d.%m"),
        "books": books,
        "image_last": image_last,
        "author_username": author.get("username"),
        "is_editor": is_editor,
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
    start_datetime = datetime(now.year, now.month, now.day, 10, 0, 0)
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
