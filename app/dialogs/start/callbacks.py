from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from app.dialogs.hometask.states import HometaskMenu


async def on_chosen_menu(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(HometaskMenu.select_hometask)
