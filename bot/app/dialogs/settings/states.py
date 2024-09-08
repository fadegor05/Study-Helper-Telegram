from aiogram.fsm.state import StatesGroup, State


class SettingsMenu(StatesGroup):
    settings = State()
