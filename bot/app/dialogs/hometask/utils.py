from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_editor(data: Dict, widget: Whenable, manager: DialogManager):
    return data.get("is_editor")


def is_not_editor(data: Dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_editor")


def is_lesson_in_schedule(data: Dict, widget: Whenable, manager: DialogManager):
    return data.get("in_schedule")


def is_lesson_not_in_schedule(data: Dict, widget: Whenable, manager: DialogManager):
    return not data.get("in_schedule")


def is_not_completed(data: Dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_completed")


def is_suggested(data: Dict, widget: Whenable, manager: DialogManager):
    return data.get("is_suggested")


def is_not_suggested(data: Dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_suggested")


def is_not_completed_and_not_suggested(data: Dict, widget: Whenable, manager: DialogManager):
    return not data.get("is_completed") and not data.get("is_suggested")
