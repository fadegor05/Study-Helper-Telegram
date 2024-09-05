from aiogram.fsm.state import StatesGroup, State


class HometaskMenu(StatesGroup):
    select_hometask = State()


class HometaskInfo(StatesGroup):
    info_hometask = State()


class HometaskCreate(StatesGroup):
    lesson_hometask = State()
    date_hometask = State()
    task_hometask = State()
    image_hometask = State()
    confirm_hometask = State()


class HometaskEdit(StatesGroup):
    task_hometask = State()
    confirm_hometask = State()

class HometaskDateEdit(StatesGroup):
    date_hometask = State()

class HometaskDelete(StatesGroup):
    confirm_hometask = State()