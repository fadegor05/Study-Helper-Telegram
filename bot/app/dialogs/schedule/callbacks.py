from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.hometask import get_hometask_by_lesson_uuid_and_datetime
from app.crud.schedule import get_day_schedule
from app.dialogs.hometask.states import HometaskInfo


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


async def open_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, lesson_uuid: str, **kwargs):
    day = int(manager.start_data.get("schedule_day"))
    today = datetime.today()
    difference = day - today.isoweekday()
    target_date = today + timedelta(days=difference)
    hometask = await get_hometask_by_lesson_uuid_and_datetime(lesson_uuid, target_date)
    if hometask:
        await manager.start(HometaskInfo.info_hometask, {"hometask_uuid": hometask.get("uuid"), "day": day}, mode=StartMode.NORMAL)
    else:
        await c.answer("Задание на данный урок отсутствует ❌")
