from typing import Any, Optional, override
from fastapi import HTTPException
from app.databases.db import DB
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class MongoDB(DB):
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._client = AsyncIOMotorClient(uri)
        self._db = self._client[db_name]

    def _objectid(self, id: str) -> ObjectId:
        try:
            return ObjectId(id)
        except Exception as e:
            raise ValueError("Invalid id") from e

    @override
    def close(self):
        if self._client:
            self._client.close()

    # Wrapper to run queries and wrap Exceptions as HttpExceptions
    async def _try(self, f) -> Any:
        try:
            return await f()
        except Exception as e:
            raise HTTPException(500, str(e))

    @override
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        async def inner():
            result = await self._db[collection].insert_one(data)
            return {"id": str(result.inserted_id), **data}

        return await self._try(inner)

    @override
    async def update(self, collection: str, id: str, data: dict[str, Any]) -> bool:
        async def inner():
            result = await self._db[collection].update_one(
                {"_id": self._objectid(id)},
                {"$set": data},
            )
            return result.did_upsert

        return await self._try(inner)

    @override
    async def find_one(self, collection: str, id: str) -> Optional[dict[str, Any]]:
        async def inner():
            document = await self._db[collection].find_one({"_id": self._objectid(id)})
            if document:
                document["id"] = str(document["_id"])
            return document

        return await self._try(inner)

    @override
    async def find_one_by_filter(
        self, collection: str, filter: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        async def inner():
            document = await self._db[collection].find_one(filter)
            if document:
                document["id"] = str(document["_id"])
            return document

        return await self._try(inner)

    @override
    async def get_all(self, collection: str) -> list[dict[str, Any]]:
        async def inner():
            users = []
            cursor = self._db[collection].find()
            async for doc in cursor:
                doc["id"] = str(doc["_id"])
                users.append(doc)
            return users

        return await self._try(inner)

    @override
    async def delete(self, collection: str, id: str) -> bool:
        async def inner():
            result = await self._db[collection].delete_one({"_id": self._objectid(id)})
            return result.deleted_count > 0

        return await self._try(inner)

    @override
    async def exists_with_username_email(
        self, collection: str, username: str, email: str
    ) -> bool:
        async def inner():
            document = await self._db[collection].find_one(
                {"$or": [{"username": username}, {"email": email}]}
            )
            return document is not None

        return await self._try(inner)

    @override
    async def exists_with_title(self, collection: str, title: str) -> bool:
        async def inner():
            document = await self._db[collection].find_one({"title": title})
            return document is not None

        return await self._try(inner)
