import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.triggers.cron import CronTrigger

from app.apsched.hometask import hometask_notification
from app.apsched.weather import update_weather
from app.crud.schedule import delete_schedule, insert_schedule, is_schedule_filled
from app.database import mongo_connection, mongo_init
from aiogram_dialog import setup_dialogs
from app.dialogs import get_dialogs
from app.handlers.router import router
from app.core.config import TELEGRAM_TOKEN, REDIS_URL
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.migrations.migrations import mongo_migrate
from app.mstimetables.service import get_schedule_from_mstimetables
from app.openmeteo.service import update_weather_from_openmeteo


async def main() -> None:
    connection = await mongo_connection()
    await mongo_init(connection)

    await mongo_migrate()

    if not await is_schedule_filled():
        schedule = await get_schedule_from_mstimetables()
        if schedule:
            await delete_schedule()
            await insert_schedule(schedule)

    storage = RedisStorage.from_url(REDIS_URL)
    storage.key_builder.with_destiny = True

    defaults = DefaultBotProperties(parse_mode="Markdown")
    bot = Bot(token=TELEGRAM_TOKEN, default=defaults)
    dp = Dispatcher(storage=storage)
    dp.include_routers(router, *get_dialogs())
    setup_dialogs(dp)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        hometask_notification,
        trigger=CronTrigger(day_of_week="0-4,6", hour=16, minute=0),
        kwargs={"bot": bot},
    )
    scheduler.add_job(
        update_weather,
        trigger=CronTrigger(hour=16, minute=5),
    )
    scheduler.start()

    await update_weather_from_openmeteo()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
