from fastapi import APIRouter
from app.controllers.admin import AdminController
from app.models.admin import AdminCreate, AdminOut


class AdminRouter:
    def __init__(self, controller: AdminController):
        self._controller = controller
        self.router = APIRouter(prefix="/admins", tags=["admins"])

        self.router.post("/create", response_model=AdminOut)(self.create_admin)
        self.router.get("/{id}", response_model=AdminOut)(self.get_admin)
        self.router.get("", response_model=list[AdminOut])(self.get_all_admins)
        self.router.delete("/{id}", status_code=204)(self.delete_admin)

    async def create_admin(self, admin: AdminCreate):
        return await self._controller.create_admin(admin)

    async def get_admin(self, id: str):
        return await self._controller.get_admin(id)

    async def get_all_admins(self):
        return await self._controller.get_all_admins()

    async def delete_admin(self, id: str):
        return await self._controller.delete_admin(id)
