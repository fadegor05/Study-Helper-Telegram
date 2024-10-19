import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, ListGroup, Column, Group
from aiogram_dialog.widgets.text import Format


def column_lessons(on_click):
    return Column(
        Select(
            Format("{item[lesson_str]}"),
            id="s_scroll_lessons",
            item_id_getter=operator.itemgetter("lesson_uuid"),
            items="lessons",
            on_click=on_click,
        )
    )
