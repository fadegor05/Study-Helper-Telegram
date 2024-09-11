from datetime import datetime

from app.database import mongo_get_collection, mongo_connection


async def get_weather():
    connection = await mongo_connection()
    weather_collection = await mongo_get_collection(connection, "weather")
    return weather_collection.find_one({})


async def create_weather(date: datetime, morning_temp: float, day_temp: float, morning_icon: str, day_icon: str, morning_datetime: datetime, day_datetime: datetime):
    connection = await mongo_connection()
    weather_collection = await mongo_get_collection(connection, "weather")
    weather_collection.delete_many({})
    weather_collection.insert_one({
        "date": datetime.isoformat(date),
        "morning_temperature": morning_temp,
        "morning_icon": morning_icon,
        "morning_datetime": datetime.isoformat(morning_datetime),
        "day_temperature": day_temp,
        "day_icon": day_icon,
        "day_datetime": datetime.isoformat(day_datetime)
    })
