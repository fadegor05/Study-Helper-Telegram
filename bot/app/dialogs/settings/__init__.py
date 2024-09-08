from aiogram_dialog import Dialog

from app.dialogs.settings import windows


def menu_dialogs():
    return [
        Dialog(
            windows.settings_window(),
        ),
    ]
