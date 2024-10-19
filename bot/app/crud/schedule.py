from datetime import time

from app.database import mongo_connection, mongo_get_collection


async def is_schedule_filled():
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    return schedule_collection.count_documents({}) > 0


async def get_all_schedule():
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    return schedule_collection.find({})


async def get_all_schedule_sorted():
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    schedule = list(schedule_collection.find({}).sort({"day": 1}))
    return schedule


async def create_day_schedule(day: int, name: str, lessons: list):
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    schedule_collection.insert_one({"day": day, "name": name, "lessons": lessons})


async def get_day_schedule(day: int):
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    return schedule_collection.find_one({"day": day})


async def get_lesson_weekdays_by_uuid(lesson_uuid: str) -> list[int]:
    schedule = await get_all_schedule_sorted()
    lesson_weekdays = []
    for day in schedule:
        for _, lesson in day.get("lessons").items():
            if (
                    lesson.get("lesson_uuid") == lesson_uuid
                    and day.get("day") not in lesson_weekdays
            ):
                lesson_weekdays.append(day.get("day"))
    return lesson_weekdays


async def sync_schedule_with_lessons_crud():
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    lesson_collection = await mongo_get_collection(connection, "lessons")
    for schedule in schedule_collection.find():
        updated_lessons = schedule["lessons"]
        for n, lesson in schedule["lessons"]:
            lesson_uuid = lesson["lesson_uuid"]
            if lesson_uuid is not None:
                matching_lesson = lesson_collection.find_one({"uuid": lesson_uuid})
                if matching_lesson:
                    lesson["name"] = matching_lesson["name"]
                updated_lessons[n] = lesson
        schedule_collection.update_one(
            {"day": schedule["day"]}, {"$set": {"lessons": updated_lessons}}
        )


async def delete_schedule():
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    schedule_collection.delete_many({})


async def insert_schedule(schedule: list):
    connection = await mongo_connection()
    schedule_collection = await mongo_get_collection(connection, "schedule")
    schedule_collection.insert_many(schedule)


async def get_first_last_lesson_time_by_day(day: int) -> (time, time):
    day = await get_day_schedule(day)
    lessons = day.get("lessons")
    first = None
    for num, lesson in lessons.items():
        if lesson["lesson_uuid"] is not None:
            first = lesson
            break
    _, last = next(reversed(lessons.items()))
    return first.get("start_time").time(), last.get("end_time").time()
