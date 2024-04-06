from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.hometask import change_hometask_status_by_uuid_and_user_id
from app.dialogs.hometask.states import HometaskInfo


async def on_chosen_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, hometask_uuid: str, **kwargs):
    await manager.start(HometaskInfo.info_hometask, {'hometask_uuid': hometask_uuid})


async def change_hometask_status(c: CallbackQuery, widget: Button, manager: DialogManager):
    hometask_uuid = manager.start_data.get('hometask_uuid')
    user_id = manager.middleware_data.get('event_chat').id
    await change_hometask_status_by_uuid_and_user_id(hometask_uuid, user_id)
