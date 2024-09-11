from app.openmeteo.service import update_weather_from_openmeteo


async def update_weather():
    await update_weather_from_openmeteo()