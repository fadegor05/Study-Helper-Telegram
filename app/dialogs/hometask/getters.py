from copy import deepcopy
from datetime import datetime, timedelta

from aiogram_dialog import DialogManager

from app.crud.hometask import get_hometasks_all, get_hometask_by_uuid
from app.crud.lesson import get_lesson_by_uuid, get_lessons_all
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram.enums.content_type import ContentType


async def get_hometasks(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.middleware_data.get('event_chat').id

    hometasks = []
    for hometask in await get_hometasks_all():
        hometask.update(date=datetime.fromisoformat(hometask.get('date')).strftime('%d.%m'),
                        is_completed='✅' if user_id in hometask.get('completed_by') else '⏳')
        hometasks.append(hometask)
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
        'date': datetime.fromisoformat(hometask.get('date')).strftime('%d.%m'),
        'books': '\n'.join([f'{book} - {books.get(book)}' for book in books]),
        'image': MediaAttachment(ContentType.PHOTO, file_id=MediaId(hometask.get('images')[-1]))
    }


async def get_lessons(dialog_manager: DialogManager, **kwargs):
    lessons = await get_lessons_all()
    return {
        'lessons': lessons
    }


async def get_dates(dialog_manager: DialogManager, **kwargs):
    dates = []
    now = datetime.now()
    start_datetime = datetime(now.year, now.month, now.day, 10, 0, 0)
    end_datetime = start_datetime + timedelta(days=9)

    current_datetime = start_datetime
    while current_datetime <= end_datetime:
        dates.append({'date': current_datetime, 'date_iso': current_datetime.isoformat(),
                      'date_str': current_datetime.strftime('%d.%m')})
        current_datetime += timedelta(days=1)

    return {
        'dates': dates
    }
