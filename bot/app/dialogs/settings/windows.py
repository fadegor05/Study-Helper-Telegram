from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.settings import getters, states, callbacks
from app.dialogs.settings.utils import is_admin


def settings_window():
    return Window(
        Const('⚙️ *Настройки*\n\nДля переключения состояния пункта нажмите на него 📍'),
        Button(Format('{hometask_notification} Напоминание о Д/З'), 'hometask_notification_button', callbacks.on_chosen_hometask_notification),
        Button(Format('{schedule_notification} Уведомление о расписании'), 'schedule_notification_button', callbacks.on_chosen_schedule_notification),
        Button(Const('🔄 Синхронизация расписания с предметами'), 'lessons_sync_button', callbacks.sync_schedule_with_lessons, when=is_admin),
        Button(Const('🔄 Синхронизация Д/З с предметами'), 'hometasks_sync_button', callbacks.sync_hometasks_with_lessons, when=is_admin),
        Button(Const('⬇️ Парсинг расписания с mstimetables'), 'schedule_parse_button', callbacks.parse_schedule, when=is_admin),
        Cancel(Const('⬅️ Назад')),
        getter=getters.get_settings,
        state=states.SettingsMenu.settings,
    )