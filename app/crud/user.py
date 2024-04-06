from app.database import mongo_get_collection, mongo_connection


async def user_exits_by_telegram_id(telegram_id: int) -> bool:
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    return True if user_collection.find_one({'telegram_id': telegram_id}) else False


async def create_user(telegram_id: int, username: str, specialization: str = None):
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'users')
    user_collection.insert_one({
        'telegram_id': telegram_id,
        'username': username,
        'specialization': specialization
    })
