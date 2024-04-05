from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Cancel

from app.dialogs.start import states


def start_window():
    return Window(
        Const('Добро Пожаловать в study helper™ 👋\n\nЭто - Менеджер домашнего задания, здесь можно найти актуальное '
              'Д/З, полезные материалы, конспекты, а также учебники 📚\n\nСкрафтил @fadegor05 ⭐\nРедактирует @TGRTX '
              '📝\n\nВыберите то, что вас интересует 🤔'),
        Button(Const('📑 Домашнее задание'), 'homework_button'),
        Button(Const('📆 Расписание'), 'schedule_button'),
        Cancel(Const('❌ Выход')),
        state=states.StartMenu.select_menu,
    )
