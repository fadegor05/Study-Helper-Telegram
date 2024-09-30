from app.database import mongo_connection, mongo_get_collection


async def mongo_migrate():
    await migrate_to_statuses_from_completed_by()


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
