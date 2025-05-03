from app.services.auth import AuthService
from app.models.auth import AdminLogin, Token
from fastapi import HTTPException

class AuthController:
    def __init__(self, service: AuthService):
        self._service = service

    async def login(self, login_data: AdminLogin) -> Token:
        try:
            return await self._service.login_admin(login_data)
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Server error during login")
