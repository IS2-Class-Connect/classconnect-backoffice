from fastapi import HTTPException
from app.exceptions.username_or_email import UsernameEmailInUser
from app.models.admin import AdminCreate, AdminOut, AdminLogin, Token, UserOut
from app.services.admin import AdminService


class AdminController:
    def __init__(self, service: AdminService):
        self._service = service

    async def create_admin(self, admin: AdminCreate) -> AdminOut:
        try:
            created_admin = await self._service.create_admin(admin)
            return created_admin
        except UsernameEmailInUser as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=500, detail="Failed to create admin due to server error"
            )

    async def get_admin(self, id: str) -> AdminOut:
        try:
            admin = await self._service.get_admin(id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=500, detail="Failed to retrieve admin due to server error"
            )
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found")

        return admin

    async def get_all_admins(self) -> list[AdminOut]:
        try:
            return await self._service.get_all_admins()
        except Exception:
            raise HTTPException(
                status_code=500, detail="Failed to create admin due to server error"
            )

    async def delete_admin(self, id: str):
        try:
            found = await self._service.delete_admin(id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=500, detail="Failed to create admin due to server error"
            )
        if not found:
            raise HTTPException(status_code=404, detail="Admin not found")

    async def login(self, login_data: AdminLogin) -> Token:
        try:
            return await self._service.login_admin(login_data)
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Server error during login")

    async def get_all_users(self) -> list[UserOut]:
        try:
            return await self._service.get_all_users()
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500, detail="Server error during get all users"
            )
