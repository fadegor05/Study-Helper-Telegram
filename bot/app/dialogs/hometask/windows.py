from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Button, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram.enums.content_type import ContentType
from aiogram_dialog.widgets.media import DynamicMedia

from app.dialogs.hometask import states, keyboards, callbacks, getters, utils
from app.dialogs.hometask.utils import is_lesson_in_schedule, is_lesson_not_in_schedule


def hometask_window():
    return Window(
        Format(
            "*Домашнее задание* 📑\n\n{title_uncompleted_str}{tomorrow_uncompleted_amount_str}{uncompleted_amount_str}\nВыберите интересующее вас задание 📚"
        ),
        keyboards.paginated_hometasks(callbacks.on_chosen_hometask),
        Button(
            Const("📝 Создать задание"),
            "hometask_create_button",
            callbacks.on_create_hometask,
            when=utils.is_editor,
        ),
        Cancel(Const("⬅️ Назад")),
        state=states.HometaskMenu.select_hometask,
        getter=getters.get_hometasks,
    )


def hometask_info_window():
    return Window(
        DynamicMedia("image_last"),
        Format(
            "*{date} {lesson}*\n{is_completed}\n\n{task}\n\n*Материалы* 📚\n{books}\n\n*Автор* 🔗\n@{author_username}"
        ),
        Button(
            Format("{is_completed_button}"),
            "status_change_hometask_button",
            callbacks.change_hometask_status,
        ),
        Button(
            Const("✏️ Изменить задание"),
            "hometask_edit_button",
            callbacks.on_edit_hometask,
            when=utils.is_editor,
        ),
        Button(
            Const("🗓️ Изменить дату"),
            "date_edit_button",
            callbacks.on_edit_date,
            when=utils.is_editor,
        ),
        Button(
            Const("🗑️ Удалить"),
            "date_delete_button",
            callbacks.on_delete_hometask,
            when=utils.is_editor,
        ),
        Cancel(Const("⬅️ Назад")),
        state=states.HometaskInfo.info_hometask,
        getter=getters.get_hometask,
    )


def hometask_lesson_window():
    return Window(
        Const("*Выберите предмет, по которому вы хотите добавить домашнее задание* ✏️"),
        keyboards.paginated_lessons(callbacks.on_chosen_lesson),
        Cancel(Const("⬅️ Назад")),
        state=states.HometaskCreate.lesson_hometask,
        getter=getters.get_lessons,
    )


def hometask_date_window():
    return Window(
        Const("*Выберите на какой день вы хотите добавить домашнее задание* 🗓️"),
        Const(
            "\n_Урока еще нет в расписании, учитывай это при выборе даты_ ⚠️",
            when=is_lesson_not_in_schedule,
        ),
        Button(
            Const("⏳ Следующий урок"),
            "hometask_date_soon",
            callbacks.on_chosen_soon_date,
            when=is_lesson_in_schedule,
        ),
        keyboards.paginated_dates(callbacks.on_chosen_date),
        Back(Const("⬅️ Назад")),
        state=states.HometaskCreate.date_hometask,
        getter=getters.get_dates,
    )


def hometask_task_window():
    return Window(
        Const("*Введите домашнее задание* 📝"),
        TextInput("hometask_task_input", on_success=callbacks.on_entered_task),
        Back(Const("⬅️ Назад")),
        state=states.HometaskCreate.task_hometask,
    )


def hometask_images_window():
    return Window(
        Const(
            "*Прикрепите фото задания* 📷\n\nЕсли же вы прикрепили нужные фото, то нажмите готово ✅"
        ),
        MessageInput(callbacks.on_sent_images, ContentType.PHOTO),
        Back(Const("⬅️ Назад")),
        Button(
            Const("✅ Готово"),
            "hometask_done_create_hometask",
            callbacks.on_done_create_hometask,
        ),
        state=states.HometaskCreate.image_hometask,
    )


def hometask_edit_date_window():
    return Window(
        Const("*Выберите на какой день вы хотите изменить домашнее задание* 🗓️"),
        Const(
            "\n_Урока еще нет в расписании, учитывай это при выборе даты_ ⚠️",
            when=is_lesson_not_in_schedule,
        ),
        Button(
            Const("⏳ Следующий урок"),
            "hometask_edit_date_soon",
            callbacks.on_chosen_soon_edit_date,
            when=is_lesson_in_schedule,
        ),
        keyboards.paginated_dates(callbacks.on_chosen_edit_date),
        Cancel(Const("⬅️ Назад")),
        state=states.HometaskDateEdit.date_hometask,
        getter=getters.get_dates,
    )


def hometask_edit_task_window():
    return Window(
        Format(
            "*Текущее домашнее задание* 📚\n\n`{task}`\n\nВведите новое домашнее задание 📝"
        ),
        TextInput("hometask_task_input", on_success=callbacks.on_entered_edit_task),
        Cancel(Const("⬅️ Назад")),
        state=states.HometaskEdit.task_hometask,
        getter=getters.get_hometask_task,
    )


def hometask_edit_done_window():
    return Window(
        Format("Измененное задание ✏️\n\n`{task}`"),
        Back(Const("⬅️ Назад")),
        Button(
            Const("✅ Готово"),
            "hometask_done_edit_hometask",
            callbacks.on_done_edit_hometask,
        ),
        state=states.HometaskEdit.confirm_hometask,
        getter=getters.get_hometask_edited,
    )


def hometask_delete_window():
    return Window(
        Format(
            "Если вы действительно хотите удалить данное задание, то нажмите *Удалить* 🗑️\n\n_После удаления нажмите назад, чтобы вернуться к списку Д/З_ ⚠️"
        ),
        Cancel(Const("⬅️ Назад")),
        Button(
            Const("🗑️ Удалить"),
            "hometask_delete_hometask",
            callbacks.on_delete_confirm_hometask,
        ),
        state=states.HometaskDelete.confirm_hometask,
    )
