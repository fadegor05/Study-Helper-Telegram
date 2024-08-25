from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.crud.user import get_user_by_telegram_id, set_hometask_notification_by_telegram_id, \
    set_schedule_notification_by_telegram_id


async def on_chosen_schedule_notification(c: CallbackQuery, widget: Button, manager: DialogManager):
    user_id = manager.middleware_data.get('event_chat').id
    user = await get_user_by_telegram_id(user_id)
    await set_schedule_notification_by_telegram_id(user_id, not user.get('schedule_notification'))


async def on_chosen_hometask_notification(c: CallbackQuery, widget: Button, manager: DialogManager):
    user_id = manager.middleware_data.get('event_chat').id
    user = await get_user_by_telegram_id(user_id)
    await set_hometask_notification_by_telegram_id(user_id, not user.get('hometask_notification'))
