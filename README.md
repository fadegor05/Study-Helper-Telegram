# 📚 StudyHelper - Бот для Расписания и Домашнего Задания

## 📜 Описание

Этот Telegram-бот автоматически парсит школьное расписание с официального сайта и предоставляет актуальную информацию о занятиях и домашнем задании. В случае изменений расписания или заданий, редакторы могут легко внести правки через интерфейс бота.

## 🎯 Основные возможности

- **Автоматическое парсинг расписания:** Бот может обновлять расписание у себя, забирая его с сайта расписания школы и уведомляет учеников об изменениях.
- **Вся информация на кончиках пальцев:** Ученики могут запросить расписание на любой день недели, сегодня или завтра
- **Управление домашним заданием:** Редакторы могут добавлять, изменять и удалять домашние задания через бота, легко привязывая их к датам и предметам.
- **Уведомления о домашнем задании:** Ученики получают уведомления о новых домашних заданиях и сроках их выполнения.
- **Контроль над выполнением:** Ученики с легкостью смогут отслеживать выполненое домашнее задание, а также бот будет отображать сначала самое свежие и невыполненные задания, а только потом остальные.

## 🚚 Роадмап

- Полное редактирование Д/З (добавить фото)
- Добавление дополнительных материалов к Д/З
- Отображение текущего и следующего урока в расписании
- Возможность прикреплять ответы и готовые решения к Д/З

## 📚 Как пользоваться

## 🚀 Установка и настройка

1. **Клонируйте репозиторий:**

   ```bash
   git clone git@github.com:fadegor05/Study-Helper-Telegram.git
   cd Study-Helper-Telegram
   ```

2. **Настройте .env**

   ```env
   TELEGRAM_TOKEN=
   MONGO_ROOT_USER=
   MONGO_ROOT_PASS=
   TZ=Europe/Moscow
   ```

3. **Запустите бота:**

   ```bash
   docker compose up
   ```

## 🛠 Стек

- **Python**
- **Aiogram**
- **Aiogram_dialog**
- **PostgreSQL**
- **Docker**

## 🗄️ MongoDB

### users

```
telegram_id: int
username: str
hometask_notification: bool
schedule_notification: bool
have_access: bool
is_editor: boolean | None
is_admin: bool | None
```

### hometasks

```
uuid: str
lesson_uuid: str
lesson: str
task: str
date: str
completed_by: [int]
images: [str]
author_id: int
edited_at: str | None
editor_id: int | None
```

### lessons

```
uuid: str
name: str

```

### schedule

```
day: int
name: str
lessons: [
    {
        name: str
        lesson_uuid: str
        start_time: str
        classroom: str
        building: str
    }
]
```

### weather

```
date: str
morning_temperature: float
morning_icon: str
morning_datetime: str
day_temperature: float
day_icon: str
day_datetime: str
```

### materials

```
uuid: str
lesson_uuid: str
link: str
name: str
```
