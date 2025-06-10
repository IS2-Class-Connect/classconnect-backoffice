from abc import abstractmethod, ABC
from typing import Any, Optional


class DB(ABC):
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    async def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, collection: str, id: str, data: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def find_one(self, collection: str, id: str) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    async def find_one_by_filter(
        self, collection: str, filter: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    async def get_all(self, collection: str) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(self, collection: str, id: str) -> bool:
        pass

    @abstractmethod
    async def exists_with_username_email(
        self, collection: str, username: str, email: str
    ) -> bool:
        pass

    @abstractmethod
    async def exists_with_title(self, collection: str, title: str) -> bool:
        pass
