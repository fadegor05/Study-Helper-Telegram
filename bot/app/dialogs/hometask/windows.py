from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Back, Next
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram.enums.content_type import ContentType
from aiogram_dialog.widgets.media import DynamicMedia

from app.dialogs.hometask import states, keyboards, callbacks, getters


def hometask_window():
    return Window(
        Format('Домашнее задание 📑\n\n📋 Невыполненых заданий: {uncompleted_amount}\n\nВыберите интересующее вас задание 📚'),
        keyboards.paginated_hometasks(callbacks.on_chosen_hometask),
        Button(Const('📝 Создать задание'), 'hometask_create_button', callbacks.on_create_hometask),
        Cancel(Const('⬅️ Назад')),
        state=states.HometaskMenu.select_hometask,
        getter=getters.get_hometasks,
    )


def hometask_info_window():
    return Window(
        DynamicMedia('image'),
        Format('{date} - {lesson} 🗒️\n{is_completed}\n\n{task}\n\nМатериалы 📚\n{books}'),
        Button(Format('{is_completed_button}'), 'status_change_hometask_button', callbacks.change_hometask_status),
        Button(Const('✏️ Редактировать'), 'hometask_edit_button'),
        Cancel(Const('⬅️ Назад')),
        state=states.HometaskInfo.info_hometask,
        getter=getters.get_hometask,
    )


def hometask_lesson_window():
    return Window(
        Const('Выберите предмет, по которому вы хотите добавить домашнее задание ✏️'),
        keyboards.paginated_lessons(callbacks.on_chosen_lesson),
        Cancel(Const('⬅️ Назад')),
        state=states.HometaskCreate.lesson_hometask,
        getter=getters.get_lessons,
    )


def hometask_date_window():
    return Window(
        Const('Выберите на какой день вы хотите добавить домашнее задание 🗓️'),
        Button(Const('⏳ Ближайший урок'), 'hometask_date_soon'),
        keyboards.paginated_dates(callbacks.on_chosen_date),
        Back(Const('⬅️ Назад')),
        state=states.HometaskCreate.date_hometask,
        getter=getters.get_dates,
    )


def hometask_task_window():
    return Window(
        Const('Введите домашнее задание 📝'),
        TextInput('hometask_task_input', on_success=callbacks.on_entered_task),
        Back(Const('⬅️ Назад')),
        state=states.HometaskCreate.task_hometask
    )


def hometask_images_window():
    return Window(
        Const('Прикрепите фото задания 📷\n\nЕсли же вы прикрепили нужные фото, то нажмите готово ✅'),
        MessageInput(callbacks.on_sent_images, ContentType.PHOTO),
        Back(Const('⬅️ Назад')),
        Button(Const('✅ Готово'), 'hometask_done_create_hometask', callbacks.on_done_create_hometask),
        state=states.HometaskCreate.image_hometask
    )