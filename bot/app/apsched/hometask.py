from aiogram import Bot

from app.crud.hometask import get_amount_hometasks_uncompleted, get_tomorrow_amount_hometasks_uncompleted
from app.crud.user import get_all_users_with_hometask_notification


async def hometask_notification(bot: Bot):
    for user in await get_all_users_with_hometask_notification():
        telegram_id = user.get('telegram_id')
        tomorrow_uncompleted_tasks = await get_tomorrow_amount_hometasks_uncompleted(telegram_id)
        if tomorrow_uncompleted_tasks > 0:
            await bot.send_message(telegram_id, f'*Привет* 👋\n\nЭто - напоминание о домашнем задании на завтра 📑\n\n📋 *Невыполненных заданий: {tomorrow_uncompleted_tasks}*\n\n_Данное сообщение можно отключить в настройках_ ⚙️')
