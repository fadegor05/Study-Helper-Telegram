from aiogram_dialog import Dialog

from app.dialogs.schedule import windows


def menu_dialogs():
    return [
        Dialog(windows.schedule_day_window()),
    ]
