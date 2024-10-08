from datetime import datetime, timedelta

from app.database import mongo_connection, mongo_get_collection


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
        for lesson in day.get("lessons"):
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
        updated_lessons = []
        for lesson in schedule["lessons"]:
            lesson_uuid = lesson["lesson_uuid"]
            matching_lesson = lesson_collection.find_one({"uuid": lesson_uuid})
            if matching_lesson:
                lesson["name"] = matching_lesson["name"]
            updated_lessons.append(lesson)
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


async def get_first_last_lesson_datetime_by_day(day: int) -> (datetime, datetime):
    day = await get_day_schedule(day)
    lessons = day.get("lessons")
    return datetime.fromisoformat(lessons[0].get("start_time")), datetime.fromisoformat(lessons[-1].get("start_time"))+timedelta(minutes=40)

