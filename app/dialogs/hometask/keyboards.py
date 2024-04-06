import operator
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def paginated_hometasks(on_click):
    return ScrollingGroup(
        Select(
            Format('⏳ DATE_PLACEHOLDER - {item[lesson]}'),
            id='s_scroll_hometasks',
            item_id_getter=operator.itemgetter('uuid'),
            items='hometasks',
            on_click=on_click
        ),
        id='hometasks_id',
        width=1, height=5
    )
