from typing import Any, Optional, override
from app.databases.db import DB
from collections import defaultdict
from uuid import uuid4


class DictDB(DB):
    def __init__(self):
        self._db = defaultdict(dict)

    @override
    def close(self):
        pass

    @override
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        id = str(uuid4())
        full_data = {"id": id, **data}
        self._db[collection][id] = full_data
        return full_data

    @override
    async def find_one(self, collection: str, id: str) -> Optional[dict[str, Any]]:
        return self._db[collection].get(id)

    @override
    async def get_all(self, collection: str) -> list[dict[str, Any]]:
        return list(self._db[collection].values())

    @override
    async def exists_with_username_email(
        self, collection: str, username: str, email: str
    ) -> bool:
        for doc in self._db[collection].values():
            if doc.get("username") == username:
                return True
            if doc.get("email") == email:
                return True
        return False

    @override
    async def delete(self, collection: str, id: str) -> bool:
        return self._db[collection].pop(id, None) is not None

    @override
    async def find_one_by_filter(
        self, collection: str, filter: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        for doc in self._db[collection].values():
            if all(doc.get(k) == v for k, v in filter.items()):
                return doc
        return None
