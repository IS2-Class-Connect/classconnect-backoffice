from fastapi import HTTPException
from app.exceptions.username_or_email import UsernameEmailInUser
from app.exceptions.rule_title_in_use import TitleAlreadyInUse
from app.models.admin import (
    AdminCreate,
    AdminOut,
    AdminLogin,
    Token,
    RuleCreate,
    RuleOut,
    RuleUpdate,
)
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.services.service import Service


class AdminController:
    def __init__(self, service: Service):
        self._service = service

    async def create_admin(self, admin: AdminCreate) -> AdminOut:
        try:
            return await self._service.create_admin(admin)
        except UsernameEmailInUser as e:
            raise HTTPException(status_code=409, detail=str(e))

    async def get_admin(self, id: str) -> AdminOut:
        try:
            admin = await self._service.get_admin(id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found")

        return admin

    async def get_all_admins(self) -> list[AdminOut]:
        return await self._service.get_all_admins()

    async def delete_admin(self, id: str):
        try:
            found = await self._service.delete_admin(id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        if not found:
            raise HTTPException(status_code=404, detail="Admin not found")

    async def login(self, login_data: AdminLogin) -> Token:
        return await self._service.login_admin(login_data)

    async def get_all_users(self) -> list[UserOut]:
        return await self._service.get_all_users()

    async def update_user_lock_status(self, uuid: str, locked: bool):
        return await self._service.update_user_lock_status(uuid, locked)

    async def get_all_users_enrollment(self) -> list[Enrollment]:
        return await self._service.get_all_users_enrollment()

    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        return await self._service.update_user_enrollment(
            uuid, courseId, enrollmentData
        )

    async def create_rule(self, rule: RuleCreate) -> RuleOut:
        try:
            return await self._service.create_rule(rule)
        except TitleAlreadyInUse as e:
            raise HTTPException(status_code=409, detail=str(e))

    async def get_all_rules(self) -> list[RuleOut]:
        return await self._service.get_all_rules()

    async def get_rule(self, id: str) -> RuleOut:
        try:
            rule = await self._service.get_rule(id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        if rule is None:
            raise HTTPException(status_code=404, detail="Rule not found")

        return rule

    async def update_rule(self, id: str, admin_name: str, rule: RuleUpdate):
        return await self._service.update_rule(id, admin_name, rule)

    async def notify_rules(self):
        return await self._service.notify_rules()
