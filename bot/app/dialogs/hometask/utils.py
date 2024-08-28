from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_editor(data: Dict, widget: Whenable, manager: DialogManager):
    return data.get('is_editor')