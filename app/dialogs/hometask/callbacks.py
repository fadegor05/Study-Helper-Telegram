from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input import MessageInput, TextInput

from app.crud.hometask import change_hometask_status_by_uuid_and_user_id, create_hometask
from app.crud.lesson import create_lesson
from app.dialogs.hometask.states import HometaskInfo, HometaskCreate


async def on_chosen_hometask(c: CallbackQuery, widget: Select, manager: DialogManager, hometask_uuid: str, **kwargs):
    await manager.start(HometaskInfo.info_hometask, {'hometask_uuid': hometask_uuid})


async def change_hometask_status(c: CallbackQuery, widget: Button, manager: DialogManager):
    hometask_uuid = manager.start_data.get('hometask_uuid')
    user_id = manager.middleware_data.get('event_chat').id
    await change_hometask_status_by_uuid_and_user_id(hometask_uuid, user_id)


async def on_create_hometask(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(HometaskCreate.lesson_hometask)


async def on_chosen_lesson(c: CallbackQuery, widget: Select, manager: DialogManager, lesson_uuid: str, **kwargs):
    manager.dialog_data.update(lesson_uuid=lesson_uuid)
    await manager.switch_to(HometaskCreate.date_hometask)


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
