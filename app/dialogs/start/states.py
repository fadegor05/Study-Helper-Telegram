from aiogram.fsm.state import StatesGroup, State


class StartMenu(StatesGroup):
    select_menu = State()
