from app.database import mongo_connection, mongo_get_collection


async def get_hometasks_all():
    connection = await mongo_connection()
    user_collection = await mongo_get_collection(connection, 'hometasks')
    return user_collection.find({})
