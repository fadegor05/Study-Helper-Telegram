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


async def have_user_access_by_telegram_id(telegram_id: int) -> bool:
    user = await get_user_by_telegram_id(telegram_id)
    return user.get('have_access')


async def create_user(telegram_id: int, username: str, specialization: str = None):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    user_collection.insert_one({
        'telegram_id': telegram_id,
        'username': username,
        'hometask_notification': True,
        'schedule_notification': True,
        'have_access': False
    })


async def get_all_users_with_hometask_notification():
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    return user_collection.find({'hometask_notification': True})


async def get_all_users_with_schedule_notification():
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    return user_collection.find({'schedule_notification': True})


async def set_hometask_notification_by_telegram_id(telegram_id: int, state: bool):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    user_collection.update_one({'telegram_id': telegram_id}, {'$set': {'hometask_notification': state}})


async def set_schedule_notification_by_telegram_id(telegram_id: int, state: bool):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    user_collection.update_one({'telegram_id': telegram_id}, {'$set': {'schedule_notification': state}})
