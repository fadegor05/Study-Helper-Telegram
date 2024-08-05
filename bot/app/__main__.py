import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from app.database import mongo_connection, mongo_init
from aiogram_dialog import setup_dialogs
from app.dialogs import get_dialogs
from app.handlers.router import router
from app.core.config import TELEGRAM_TOKEN, MONGO_DATABASE_NAME


async def main() -> None:
    connection = await mongo_connection()
    await mongo_init(connection)
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, *get_dialogs())
    setup_dialogs(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stopped')
