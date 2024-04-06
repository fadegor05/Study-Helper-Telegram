from aiogram_dialog import DialogManager

from app.crud.hometask import get_hometasks_all


async def get_hometasks(dialog_manager: DialogManager, **kwargs):
    hometasks = await get_hometasks_all()
    return {
        'hometasks': hometasks
    }