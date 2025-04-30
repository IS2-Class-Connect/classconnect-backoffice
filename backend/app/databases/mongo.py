from typing import Any, Optional, override
from app.databases.db import DB
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB(DB):
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._client = AsyncIOMotorClient(uri)
        self._db = self._client[db_name]

    @override
    def close(self):
        if self._client:
            self._client.close()

    @override
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        result = await self._db[collection].insert_one(data)
        return {"id": str(result.inserted_id), **data}

    @override
    async def find_one(self, collection: str, id: str) -> Optional[dict[str, Any]]:
        document = await self._db[collection].find_one({"_id": id})
        if document:
            document["id"] = str(document["_id"])
        return document

    @override
    async def get_all(self, collection: str) -> list[dict[str, Any]]:
        users = []
        cursor = self._db[collection].find()
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            users.append(doc)
        return users

    @override
    async def exists_with_username_email(
        self, collection: str, username: str, email: str
    ) -> bool:
        document = await self._db[collection].find_one(
            {"$or": [{"username": username}, {"email": email}]}
        )

        return document is not None

    @override
    async def delete(self, collection: str, id: str) -> bool:
        result = await self._db[collection].delete_one({"_id": id})
        return result.deleted_count > 0
