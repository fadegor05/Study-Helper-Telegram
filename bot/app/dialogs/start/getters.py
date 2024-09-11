from datetime import datetime

from aiogram_dialog import DialogManager

from app.crud.weather import get_weather


async def get_start(dialog_manager: DialogManager, **kwargs):
    weather = await get_weather()
    weather_str = ""
    if weather:
        date = datetime.fromisoformat(weather.get("date")).strftime("%d.%m")
        morning_time = datetime.fromisoformat(weather.get("morning_datetime")).strftime("%H:%M")
        day_time = datetime.fromisoformat(weather.get("day_datetime")).strftime("%H:%M")
        morning_icon = weather.get("morning_icon")
        day_icon = weather.get("day_icon")
        morning_temp = weather.get("morning_temperature")
        day_temp = weather.get("day_temperature")
        weather_str = f"\n\n*Погода на {date}* ☁️\nУтром в {morning_time}, {morning_temp}°C {morning_icon}\nДнем в {day_time}, {day_temp}°C {day_icon}"

    return {
        "weather_str": weather_str
    }