from typing import Optional, override, Callable
from app.databases.db import DB
from app.exceptions.username_or_email import UsernameEmailInUser
from app.exceptions.rule_title_in_use import TitleAlreadyInUse
from app.models.users import UserOut, EnrollmentUsers, Enrollment, EnrollmentUpdate
from app.services.service import Service
from fastapi import HTTPException
from datetime import datetime, timedelta
from requests import HTTPError, Response
from app.models.admin import (
    AdminCreate,
    AdminOut,
    AdminLogin,
    Token,
    RuleCreate,
    RuleOut,
    RuleUpdate,
    RulePacket,
)
import bcrypt
import jwt
import requests
import logging

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AdminService(Service):
    def __init__(self, db: DB, gateway_token: str, gateway_url: str, jwt_secret: str):
        self._db = db
        self._admin_coll = "admins"
        self._rule_coll = "rules"
        self._gateway_token = gateway_token
        self._gateway_url = gateway_url
        self._secret = jwt_secret

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    @override
    async def create_admin(self, data: AdminCreate) -> AdminOut:
        existing = await self._db.exists_with_username_email(
            self._admin_coll, data.username, data.email
        )
        if existing:
            raise UsernameEmailInUser()

        hashed_password = self.hash_password(data.password)
        admin_dict = data.model_dump()
        admin_dict["password"] = hashed_password
        admin_dict["registration_date"] = datetime.utcnow().isoformat() + "Z"

        admin = await self._db.create(self._admin_coll, admin_dict)
        return AdminOut(**admin)

    @override
    async def get_admin(self, id: str) -> Optional[AdminOut]:
        admin = await self._db.find_one(self._admin_coll, id)
        return AdminOut(**admin) if admin else None

    @override
    async def get_all_admins(self) -> list[AdminOut]:
        return [
            AdminOut(**admin) for admin in (await self._db.get_all(self._admin_coll))
        ]

    @override
    async def delete_admin(self, id: str):
        return await self._db.delete(self._admin_coll, id)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    def create_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": expire})
        return jwt.encode(data, self._secret, algorithm=ALGORITHM)

    @override
    async def login_admin(self, credentials: AdminLogin) -> Token:
        admin = await self._db.find_one_by_filter(
            self._admin_coll, {"email": credentials.email}
        )
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.verify_password(credentials.password, admin["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self.create_token({"sub": str(admin["id"]), "email": admin["email"]})
        return Token(access_token=token)

    @override
    async def create_rule(self, data: RuleCreate) -> RuleOut:
        existing = await self._db.exists_with_title(self._rule_coll, data.title)
        if existing:
            raise TitleAlreadyInUse()

        rule_dict = data.model_dump()
        rule = await self._db.create(self._rule_coll, rule_dict)
        return RuleOut(**rule)

    @override
    async def get_all_rules(self) -> list[RuleOut]:
        return [RuleOut(**rule) for rule in (await self._db.get_all(self._rule_coll))]

    @override
    async def get_rule(self, id: str) -> Optional[RuleOut]:
        rule = await self._db.find_one(self._rule_coll, id)
        return RuleOut(**rule) if rule else None

    @override
    async def update_rule(self, id: str, admin_name: str, data: RuleUpdate):
        rule_dict = data.model_dump(exclude_unset=True)

        prev = await self._db.update(self._rule_coll, id, rule_dict)
        if not prev:
            raise HTTPException(404, "The provided rule id doesn't exist")

        changes = []
        for field, new_value in rule_dict.items():
            change = f"{field}:\n\tfrom: `{prev[field]}`\n\tto:   `{new_value}`"
            changes.append(change)

        changes_fmt = "\n".join(changes)
        logging.info(f"{admin_name} made changes to rule id: {id}:\n{changes_fmt}")

    async def _send_to_gateway_through_admin_backend(
        self, method: Callable, endpoint: str, **kwargs
    ) -> Response:
        endpoint = f"/admin-backend{endpoint}"
        return await self._send_to_gateway_directly(method, endpoint, **kwargs)

    @override
    async def get_all_users(self) -> list[UserOut]:
        endpoint = "/users"
        res = await self._send_to_gateway_through_admin_backend(requests.get, endpoint)
        return [UserOut(**user) for user in res.json()]

    @override
    async def get_all_users_enrollment(self) -> list[Enrollment]:
        endpoint = "/courses/enrollments"
        res = await self._send_to_gateway_through_admin_backend(requests.get, endpoint)
        return EnrollmentUsers(**res.json()).data

    @override
    async def update_user_lock_status(self, uuid: str, locked: bool):
        endpoint = f"/users/{uuid}/lock-status"
        data = {"locked": locked}
        await self._send_to_gateway_through_admin_backend(
            requests.patch, endpoint, json=data
        )
        status = "locked" if locked else "unlocked"
        logging.info(f"{status} user {uuid}")

    @override
    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        endpoint = f"/courses/{courseId}/enrollments/{uuid}"
        data = {"role": enrollmentData.role}
        await self._send_to_gateway_through_admin_backend(
            requests.patch, endpoint, json=data
        )
        logging.info(
            f"updated role for user {uuid} to {enrollmentData.role} at course {courseId}"
        )

    async def _send_to_gateway_directly(
        self, method: Callable, endpoint: str, **kwargs
    ) -> Response:
        url = f"{self._gateway_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self._gateway_token}"}
        try:
            res: Response = method(
                **{"url": url, "headers": headers, "timeout": 5, **kwargs}
            )
            res.raise_for_status()
            return res
        except HTTPError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.reason
            )

    @override
    async def notify_rules(self):
        rules = await self.get_all_rules()
        endpoint = "/email/rules"
        data = RulePacket(rules=rules).model_dump()
        await self._send_to_gateway_directly(requests.post, endpoint, json=data)
        logging.info("sent notification for rules")
