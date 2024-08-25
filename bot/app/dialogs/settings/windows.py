from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.settings import getters, states, callbacks


def settings_window():
    return Window(
        Const('⚙️ Настройки\n\nДля переключения состояния пункта нажмите на него 📍'),
        Button(Format('{hometask_notification} Напоминание о Д/З'), 'hometask_notification_button', callbacks.on_chosen_hometask_notification),
        Button(Format('{schedule_notification} Уведомление о расписании'), 'schedule_notification_button', callbacks.on_chosen_schedule_notification),
        Cancel(Const('⬅️ Назад')),
        getter=getters.get_settings,
        state=states.SettingsMenu.settings,
    )