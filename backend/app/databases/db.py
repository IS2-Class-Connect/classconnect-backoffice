import abc
from typing import Any, Optional

class DB(abc.ABC):
    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    async def find_one(self, collection: str, id: str) -> Optional[dict[str, Any]]:
        pass

    @abc.abstractmethod
    async def get_all(self, collection: str) -> list[dict[str, Any]]:
        pass

    @abc.abstractmethod
    async def exists_with_username_email(self, collection: str, username: str, email: str) -> bool:
        pass

    @abc.abstractmethod
    async def delete(self, collection: str, id: str) -> bool:
        pass
