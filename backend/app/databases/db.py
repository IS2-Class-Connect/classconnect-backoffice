from abc import abstractmethod, ABC
from typing import Any, Optional, Dict


class DB(ABC):
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(
        self, collection: str, id: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find_one(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find_one_by_filter(
        self, collection: str, filter: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_all(self, collection: str) -> list[Dict[str, Any]]:
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
