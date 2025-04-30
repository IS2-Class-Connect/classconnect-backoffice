from fastapi import HTTPException
from app.models.admin import AdminCreate, AdminOut
from app.services.admin import AdminService


class AdminController:
    def __init__(self, service: AdminService):
        self._service = service

    async def create_admin(self, admin: AdminCreate) -> AdminOut:
        try:
            created_admin = await self._service.create_admin(admin)
            return created_admin
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=500, detail="Failed to create admin due to server error"
            )

    async def get_admin(self, id: str) -> AdminOut:
        admin = await self._service.get_admin(id)
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found")

        return admin

    async def get_all_admins(self) -> list[AdminOut]:
        return await self._service.get_all_admins()

    async def delete_admin(self, id: str):
        return await self._service.delete_admin(id)
