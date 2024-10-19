from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select, Button

from app.crud.hometask import get_hometask_by_lesson_uuid_and_date
from app.crud.schedule import get_day_schedule
from app.dialogs.hometask.states import HometaskInfo


async def next_day(c: CallbackQuery, widget: Button, manager: DialogManager):
    current_date = datetime.fromisoformat(manager.start_data.get("current_date"))
    current_date += timedelta(days=1)
    if current_date.isoweekday() == 7:
        current_date += timedelta(days=1)
    if await get_day_schedule(current_date.isoweekday()):
        manager.start_data.update(current_date=current_date.isoformat())
        await manager.show()
    else:
        await c.answer("Расписание на данный день отсутствует ❌")


async def previous_day(c: CallbackQuery, widget: Button, manager: DialogManager):
    current_date = datetime.fromisoformat(manager.start_data.get("current_date"))
    current_date -= timedelta(days=1)
    if current_date.isoweekday() == 7:
        current_date -= timedelta(days=1)
    if await get_day_schedule(current_date.isoweekday()):
        manager.start_data.update(current_date=current_date.isoformat())
        await manager.show()
    else:
        await c.answer("Расписание на данный день отсутствует ❌")


async def open_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, lesson_uuid: str, **kwargs):
    current_date = datetime.fromisoformat(manager.start_data.get("current_date"))
    hometask = await get_hometask_by_lesson_uuid_and_date(lesson_uuid, current_date.date())
    if hometask:
        await manager.start(HometaskInfo.info_hometask, {"hometask_uuid": hometask.get("uuid")}, mode=StartMode.NORMAL)
    else:
        await c.answer("Задание на данный урок отсутствует ❌")
