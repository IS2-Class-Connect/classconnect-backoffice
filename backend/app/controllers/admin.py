from fastapi import HTTPException
from app.exceptions.username_or_email import UsernameEmailInUser
from app.models.admin import AdminCreate, AdminOut, AdminLogin, Token
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.services.service import Service


class AdminController:
    def __init__(self, service: Service):
        self._service = service

    async def create_admin(self, admin: AdminCreate) -> AdminOut:
        try:
            created_admin = await self._service.create_admin(admin)
            return created_admin
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
