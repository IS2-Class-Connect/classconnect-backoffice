from app.services.auth import AuthService  
from app.controllers.auth import AuthController
from app.models.auth import AdminLogin, Token
from fastapi import APIRouter
class AuthRouter:
    def __init__(self, controller: AuthController):
        self._controller = controller
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.router.post("/login", response_model=Token)(self.login)

    async def login(self, login_data: AdminLogin):
        return await self._controller.login(login_data)

