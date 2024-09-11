from typing import Any, Mapping

from pymongo import MongoClient
from pymongo.collection import Collection

from app.core.config import MONGO_URL, MONGO_DATABASE_NAME

COLLECTIONS = [
    "users",
    "lessons",
    "hometasks",
    "schedule",
    "materials",
    "weather"
]


async def mongo_connection(connection_url: str = MONGO_URL) -> MongoClient:
    connection = MongoClient(connection_url)
    return connection


async def mongo_init(
    connection: MongoClient, database_name: str = MONGO_DATABASE_NAME
) -> None:
    db = connection.get_database(database_name)
    for collection in COLLECTIONS:
        if collection not in db.list_collection_names():
            db.create_collection(collection)


async def mongo_get_collection(
    connection: MongoClient,
    collection_name: str,
    database_name: str = MONGO_DATABASE_NAME,
) -> Collection[Mapping[str, Any] | Any] | None:
    if collection_name not in COLLECTIONS:
        return None
    db = connection.get_database(database_name)
    return db.get_collection(collection_name)
