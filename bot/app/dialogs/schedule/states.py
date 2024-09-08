from aiogram.fsm.state import StatesGroup, State


class ScheduleMenu(StatesGroup):
    select_schedule = State()


class ScheduleInfo(StatesGroup):
    info_schedule = State()
