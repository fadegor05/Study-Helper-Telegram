import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, ListGroup, Column, Group
from aiogram_dialog.widgets.text import Format


def column_schedule(on_click):
    return Group(
        Select(
            Format("📆 {item[name]}"),
            id="s_scroll_schedule",
            item_id_getter=operator.itemgetter("day"),
            items="schedule",
            on_click=on_click,
        ),
        width=2,
    )


def column_lessons():
    return Column(
        Select(
            Format("{item[start_time]} {item[name]} {item[place]}"),
            id="s_scroll_lessons",
            item_id_getter=operator.itemgetter("lesson_uuid"),
            items="lessons",
        )
    )
