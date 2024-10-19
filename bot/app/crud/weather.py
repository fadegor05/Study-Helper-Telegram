from datetime import datetime, date, time

from app.database import mongo_get_collection, mongo_connection


async def get_weather():
    connection = await mongo_connection()
    weather_collection = await mongo_get_collection(connection, "weather")
    weather_data = weather_collection.find_one({})
    if weather_data:
        weather_data['date'] = weather_data['date'].date()
        weather_data['morning_time'] = weather_data['morning_time'].time()
        weather_data['day_time'] = weather_data['day_time'].time()
    return weather_data


async def create_weather(day_date: date, morning_temp: float, day_temp: float, morning_icon: str, day_icon: str, morning_time: time, day_time: time):
    connection = await mongo_connection()
    weather_collection = await mongo_get_collection(connection, "weather")
    weather_collection.delete_many({})
    weather_collection.insert_one({
        "date": datetime.combine(day_date, datetime.min.time()),
        "morning_temperature": morning_temp,
        "morning_icon": morning_icon,
        "morning_time": datetime.combine(datetime.min.date(), morning_time),
        "day_temperature": day_temp,
        "day_icon": day_icon,
        "day_time": datetime.combine(datetime.min.date(), day_time)
    })
