from app.database import mongo_get_collection, mongo_connection


async def get_user_by_telegram_id(telegram_id: int):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    return user_collection.find_one({'telegram_id': telegram_id})


async def is_user_editor_by_telegram_id(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    return True if user.get('is_editor') else False


async def user_exits_by_telegram_id(telegram_id: int) -> bool:
    return True if await get_user_by_telegram_id(telegram_id) else False


async def create_user(telegram_id: int, username: str, specialization: str = None):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    user_collection.insert_one({
        'telegram_id': telegram_id,
        'username': username,
        'hometask_notification': True,
        'schedule_notification': True
    })
