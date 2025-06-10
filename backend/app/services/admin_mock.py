from typing import Optional, override
from app.models.admin import (
    AdminCreate,
    AdminOut,
    AdminLogin,
    Token,
    RuleCreate,
    RuleOut,
)
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.services.service import Service
from app.services.admin import AdminService
from fastapi import HTTPException


class AdminMockService(Service):
    def __init__(
        self,
        service: AdminService,
        users: dict[str, UserOut],
        enrollments: dict[str, dict[str, Enrollment]],
    ):
        self._inner = service
        self._users = users
        self._enrollments = enrollments

    @override
    async def create_admin(self, data: AdminCreate) -> AdminOut:
        return await self._inner.create_admin(data)

    @override
    async def get_admin(self, id: str) -> Optional[AdminOut]:
        return await self._inner.get_admin(id)

    @override
    async def get_all_admins(self) -> list[AdminOut]:
        return await self._inner.get_all_admins()

    @override
    async def delete_admin(self, id: str):
        return await self._inner.delete_admin(id)

    @override
    async def login_admin(self, credentials: AdminLogin) -> Token:
        return await self._inner.login_admin(credentials)

    @override
    async def get_all_users(self) -> list[UserOut]:
        return list(self._users.values())

    @override
    async def get_all_users_enrollment(self) -> list[Enrollment]:
        return [
            enrollment
            for user_enrollments in self._enrollments.values()
            for enrollment in user_enrollments.values()
        ]

    @override
    async def update_user_lock_status(self, uuid: str, locked: bool):
        if uuid not in self._users:
            raise HTTPException(404, "uuid was not found in users db")
        self._users[uuid].accountLockedByAdmins = locked

    @override
    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        if uuid not in self._enrollments:
            raise HTTPException(404, "uuid not found in enrollments")
        if courseId not in self._enrollments[uuid]:
            raise HTTPException(404, "courseId not found in user's enrollments")
        self._enrollments[uuid][courseId].role = enrollmentData.role

    @override
    async def create_rule(self, data: RuleCreate) -> RuleOut:
        return await self._inner.create_rule(data)

    @override
    async def get_all_rules(self) -> list[RuleOut]:
        return await self._inner.get_all_rules()
