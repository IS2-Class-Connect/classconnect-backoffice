from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.users import UserOut, EnrollmentUpdate, Enrollment
from app.models.admin import (
    AdminCreate,
    AdminLogin,
    AdminOut,
    Token,
    RuleCreate,
    RuleOut,
    RuleUpdate,
)


class Service(ABC):
    @abstractmethod
    async def create_admin(self, data: AdminCreate) -> AdminOut:
        pass

    @abstractmethod
    async def get_admin(self, id: str) -> Optional[AdminOut]:
        pass

    @abstractmethod
    async def get_all_admins(self) -> List[AdminOut]:
        pass

    @abstractmethod
    async def delete_admin(self, id: str) -> bool:
        pass

    @abstractmethod
    async def login_admin(self, credentials: AdminLogin) -> Token:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[UserOut]:
        pass

    @abstractmethod
    async def get_all_users_enrollment(self) -> List[Enrollment]:
        pass

    @abstractmethod
    async def update_user_lock_status(self, uuid: str, locked: bool):
        pass

    @abstractmethod
    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        pass

    @abstractmethod
    async def create_rule(self, data: RuleCreate) -> RuleOut:
        pass

    @abstractmethod
    async def get_all_rules(self) -> list[RuleOut]:
        pass

    @abstractmethod
    async def get_rule(self, id: str) -> Optional[RuleOut]:
        pass

    @abstractmethod
    async def update_rule(self, id: str, data: RuleUpdate):
        pass
