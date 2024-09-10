from uuid import uuid4

from app.database import mongo_connection, mongo_get_collection


async def create_material(name: str, link: str, lesson_uuid: str):
    connection = await mongo_connection()
    material_collection = await mongo_get_collection(connection, "materials")
    material_collection.insert_one(
        {"uuid": str(uuid4()), "name": name, "lesson_uuid": lesson_uuid, "link": link}
    )


async def get_material_by_uuid(uuid: str):
    connection = await mongo_connection()
    material_collection = await mongo_get_collection(connection, "materials")
    return material_collection.find_one({"uuid": uuid})


async def get_materials_by_lesson_uuid(lesson_uuid: str):
    connection = await mongo_connection()
    material_collection = await mongo_get_collection(connection, "materials")
    return list(material_collection.find({"lesson_uuid": lesson_uuid}))
