from typing import List
from uuid import uuid4
from datetime import datetime, timedelta

from app.crud.lesson import get_lesson_by_uuid
from app.database import mongo_connection, mongo_get_collection


async def get_amount_hometasks_uncompleted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    return hometask_collection.count_documents({'completed_by': {'$nin': [telegram_id]}})


async def get_tomorrow_amount_hometasks_uncompleted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    uncompleted_hometasks = hometask_collection.find({'completed_by': {'$nin': [telegram_id]}})
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    if tomorrow == 7:
        tomorrow += timedelta(days=1)
    tomorrow_uncompleted_hometaks = 0
    for hometask in uncompleted_hometasks:
        if datetime.fromisoformat(hometask.get('date')).date() == tomorrow:
            tomorrow_uncompleted_hometaks += 1
    return tomorrow_uncompleted_hometaks


async def get_hometasks_all_sorted(telegram_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    tomorrow = (datetime.today() + timedelta(days=1)).date()
    if tomorrow == 7:
        tomorrow += timedelta(days=1)
    uncompleted = list(hometask_collection.find({'completed_by': {'$nin': [telegram_id]}}).sort({'date': -1}))
    uncompleted.sort(key=lambda x: datetime.fromisoformat(x['date']).date() != tomorrow)
    completed = list(hometask_collection.find({'completed_by': {'$in': [telegram_id]}}).sort({'date': -1}))
    completed.sort(key=lambda x: datetime.fromisoformat(x['date']).date() != tomorrow)
    for hometask in completed:
        uncompleted.append(hometask)
    return uncompleted

async def update_hometask_task_by_uuid(hometask_uuid: str, task: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask_collection.update_one({'uuid': hometask_uuid}, {'$set': {'task': task}})

async def get_hometasks_all():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    return hometask_collection.find({})


async def get_hometask_by_uuid(hometask_uuid: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask = hometask_collection.find_one({'uuid': hometask_uuid})
    return hometask


async def create_hometask(lesson_uuid: str, task: str, date: datetime, images: List[str], author_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    lesson = await get_lesson_by_uuid(lesson_uuid)
    hometask_collection.insert_one({
        'uuid': str(uuid4()),
        'lesson_uuid': lesson_uuid,
        'lesson': lesson.get('name'),
        'task': task,
        'date': date,
        'completed_by': [],
        'images': images,
        'author_id': author_id
    })


async def change_hometask_status_by_uuid_and_user_id(hometask_uuid: str, user_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask = hometask_collection.find_one({'uuid': hometask_uuid})
    if user_id in hometask.get('completed_by'):
        hometask_collection.update_one({'uuid': hometask_uuid}, {'$pull': {'completed_by': user_id}})
    else:
        hometask_collection.update_one({'uuid': hometask_uuid}, {'$push': {'completed_by': user_id}})


async def sync_hometasks_with_lessons_crud():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    lesson_collection = await mongo_get_collection(connection, 'lessons')
    for hometask in hometask_collection.find({}):
        lesson_uuid = hometask["lesson_uuid"]
        matching_lesson = lesson_collection.find_one({"uuid": lesson_uuid})
        if matching_lesson:
            new_lesson_name = matching_lesson["name"]
            hometask_collection.update_one(
                {"uuid": hometask["uuid"]},
                {"$set": {"lesson": new_lesson_name}}
            )