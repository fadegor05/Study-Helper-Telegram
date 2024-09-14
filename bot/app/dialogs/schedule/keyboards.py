import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, ListGroup, Column, Group
from aiogram_dialog.widgets.text import Format



def column_lessons():
    return Column(
        Select(
            Format("{item[start_time]} {item[name]} {item[place]}"),
            id="s_scroll_lessons",
            item_id_getter=operator.itemgetter("lesson_uuid"),
            items="lessons",
        )
    )
