from fastapi import APIRouter, Body
from app.controllers.admin import AdminController
from app.models.admin import AdminCreate, AdminOut, AdminLogin, Token
from app.models.users import UserOut, EnrollmentUsers, Enrollment, EnrollmentUpdate
from app.models.admin import LockStatusUpdate


class AdminRouter:
    def __init__(self, controller: AdminController):
        self._controller = controller
        self.router = APIRouter(prefix="/admins", tags=["admins"])

        self.router.post("", response_model=AdminOut, status_code=201)(
            self.create_admin
        )
        self.router.get("/users", response_model=list[UserOut])(self.get_all_users)
        self.router.get("/{id}", response_model=AdminOut)(self.get_admin)
        self.router.get("", response_model=list[AdminOut])(self.get_all_admins)
        self.router.delete("/{id}", status_code=204)(self.delete_admin)
        self.router.post("/login", response_model=Token)(self.login)
        self.router.patch("/users/{uuid}/lock-status")(self.update_user_lock_status)
        self.router.get("/courses/enrollments", response_model=list[Enrollment])(self.get_all_users_enrollment)
        self.router.patch("/courses/{courseId}/enrollments/{uuid}")(self.update_user_enrollment)

    async def login(self, login_data: AdminLogin):
        return await self._controller.login(login_data)

    async def create_admin(self, admin: AdminCreate):
        return await self._controller.create_admin(admin)

    async def get_admin(self, id: str):
        return await self._controller.get_admin(id)

    async def get_all_admins(self):
        return await self._controller.get_all_admins()

    async def delete_admin(self, id: str):
        return await self._controller.delete_admin(id)

    async def get_all_users(self):
        return await self._controller.get_all_users()

    async def get_all_users_enrollment(self):
        return await self._controller.get_all_users_enrollment()

    async def update_user_lock_status(self, uuid: str, payload: LockStatusUpdate):
        return await self._controller.update_user_lock_status(uuid, payload.locked)
    
    async def update_user_enrollment(self,courseId: str, uuid: str, enrollmentData: EnrollmentUpdate):
        return await self._controller.update_user_enrollment(uuid,courseId,enrollmentData)
