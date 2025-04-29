from fastapi import APIRouter
from app.controllers.admin import Controller
from app.models.admin import AdminCreate, AdminOut

class AdminRouter:
    def __init__(self, controller: Controller):
        self._controller = controller
        self.router = APIRouter(prefix="/admin", tags=["admin"])

        self.router.post("/register", response_model=AdminOut)(self.register_admin)
        self.router.get("/{admin_id}", response_model=AdminOut)(self.get_admin)

    async def register_admin(self, admin: AdminCreate):
        return await self._controller.register_admin(admin)

    async def get_admin(self, admin_id: str):
        return await self._controller.get_admin(admin_id)

