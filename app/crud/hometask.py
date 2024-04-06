from uuid import uuid4
from datetime import datetime

from app.database import mongo_connection, mongo_get_collection


async def get_hometasks_all():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    return hometask_collection.find({})


async def create_hometask(lesson_uuid: int, task: str, date: datetime):
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, 'hometasks')
    hometask_collection.insert_one({
        'uuid': uuid4(),
        'lesson_uuid': lesson_uuid,
        'task': task,
        'date': date
    })
