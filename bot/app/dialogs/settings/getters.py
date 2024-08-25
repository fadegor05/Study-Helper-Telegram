from aiogram_dialog import DialogManager

from app.crud.user import get_user_by_telegram_id


async def get_settings(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.middleware_data.get('event_chat').id
    user = await get_user_by_telegram_id(user_id)
    return {
        'hometask_notification': '✅' if user.get('hometask_notification') else '❎',
        'schedule_notification': '✅' if user.get('schedule_notification') else '❎'
    }