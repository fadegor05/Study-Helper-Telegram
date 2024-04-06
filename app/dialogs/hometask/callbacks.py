from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button


async def on_chosen_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, hometask_uuid: str, **kwargs):
    print(hometask_uuid)
