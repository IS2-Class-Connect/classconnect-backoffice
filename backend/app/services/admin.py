from typing import Optional
from app.databases.db import DB
from app.models.admin import AdminCreate, AdminOut
import bcrypt

class AdminService:
    def __init__(self, db: DB):
        self._db = db
        self._admin_coll = "admins"

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()

    async def create_admin(self, admin_data: AdminCreate) -> AdminOut:
        existing = await self._db.exists_with_username_email(self._admin_coll, admin_data.username, admin_data.email)
        if existing:
            raise ValueError("Username or email already exists")

        hashed_password = self.hash_password(admin_data.password)
        admin_dict = admin_data.model_dump()
        admin_dict["password"] = hashed_password

        admin =  await self._db.create(self._admin_coll, admin_dict)
        return AdminOut(**admin)

    async def get_admin(self, id: str) -> Optional[AdminOut]:
        admin = await self._db.find_one(self._admin_coll, id)
        return AdminOut(**admin) if admin else None

    async def get_all_admins(self) -> list[AdminOut]:
        return [AdminOut(**admin) for admin in await self._db.get_all(self._admin_coll)]
