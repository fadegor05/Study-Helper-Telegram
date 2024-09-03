import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_schedule(on_click):
    return ScrollingGroup(
        Select(
            Format('📆 {item[name]}'),
            id='s_scroll_schedule',
            item_id_getter=operator.itemgetter('day'),
            items='schedule',
            on_click=on_click
        ),
        id='schedule_day_id',
        width=1, height=7
    )


def paginated_lessons():
    return ScrollingGroup(
        Select(
            Format('{item[start_time]} {item[name]} {item[place]}'),
            id='s_scroll_lessons',
            item_id_getter=operator.itemgetter('lesson_uuid'),
            items='lessons',
        ),
        id='lessons_id',
        width=1, height=7
    )
