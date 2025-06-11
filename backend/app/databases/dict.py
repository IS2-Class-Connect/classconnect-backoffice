from typing import Any, Optional, override, Dict, Tuple
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
    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        id = str(uuid4())
        full_data = {"id": id, **data}
        self._db[collection][id] = full_data
        return full_data

    @override
    async def update(
        self, collection: str, id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        value = self._db[collection].get(id)
        if not value:
            return None

        self._db[collection][id] = {**value, **data}
        return value

    @override
    async def find_one(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        return self._db[collection].get(id)

    @override
    async def find_one_by_filter(
        self, collection: str, filter: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        for doc in self._db[collection].values():
            if all(doc.get(k) == v for k, v in filter.items()):
                return doc
        return None

    @override
    async def get_all(self, collection: str) -> list[Dict[str, Any]]:
        return list(self._db[collection].values())

    @override
    async def delete(self, collection: str, id: str) -> bool:
        return self._db[collection].pop(id, None) is not None

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
    async def exists_with_title(self, collection: str, title: str) -> bool:
        for doc in self._db[collection].values():
            if doc.get("title") == title:
                return True
        return False
