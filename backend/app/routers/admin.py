from fastapi import APIRouter
from app.controllers.admin import AdminController
from app.models.admin import AdminCreate, AdminOut

class AdminRouter:
    def __init__(self, controller: AdminController):
        self._controller = controller
        self.router = APIRouter(prefix="/admin", tags=["admin"])

        self.router.post("/register", response_model=AdminOut)(self.register_admin)
        self.router.get("/{admin_id}", response_model=AdminOut)(self.get_admin)
        self.router.get("", response_model=)

    async def register_admin(self, admin: AdminCreate):
        return await self._controller.register_admin(admin)

    async def get_admin(self, admin_id: str):
        return await self._controller.get_admin(admin_id)

    async def get_all_admins(self):
        return await self._controller.get_all_admins()
