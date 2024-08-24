from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import MessageInput, TextInput

from app.crud.hometask import change_hometask_status_by_uuid_and_user_id, create_hometask, get_hometask_by_uuid
from app.crud.schedule import get_lesson_weekdays_by_uuid
from app.crud.user import is_user_editor_by_telegram_id
from app.dialogs.hometask.states import HometaskInfo, HometaskCreate


async def on_chosen_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, hometask_uuid: str, **kwargs):
    hometask = await get_hometask_by_uuid(hometask_uuid)
    media_list = []
    if hometask.get('images'):
        for image in hometask.get('images')[:-1]:
            media_list.append(InputMediaPhoto(media=image))
        if len(media_list) > 0:
            media_group = MediaGroupBuilder(media_list)
            await c.bot.send_media_group(chat_id=c.from_user.id, media=media_group.build())
    await manager.start(HometaskInfo.info_hometask, {'hometask_uuid': hometask_uuid})


async def change_hometask_status(c: CallbackQuery, widget: Button, manager: DialogManager):
    hometask_uuid = manager.start_data.get('hometask_uuid')
    user_id = manager.middleware_data.get('event_chat').id
    await change_hometask_status_by_uuid_and_user_id(hometask_uuid, user_id)


async def on_create_hometask(c: CallbackQuery, widget: Button, manager: DialogManager):
    user_id = manager.middleware_data.get('event_chat').id
    if not await is_user_editor_by_telegram_id(user_id):
        await c.answer('У вас недостаточно прав для этого ❌')
        return
    await manager.start(HometaskCreate.lesson_hometask)


async def on_chosen_lesson(c: CallbackQuery, widget: Select, manager: DialogManager, lesson_uuid: str, **kwargs):
    manager.dialog_data.update(lesson_uuid=lesson_uuid)
    await manager.switch_to(HometaskCreate.date_hometask)


async def on_chosen_soon_date(c: CallbackQuery, widget: Button, manager: DialogManager):
    lesson_uuid = manager.dialog_data.get('lesson_uuid')
    lesson_weekdays = await get_lesson_weekdays_by_uuid(lesson_uuid)
    date = None
    now = datetime.now() + timedelta(days=1)
    start_datetime = datetime(now.year, now.month, now.day, 10, 0, 0)
    end_datetime = start_datetime + timedelta(days=7)

    current_datetime = start_datetime
    while current_datetime <= end_datetime:
        if current_datetime.isoweekday() in lesson_weekdays:
            date = current_datetime.isoformat()
            break
        current_datetime += timedelta(days=1)
    manager.dialog_data.update(date=date)
    await manager.switch_to(HometaskCreate.task_hometask)


async def on_chosen_date(c: CallbackQuery, widget: Select, manager: DialogManager, date: str, **kwargs):
    manager.dialog_data.update(date=date)
    await manager.switch_to(HometaskCreate.task_hometask)


async def on_entered_task(m: Message, widget: TextInput, manager: DialogManager, task: str, **kwargs):
    manager.dialog_data.update(task=task)
    await manager.switch_to(HometaskCreate.image_hometask)


async def on_sent_images(m: Message, widget: MessageInput, manager: DialogManager):
    file_id = m.photo[-1].file_id
    images = manager.dialog_data.get('images')
    if not images:
        images = [file_id]
    else:
        images.append(file_id)
    manager.dialog_data.update(images=images)


async def on_done_create_hometask(c: CallbackQuery, widget: Button, manager: DialogManager):
    lesson_uuid = manager.dialog_data.get('lesson_uuid')
    date = manager.dialog_data.get('date')
    task = manager.dialog_data.get('task')
    images = manager.dialog_data.get('images')
    await create_hometask(lesson_uuid, task, date, images)
    await c.answer('Задание было успешно добавлено ✅')
    await manager.done()
