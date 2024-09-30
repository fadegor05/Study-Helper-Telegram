from typing import List
from uuid import uuid4
from datetime import datetime, timedelta

from app.crud.lesson import get_lesson_by_uuid
from app.database import mongo_connection, mongo_get_collection


# Statuses
# Nothing - Not completed
# 0 - Skipped
# 1 - Completed

async def get_amount_hometasks_uncompleted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    return hometask_collection.count_documents(
        {
            f"statuses.{telegram_id}": {"$exists": False},
            "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}],
        }
    )


async def get_tomorrow_amount_hometasks_uncompleted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    uncompleted_hometasks = hometask_collection.find(
        {
            f"statuses.{telegram_id}": {"$exists": False},
            "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}],
        }
    )
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    if tomorrow == 7:
        tomorrow += timedelta(days=1)
    tomorrow_uncompleted_hometaks = 0
    for hometask in uncompleted_hometasks:
        if datetime.fromisoformat(hometask.get("date")).date() == tomorrow:
            tomorrow_uncompleted_hometaks += 1
    return tomorrow_uncompleted_hometaks


async def get_hometasks_all_sorted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")

    tomorrow = (datetime.today() + timedelta(days=1)).date()

    uncompleted = list(
        hometask_collection.find(
            {
                f"statuses.{telegram_id}": {"$exists": False},
                "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}],
            }
        )
    )

    completed = list(
        hometask_collection.find(
            {
                f"statuses.{telegram_id}": 1,
                "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}],
            }
        )
    )

    skipped = list(
        hometask_collection.find(
            {
                f"statuses.{telegram_id}": 0,
                "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}],
            }
        )
    )

    def custom_sort(hometask):
        task_date = datetime.fromisoformat(hometask["date"]).date()
        if task_date >= tomorrow:
            return (0, task_date)
        else:
            return (1, -task_date.toordinal())

    uncompleted.sort(key=custom_sort)
    completed.sort(key=custom_sort)
    skipped.sort(key=custom_sort)

    sorted_hometasks = uncompleted + completed + skipped

    return sorted_hometasks


async def update_hometask_task_by_uuid(hometask_uuid: str, task: str, editor_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    now = datetime.now() + timedelta(hours=1)
    hometask_collection.update_one(
        {"uuid": hometask_uuid},
        {"$set": {"task": task, "edited_at": now.isoformat(), "editor_id": editor_id, "statuses": {}}},
    )


async def update_hometask_date_by_uuid(hometask_uuid: str, date: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask_collection.update_one({"uuid": hometask_uuid}, {"$set": {"date": date, "statuses": {}}})


async def get_hometasks_all():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    return hometask_collection.find({})


async def get_hometask_by_lesson_uuid_and_datetime(lesson_uuid: str, date: datetime):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    formatted_date = date.strftime("%Y-%m-%d")
    hometask_date = datetime.fromisoformat(f"{formatted_date}T10:00:00")
    hometasks = hometask_collection.find_one({"lesson_uuid": lesson_uuid, "date": hometask_date.isoformat(),
                                              "$or": [{"is_hidden": {"$exists": False}}, {"is_hidden": False}]})
    return hometasks


async def get_hometask_by_uuid(hometask_uuid: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask = hometask_collection.find_one({"uuid": hometask_uuid})
    return hometask


async def hide_hometask_by_uuid(hometask_uuid: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask_collection.update_one(
        {"uuid": hometask_uuid}, {"$set": {"is_hidden": True}}
    )


async def create_hometask(
        lesson_uuid: str, task: str, date: datetime, images: List[str], author_id: int
):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    lesson = await get_lesson_by_uuid(lesson_uuid)
    hometask_collection.insert_one(
        {
            "uuid": str(uuid4()),
            "lesson_uuid": lesson_uuid,
            "lesson": lesson.get("name"),
            "task": task,
            "date": date,
            "statuses": {},
            "images": images,
            "author_id": author_id,
        }
    )


async def skip_hometask_by_uuid_and_telegram_uuid(hometask_uuid: str, telegram_uuid: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask = hometask_collection.find_one({"uuid": hometask_uuid})
    hometask_collection.update_one(
        {"uuid": hometask_uuid}, {"$set": {f"statuses.{telegram_uuid}": 0}}
    )

async def complete_hometask_by_uuid_and_telegram_uuid(hometask_uuid: str, telegram_uuid: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask = hometask_collection.find_one({"uuid": hometask_uuid})
    hometask_collection.update_one(
        {"uuid": hometask_uuid}, {"$set": {f"statuses.{telegram_uuid}": 1}}
    )

async def uncomplete_hometask_by_uuid_and_telegram_uuid(hometask_uuid: str, telegram_uuid: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    hometask = hometask_collection.find_one({"uuid": hometask_uuid})
    hometask_collection.update_one(
        {"uuid": hometask_uuid}, {"$unset": {f"statuses.{telegram_uuid}": ""}}
    )


async def sync_hometasks_with_lessons_crud():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")
    lesson_collection = await mongo_get_collection(connection, "lessons")
    for hometask in hometask_collection.find({}):
        lesson_uuid = hometask["lesson_uuid"]
        matching_lesson = lesson_collection.find_one({"uuid": lesson_uuid})
        if matching_lesson:
            new_lesson_name = matching_lesson["name"]
            hometask_collection.update_one(
                {"uuid": hometask["uuid"]}, {"$set": {"lesson": new_lesson_name}}
            )
