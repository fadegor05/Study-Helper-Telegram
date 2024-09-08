import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.triggers.cron import CronTrigger

from app.apsched.hometask import hometask_notification
from app.database import mongo_connection, mongo_init
from aiogram_dialog import setup_dialogs
from app.dialogs import get_dialogs
from app.handlers.router import router
from app.core.config import TELEGRAM_TOKEN, REDIS_URL
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main() -> None:
    connection = await mongo_connection()
    await mongo_init(connection)
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
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
