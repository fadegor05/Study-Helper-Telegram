from pymongo import MongoClient

from app.core.config import MONGO_URL, MONGO_DATABASE_NAME

COLLECTIONS = [
    'users',
    'lessons'
]


async def mongo_connection(connection_url: str = MONGO_URL) -> MongoClient:
    connection = MongoClient(connection_url)
    return connection


async def mongo_init(connection: MongoClient, database_name: str = MONGO_DATABASE_NAME) -> None:
    db = connection.get_database(database_name)
    for collection in COLLECTIONS:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
