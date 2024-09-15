from datetime import datetime, timedelta

from aiogram.types import CallbackQuery

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager

from app.crud.schedule import get_all_schedule_sorted
from app.dialogs.hometask.states import HometaskMenu
from app.dialogs.schedule.states import ScheduleMenu
from app.dialogs.settings.states import SettingsMenu


async def on_chosen_hometask(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(HometaskMenu.select_hometask)


async def on_chosen_schedule(c: CallbackQuery, widget: Button, manager: DialogManager):
    today = datetime.today()
    schedule = await get_all_schedule_sorted()
    i = 0
    while i < 7:
        for day in schedule:
            if today.isoweekday() == int(day.get("day")):
                await manager.start(ScheduleMenu.info_schedule, {"schedule_day": int(today.isoweekday())})
                return
        today += timedelta(days=1)
        i += 1


async def on_chosen_settings(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(SettingsMenu.settings)
