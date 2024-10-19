from datetime import datetime

from aiogram_dialog import DialogManager

from app.crud.weather import get_weather


async def get_start(dialog_manager: DialogManager, **kwargs):
    weather = await get_weather()
    weather_str = ""
    if weather:
        date_str = weather.get("date").strftime("%d.%m")
        morning_time_str = weather.get("morning_time").strftime("%H:%M")
        day_time_str = weather.get("day_time").strftime("%H:%M")
        morning_icon = weather.get("morning_icon")
        day_icon = weather.get("day_icon")
        morning_temp = weather.get("morning_temperature")
        day_temp = weather.get("day_temperature")
        weather_str = f"\n\n*Погода на {date_str}* ☁️\nУтром в {morning_time_str}, {morning_temp}°C {morning_icon}\nДнем в {day_time_str}, {day_temp}°C {day_icon}"

    return {
        "weather_str": weather_str
    }