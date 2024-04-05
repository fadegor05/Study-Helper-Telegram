from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from app.dialogs.start.states import StartMenu
from app.handlers.router import router


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(StartMenu.select_menu, mode=StartMode.RESET_STACK)
