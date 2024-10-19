from app.database import mongo_connection, mongo_get_collection
from datetime import datetime


async def mongo_migrate():
    await migrate_to_statuses_from_completed_by()
    await migrate_from_isoformat_to_datetime_hometasks()


async def migrate_to_statuses_from_completed_by():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")

    documents = hometask_collection.find({"completed_by": {"$exists": True}})

    for doc in documents:
        completed_by = doc.get('completed_by', [])

        statuses = {str(user): 1 for user in completed_by}

        update_operation = {
            "$set": {"statuses": statuses},
            "$unset": {"completed_by": ""}
        }

        hometask_collection.update_one({"uuid": doc["uuid"]}, update_operation)


async def migrate_from_isoformat_to_datetime_hometasks():
    connection = await mongo_connection()
    hometask_collection = await mongo_get_collection(connection, "hometasks")

    documents = hometask_collection.find({"date": {"$type": "string"}})

    for doc in documents:
        datetime_str = doc.get("date")
        datetime_migrated = datetime.combine(datetime.fromisoformat(datetime_str).date(), datetime.min.time())

        update_operation = {
            "$set": {"date": datetime_migrated},
        }

        hometask_collection.update_one({"uuid": doc["uuid"]}, update_operation)

    documents = hometask_collection.find({"edited_at": {"$type": "string"}})

    for doc in documents:
        datetime_str = doc.get("edited_at")
        datetime_migrated = datetime.combine(datetime.fromisoformat(datetime_str).date(), datetime.min.time())

        update_operation = {
            "$set": {"edited_at": datetime_migrated},
        }

        hometask_collection.update_one({"uuid": doc["uuid"]}, update_operation)