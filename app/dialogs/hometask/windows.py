from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button
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


def hometask_info_window():
    return Window(
        Format('PLACEHOILDER_DATE - {lesson} 🗒️\n{is_completed}\n\n{task}\n\nМатериалы 📚\n{books}'),
        Button(Format('{is_completed_button}'), 'status_change_hometask_button', callbacks.change_hometask_status),
        Cancel(Const('⬅️ Назад')),
        Button(Const('✏️ Редактировать'), 'hometask_edit_button'),
        state=states.HometaskInfo.info_hometask,
        getter=getters.get_hometask,
    )

