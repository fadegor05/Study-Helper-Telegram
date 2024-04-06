from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.hometask import states, keyboards, callbacks, getters


def hometask_window():
    return Window(
        Format('Домашнее задание 📑\n\n📋 Невыполненых заданий: PLACEHOLDER\n\nВыберите интересующее вас задание 📚'),
        keyboards.paginated_hometasks(callbacks.on_chosen_hometask),
        Cancel(Const('⬅️ Назад')),
        state=states.HometaskMenu.select_hometask,
        getter=getters.get_hometasks,
    )
