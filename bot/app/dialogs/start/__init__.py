from aiogram_dialog import Dialog

from app.dialogs.start import windows


def menu_dialogs():
    return [
        Dialog(
            windows.start_window(),
        ),
    ]
