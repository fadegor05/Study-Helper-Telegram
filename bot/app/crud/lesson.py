from typing import Dict
from uuid import uuid4

from app.database import mongo_connection, mongo_get_collection


async def get_lessons_all():
    connection = await mongo_connection()
    lesson_collection = await mongo_get_collection(connection, "lessons")
    return lesson_collection.find({})


async def create_lesson(
    name: str, classroom: str, building: int, books: Dict[str, str]
):
    connection = await mongo_connection()
    lesson_collection = await mongo_get_collection(connection, "lessons")
    lesson_collection.insert_one(
        {
            "uuid": str(uuid4()),
            "name": name,
            "classroom": classroom,
            "building": building,
            "books": books,
        }
    )


async def get_lesson_by_uuid(lesson_uuid: str):
    connection = await mongo_connection()
    lesson_collection = await mongo_get_collection(connection, "lessons")
    return lesson_collection.find_one({"uuid": lesson_uuid})


async def delete_lessons():
    connection = await mongo_connection()
    lesson_collection = await mongo_get_collection(connection, "lessons")
    lesson_collection.delete_many({})


async def insert_lessons(lessons: list):
    connection = await mongo_connection()
    lesson_collection = await mongo_get_collection(connection, "lessons")
    lesson_collection.insert_many(lessons)
