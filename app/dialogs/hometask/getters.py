from aiogram_dialog import DialogManager

from app.crud.hometask import get_hometasks_all, get_hometask_by_uuid
from app.crud.lesson import get_lesson_by_uuid
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const


async def get_hometasks(dialog_manager: DialogManager, **kwargs):
    hometasks = await get_hometasks_all()
    return {
        'hometasks': hometasks
    }


async def get_hometask(dialog_manager: DialogManager, **kwargs):
    hometask_uuid = dialog_manager.start_data.get('hometask_uuid')
    hometask = await get_hometask_by_uuid(hometask_uuid)
    user_id = dialog_manager.middleware_data.get('event_chat').id
    lesson = await get_lesson_by_uuid(hometask.get('lesson_uuid'))
    books = lesson.get('books')
    is_completed = True if user_id in hometask.get('completed_by') else False
    return {
        'lesson': hometask.get('lesson'),
        'is_completed': 'Выполнено ✅' if is_completed else 'Не выполнено ⏳',
        'is_completed_button': '✅ Выполнено' if not is_completed else '❌ Отменить выполнение',
        'task': hometask.get('task'),
        'books': '\n'.join([ f'{book} - {books.get(book)}' for book in books])
    }
