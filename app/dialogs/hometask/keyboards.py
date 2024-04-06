import operator
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_hometasks(on_click):
    return ScrollingGroup(
        Select(
            Format('⏳ {item[date]} - {item[lesson]}'),
            id='s_scroll_hometasks',
            item_id_getter=operator.itemgetter('uuid'),
            items='hometasks',
            on_click=on_click
        ),
        id='hometasks_id',
        width=1, height=5
    )


def paginated_lessons(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[name]}'),
            id='s_scroll_lessons',
            item_id_getter=operator.itemgetter('uuid'),
            items='lessons',
            on_click=on_click
        ),
        id='lessons_id',
        width=1, height=5
    )


def paginated_dates(on_click):
    return ScrollingGroup(
        Select(
            Format('📆 {item[date_str]}'),
            id='s_scroll_dates',
            item_id_getter=operator.itemgetter('date_iso'),
            items='dates',
            on_click=on_click
        ),
        id='dates_id',
        width=1, height=5
    )
