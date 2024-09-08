from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.schedule import get_day_schedule
from app.dialogs.schedule.states import ScheduleInfo


async def on_chosen_schedule_day(
    c: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    schedule_day: int,
    **kwargs,
):
    await manager.start(ScheduleInfo.info_schedule, {"schedule_day": schedule_day})


async def on_chosen_today(c: CallbackQuery, widget: Button, manager: DialogManager):
    day = datetime.today().isoweekday()
    if day == 7:
        day = 6
    if await get_day_schedule(day):
        await manager.start(ScheduleInfo.info_schedule, {"schedule_day": day})
    else:
        await c.answer("Расписание на данный день отсутствует ❌")


async def on_chosen_tomorrow(c: CallbackQuery, widget: Button, manager: DialogManager):
    day = datetime.today().isoweekday() + 1
    if day == 8:
        day = 1
    if await get_day_schedule(day):
        await manager.start(ScheduleInfo.info_schedule, {"schedule_day": day})
    else:
        await c.answer("Расписание на данный день отсутствует ❌")
