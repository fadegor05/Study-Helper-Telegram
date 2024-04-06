from uuid import uuid4
from datetime import datetime

from app.crud.lesson import get_lesson_by_uuid
from app.database import mongo_connection, mongo_get_collection


async def get_hometasks_all():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    return hometask_collection.find({})


async def get_hometask_by_uuid(hometask_uuid: str):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask = hometask_collection.find_one({'uuid': hometask_uuid})
    return hometask


async def create_hometask(lesson_uuid: str, task: str, date: datetime):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    lesson = await get_lesson_by_uuid(lesson_uuid)
    hometask_collection.insert_one({
        'uuid': uuid4(),
        'lesson_uuid': lesson_uuid,
        'lesson': lesson.get('name'),
        'task': task,
        'date': date,
        'is_completed': False
    })


async def change_hometask_status_by_uuid_and_user_id(hometask_uuid: str, user_id: int):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask = hometask_collection.find_one({'uuid': hometask_uuid})
    if user_id in hometask.get('completed_by'):
        hometask_collection.update_one({'uuid': hometask_uuid}, {'$pull': {'completed_by': user_id}})
    else:
        hometask_collection.update_one({'uuid': hometask_uuid}, {'$push': {'completed_by': user_id}})
