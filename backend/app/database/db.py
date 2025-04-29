from typing import Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient

class AdminDB:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._client = AsyncIOMotorClient(db_name)
        self._db = self._client[db_name]

    def close(self):
        if self._client:
            self._client.close()

    async def create(self, collection_name: str, data: dict[str, Any]) -> dict[str, Any]:
        result = await self._db[collection_name].insert_one(data)
        return {"id": str(result.inserted_id), **data}

    # Generic method to find one document
    async def find_one(self, collection_name: str, query: dict[str, Any]) -> Optional[dict[str, Any]]:
        document = await self._db[collection_name].find_one(query)
        if document:
            document["id"] = str(document["_id"])
        return document

    # Generic method to update a document
    async def update(self, collection_name: str, query: dict[str, Any], update_data: dict[str, Any]) -> bool:
        collection = self._db[collection_name]
        result = await collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0
