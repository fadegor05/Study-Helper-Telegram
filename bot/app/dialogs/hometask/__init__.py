from aiogram_dialog import Dialog

from app.dialogs.hometask import windows


def menu_dialogs():
    return [
        Dialog(
            windows.hometask_window(),
        ),
        Dialog(
            windows.hometask_info_window(),
        ),
        Dialog(
            windows.hometask_lesson_window(),
            windows.hometask_date_window(),
            windows.hometask_task_window(),
            windows.hometask_images_window(),
        ),
        Dialog(
            windows.hometask_edit_task_window(),
            windows.hometask_edit_done_window(),
        )
    ]