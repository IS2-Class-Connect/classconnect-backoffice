from fastapi import APIRouter
from app.controllers.admin import AdminController
from app.controllers.metrics import MetricsController
from app.models.admin import AdminCreate, AdminOut, AdminLogin, Token
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
from app.models.admin import LockStatusUpdate
import logging


class AdminRouter:
    def __init__(self, controller: AdminController):
        self._controller = controller
        self._metrics_controller = MetricsController()
        self.router = APIRouter(prefix="/admins", tags=["admins"])

        self.router.get("/metrics")(self.get_metrics)
        self.router.get("/users", response_model=list[UserOut])(self.get_all_users)
        self.router.get("", response_model=list[AdminOut])(self.get_all_admins)
        self.router.get("/{id}", response_model=AdminOut)(self.get_admin)
        self.router.get("/courses/enrollments", response_model=list[Enrollment])(
            self.get_all_users_enrollment
        )
        self.router.post("/login", response_model=Token)(self.login)
        self.router.post("", response_model=AdminOut, status_code=201)(
            self.create_admin
        )
        self.router.delete("/{id}", status_code=204)(self.delete_admin)
        self.router.patch("/users/{uuid}/lock-status")(self.update_user_lock_status)
        self.router.patch("/courses/{courseId}/enrollments/{uuid}")(
            self.update_user_enrollment
        )

    async def login(self, login_data: AdminLogin):
        logging.info(f"Trying to login for admin {login_data.email}")
        return await self._controller.login(login_data)

    async def create_admin(self, admin: AdminCreate):
        logging.info(f"Trying to create an admin {admin.email}")
        return await self._controller.create_admin(admin)

    async def get_admin(self, id: str):
        logging.info(f"Trying to get an admin {id}")
        return await self._controller.get_admin(id)

    async def get_all_admins(self):
        logging.info(f"Trying to get all admins")
        return await self._controller.get_all_admins()

    async def delete_admin(self, id: str):
        logging.info(f"Trying to delete an admin {id}")
        return await self._controller.delete_admin(id)

    async def get_all_users(self):
        logging.info(f"Trying to get all the users")
        return await self._controller.get_all_users()

    async def get_all_users_enrollment(self):
        logging.info(f"Trying to get all user enrollments")
        return await self._controller.get_all_users_enrollment()

    async def update_user_lock_status(self, uuid: str, payload: LockStatusUpdate):
        status = "locked" if payload.locked else "unlocked"
        logging.info(f"Trying to update user status for user {uuid} to {status}")
        return await self._controller.update_user_lock_status(uuid, payload.locked)

    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        logging.info(f"Trying to update user enrollment for user {uuid}")
        return await self._controller.update_user_enrollment(
            uuid, courseId, enrollmentData
        )

    async def get_metrics(self):
        logging.info("Trying to get metrics")
        return self._metrics_controller.get_metrics()
