from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.controllers.admin import AdminController
from app.controllers.metrics import MetricsController
from app.models.admin import (
    AdminCreate,
    AdminOut,
    AdminLogin,
    Token,
    LockStatusUpdate,
    RuleCreate,
    RuleOut,
    RuleUpdateWithAdminName,
)
from app.models.users import UserOut, Enrollment, EnrollmentUpdate
import logging
import jwt

security = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"


def validate_token_with_secret_key(secret_key: str):
    def validate_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication credentials were provided",
            )

        try:
            token = credentials.credentials
            return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

    return validate_token


class AdminRouter:
    def __init__(self, controller: AdminController, secret_key: str):
        self._controller = controller
        self._metrics_controller = MetricsController()
        self.router = APIRouter(prefix="/admins", tags=["admins"])

        # Unprotected
        self.router.get("/metrics")(self.get_metrics)
        self.router.post("/login", response_model=Token)(self.login)
        self.router.get("/rules", response_model=list[RuleOut])(self.get_all_rules)

        # Protected
        # dependencies = [Depends(validate_token_with_secret_key(secret_key))]
        dependencies = []
        self.router.get(
            "/users",
            response_model=list[UserOut],
            dependencies=dependencies,
        )(self.get_all_users)

        self.router.get(
            "",
            response_model=list[AdminOut],
            dependencies=dependencies,
        )(self.get_all_admins)

        self.router.post(
            "/rules",
            status_code=201,
            dependencies=dependencies,
            response_model=RuleOut,
        )(self.create_rule)

        self.router.get(
            "/courses/enrollments",
            response_model=list[Enrollment],
            dependencies=dependencies,
        )(self.get_all_users_enrollment)

        self.router.post(
            "",
            response_model=AdminOut,
            status_code=201,
            dependencies=dependencies,
        )(self.create_admin)

        self.router.post(
            "/rules/notify",
            status_code=204,
            dependencies=dependencies,
        )(self.notify_rules)

        self.router.delete(
            "/{id}",
            status_code=204,
            dependencies=dependencies,
        )(self.delete_admin)

        self.router.patch(
            "/users/{uuid}/lock-status",
            dependencies=dependencies,
        )(self.update_user_lock_status)

        self.router.patch(
            "/courses/{courseId}/enrollments/{uuid}",
            dependencies=dependencies,
        )(self.update_user_enrollment)

        self.router.get(
            "/{id}",
            response_model=AdminOut,
            dependencies=dependencies,
        )(self.get_admin)

        self.router.get(
            "/rules/{id}",
            response_model=RuleOut,
            dependencies=dependencies,
        )(self.get_rule)

        self.router.patch(
            "/rules/{id}",
            dependencies=dependencies,
        )(self.update_rule)

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
        return self._metrics_controller.get_metrics()

    async def create_rule(self, rule: RuleCreate):
        logging.info(f"Trying to create a new rule with title {rule.title}")
        return await self._controller.create_rule(rule)

    async def get_all_rules(self):
        logging.info("Trying to get all rules")
        return await self._controller.get_all_rules()

    async def update_rule(self, id: str, update: RuleUpdateWithAdminName):
        admin_name = update.admin_name
        rule_update = update.update
        logging.info(f"Trying to update rule with id: {id}, by {admin_name}")
        return await self._controller.update_rule(id, admin_name, rule_update)

    async def get_rule(self, id: str):
        logging.info(f"Trying to get rule with id: {id}")
        return await self._controller.get_rule(id)

    async def notify_rules(self):
        logging.info(f"Trying to notify rules")
        return await self._controller.notify_rules()
