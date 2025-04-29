from fastapi import HTTPException
from app.models.admin import AdminCreate
from app.services.admin import AdminService


class Controller:
    def __init__(self, service: AdminService):
        self._service = service

    async def register_admin(self, admin: AdminCreate):
        """
        Endpoint to register a new admin.
        - It accepts admin registration data and checks if the username or email already exists.
        - If registration is successful, the new admin data (with a hashed password) is returned.
        """
        try:
            created_admin = await self._service.create_admin(admin)
            return created_admin
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create admin due to server error.")

    async def get_admin(self, admin_id: str):
        """
        Endpoint to get an admin by their ID.
        - Returns the admin details.
        """
        admin = await self._service._db.find_one("admins", {"id": admin_id})
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found.")
        return admin

