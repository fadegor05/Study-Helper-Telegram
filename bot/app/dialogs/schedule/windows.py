from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Row
from aiogram_dialog.widgets.text import Format, Const

from app.dialogs.schedule import states, keyboards, callbacks, getters


def schedule_day_window():
    return Window(
        Format("*{name} *📆"),
        keyboards.column_lessons(callbacks.open_hometask),
        Row(Button(Const("◀️ Предыдущий день"), "previous_day_button", callbacks.previous_day), Button(Const("Следующий день ▶️"), "next_day_button", callbacks.next_day)),
        Cancel(Const("⬅️ Назад")),
        state=states.ScheduleMenu.info_schedule,
        getter=getters.get_schedule_day,
    )
