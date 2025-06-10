from typing import Optional, override
from app.databases.db import DB
from app.exceptions.username_or_email import UsernameEmailInUser
from app.exceptions.rule_title_in_use import TitleAlreadyInUse
from app.models.users import UserOut, EnrollmentUsers, Enrollment, EnrollmentUpdate
from app.services.service import Service
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.models.admin import (
    AdminCreate,
    AdminOut,
    AdminLogin,
    Token,
    RuleCreate,
    RuleOut,
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
    async def get_all_users(self) -> list[UserOut]:
        url = f"{self._gateway_url}/admin-backend/users"
        headers = {"Authorization": f"Bearer {self._gateway_token}"}

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            return [UserOut(**user) for user in res.json()]
        except Exception:
            raise HTTPException(
                status_code=502, detail="Failed to connect to users service"
            )

    @override
    async def get_all_users_enrollment(self) -> list[Enrollment]:
        url = f"{self._gateway_url}/admin-backend/courses/enrollments"
        headers = {"Authorization": f"Bearer {self._gateway_token}"}

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()
            return EnrollmentUsers(**data).data
        except Exception:
            raise HTTPException(
                status_code=502, detail="Failed to connect to education service"
            )

    @override
    async def update_user_lock_status(self, uuid: str, locked: bool):
        url = f"{self._gateway_url}/admin-backend/users/{uuid}/lock-status"
        headers = {"Authorization": f"Bearer {self._gateway_token}"}
        data = {"locked": locked}

        try:
            res = requests.patch(url, json=data, headers=headers, timeout=5)
            res.raise_for_status()
            status = "locked" if locked else "unlocked"
            logging.info(f"{status} user {uuid}")
            return res.json()
        except Exception:
            raise HTTPException(
                status_code=502, detail="Failed to connect to users service"
            )

    @override
    async def update_user_enrollment(
        self, courseId: str, uuid: str, enrollmentData: EnrollmentUpdate
    ):
        url = f"{self._gateway_url}/admin-backend/courses/{courseId}/enrollments/{uuid}"
        headers = {"Authorization": f"Bearer {self._gateway_token}"}
        data = {"role": enrollmentData.role}

        try:
            res = requests.patch(url, json=data, headers=headers, timeout=5)
            res.raise_for_status()
            logging.info(
                f"updated role for user {uuid} to {enrollmentData.role} at course {courseId}"
            )
            return res.json()
        except Exception:
            raise HTTPException(
                status_code=502, detail="Failed to connect to education service"
            )

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
