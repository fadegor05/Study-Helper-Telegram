from aiogram import Bot

from app.crud.user import get_all_users_with_schedule_notification


async def schedule_notification(bot: Bot):
    for user in await get_all_users_with_schedule_notification():
        telegram_id = user.get('telegram_id')
        await bot.send_message(telegram_id, f'Привет 👋\n\nРасписание было обновлено, советуем посмотреть на изменения 📆\n\nДанное сообщение можно отключить в настройках ⚙️')

