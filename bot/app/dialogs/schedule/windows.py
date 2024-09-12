from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Row
from aiogram_dialog.widgets.text import Format, Const

from app.dialogs.schedule import states, keyboards, callbacks, getters


def schedule_window():
    return Window(
        Const("*Расписание *🗓️\n\nВыберите день недели, интересующий вас 📄"),
        Button(Const("🔗 Сегодня"), "today_schedule_button", callbacks.on_chosen_today),
        Button(
            Const("🕒 Завтра"), "tomorrow_schedule_button", callbacks.on_chosen_tomorrow
        ),
        keyboards.column_schedule(callbacks.on_chosen_schedule_day),
        Cancel(Const("⬅️ Назад")),
        state=states.ScheduleMenu.select_schedule,
        getter=getters.get_schedule,
    )


def schedule_day_window():
    return Window(
        Format("*{name} *📆"),
        keyboards.column_lessons(),
        Row(Button(Const("◀️ Предыдущий день"), "previous_day_button", callbacks.previous_day), Button(Const("Следующий день ▶️"), "next_day_button", callbacks.next_day)),
        Cancel(Const("⬅️ Назад")),
        state=states.ScheduleInfo.info_schedule,
        getter=getters.get_schedule_day,
    )
