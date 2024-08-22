from . import start, hometask, schedule


def get_dialogs():
    return [
        *start.menu_dialogs(),
        *hometask.menu_dialogs(),
        *schedule.menu_dialogs(),
    ]