from aiogram_dialog import Dialog

from app.dialogs.hometask import windows


def menu_dialogs():
    return [
        Dialog(
            windows.hometask_window(),
        ),
    ]