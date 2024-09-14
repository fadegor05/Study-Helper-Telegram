from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.schedule import get_day_schedule


async def next_day(c: CallbackQuery, widget: Button, manager: DialogManager):
    day = int(manager.start_data.get("schedule_day"))
    day += 1
    if day >= 7:
        day = 1
    if await get_day_schedule(day):
        manager.start_data.update(schedule_day=day)
        await manager.show()
    else:
        await c.answer("Расписание на данный день отсутствует ❌")


async def previous_day(c: CallbackQuery, widget: Button, manager: DialogManager):
    day = int(manager.start_data.get("schedule_day"))
    day -= 1
    if day <= 0:
        day = 6
    if await get_day_schedule(day):
        manager.start_data.update(schedule_day=day)
        await manager.show()
    else:
        await c.answer("Расписание на данный день отсутствует ❌")
