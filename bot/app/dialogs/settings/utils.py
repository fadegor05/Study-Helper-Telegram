from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_admin(data: Dict, widget: Whenable, manager: DialogManager):
    return data.get("is_admin")
