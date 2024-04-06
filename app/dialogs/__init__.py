from . import start, hometask


def get_dialogs():
    return [
        *start.menu_dialogs(),
        *hometask.menu_dialogs(),
    ]