from typing import Any, Optional, override
from app.databases.db import DB
from collections import defaultdict
from uuid import UUID

class DictDB(DB):
    def __init__(self, uri: str, db_name: str):
        self._db = defaultdict(dict)

    @override
    def close(self):
        pass

    @override
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        id = UUID()
        self._db[collection][id] = data
        return {"id": id, **data}

    @override
    async def find_one(self, collection: str, id: UUID) -> Optional[dict[str, Any]]:
        return self._db[collection].get(id)

    @override
    async def get_all(self, collection: str) -> list[Any]:
        return list(self._db[collection].values())

    @override
    async def exists_with_username_email(self, collection: str, username: str, email: str) -> bool:
        for doc in self._db.values():
            if doc.get("username") == username:
                return True
            if doc.get("email") == email:
                return True
        return False


