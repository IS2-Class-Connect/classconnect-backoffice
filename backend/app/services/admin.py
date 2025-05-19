from typing import Optional
from app.databases.db import DB
from app.exceptions.username_or_email import UsernameEmailInUser
from app.models.admin import AdminCreate, AdminOut, AdminLogin, Token
from app.models.users import UserOut, EnrollmentUsers, Enrollment, EnrollmentUpdate
import bcrypt
from fastapi import HTTPException
from datetime import datetime, timedelta
import jwt
import requests

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AdminService:
    def __init__(self, db: DB, admin_token: str, gateway_url: str):
        self._db = db
        self._admin_coll = "admins"
        self._admin_token = admin_token
        self._gateway_url = gateway_url

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    async def create_admin(self, admin_data: AdminCreate) -> AdminOut:
        existing = await self._db.exists_with_username_email(
            self._admin_coll, admin_data.username, admin_data.email
        )
        if existing:
            raise UsernameEmailInUser()

        hashed_password = self.hash_password(admin_data.password)
        admin_dict = admin_data.model_dump()
        admin_dict["password"] = hashed_password
        admin_dict["registration_date"] = datetime.utcnow().isoformat() + "Z"

        admin = await self._db.create(self._admin_coll, admin_dict)
        return AdminOut(**admin)

    async def get_admin(self, id: str) -> Optional[AdminOut]:
        admin = await self._db.find_one(self._admin_coll, id)
        return AdminOut(**admin) if admin else None

    async def get_all_admins(self) -> list[AdminOut]:
        return [AdminOut(**admin) for admin in await self._db.get_all(self._admin_coll)]

    async def delete_admin(self, id: str):
        return await self._db.delete(self._admin_coll, id)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    def create_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": expire})
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    async def login_admin(self, login_data: AdminLogin) -> Token:
        admin = await self._db.find_one_by_filter(
            self._admin_coll, {"email": login_data.email}
        )
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.verify_password(login_data.password, admin["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = self.create_token({"sub": str(admin["_id"]), "email": admin["email"]})
        return Token(access_token=token)

    async def get_all_users(self) -> list[UserOut]:
        url = f"{self._gateway_url}/admin-backend/users"
        headers = {"Authorization": f"Bearer {self._admin_token}"}

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            return [UserOut(**user) for user in res.json()]
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=502, detail="Failed to connect to users service"
            )

    async def get_all_users_enrollment(self) ->  list[Enrollment]:
        url = f"{self._gateway_url}/admin-backend/courses/enrollments"
        headers = {"Authorization": f"Bearer {self._admin_token}"}

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()  
            print(data)
            return EnrollmentUsers(**data).data
        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=502, detail="Failed to connect to education service"
            )


    async def update_user_lock_status(self, uuid: str, locked: bool):
        url = f"{self._gateway_url}/admin-backend/users/{uuid}/lock-status"
        headers = {"Authorization": f"Bearer {self._admin_token}"}
        data = {"locked": locked}

        try:
            res = requests.patch(url, json=data, headers=headers, timeout=5)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=502, detail="Failed to connect to users service")

    async def update_user_enrollment(self,courseId: str, uuid: str, enrollmentData: EnrollmentUpdate):
        url = f"{self._gateway_url}/admin-backend/courses/{courseId}/enrollments/{uuid}"
        headers = {"Authorization": f"Bearer {self._admin_token}"}
        data = {"role": enrollmentData.role}

        try:
            res = requests.patch(url, json=data, headers=headers, timeout=5)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=502, detail="Failed to connect to education service")
