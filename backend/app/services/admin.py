from typing import Optional
from app.databases.db import DB
from app.models.admin import AdminCreate
import hashlib

class AdminService:
    def __init__(self, db: DB):
        self._db = db
        self._admin_coll = "admins"

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_admin(self, admin_data: AdminCreate) -> dict:
        existing = await self._db.exists_with_username_email(self._admin_coll, admin_data.username, admin_data.email)
        if existing:
            raise ValueError("Username or email already exists")

        hashed_password = self.hash_password(admin_data.password)
        admin_dict = admin_data.model_dump()
        admin_dict["password"] = hashed_password
        return await self._db.create(self._admin_coll, admin_dict)

    async def get_admin(self, id: str) -> Optional[dict]:
        return await self._db.find_one(self._admin_coll, id)

    async def get_all_admins(self) -> list:
        return await self._db.get_all(self._admin_coll)
