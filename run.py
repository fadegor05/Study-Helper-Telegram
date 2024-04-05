import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from app.handlers.router import router
from app.core.config import TELEGRAM_TOKEN


async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stopped')