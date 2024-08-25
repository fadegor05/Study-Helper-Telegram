from . import start, hometask, schedule, settings


def get_dialogs():
    return [
        *start.menu_dialogs(),
        *hometask.menu_dialogs(),
        *schedule.menu_dialogs(),
        *settings.menu_dialogs(),
    ]