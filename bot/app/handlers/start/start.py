from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from app.crud.user import create_user, user_exits_by_telegram_id, have_user_access_by_telegram_id
from app.dialogs.start.states import StartMenu
from app.handlers.router import router


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    if not await user_exits_by_telegram_id(int(message.from_user.id)):
        await create_user(int(message.from_user.id), message.from_user.username)
    if not await have_user_access_by_telegram_id(int(message.from_user.id)):
        await message.answer('*Упс...* К сожалению, у вас нет доступа к этом боту ⛔️️')
        return
    await dialog_manager.start(StartMenu.select_menu, mode=StartMode.RESET_STACK)

