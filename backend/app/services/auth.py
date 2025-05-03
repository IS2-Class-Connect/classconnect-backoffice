# app/services/auth.py
from app.models.auth import AdminLogin, Token
from app.models.admin import AdminOut
from app.databases.db import DB
from fastapi import HTTPException
from datetime import datetime, timedelta
import bcrypt
import jwt 

SECRET_KEY = "secret" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self, db: DB):
        self._db = db
        self._admin_coll = "admins"

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    def create_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": expire})
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    async def login_admin(self, login_data: AdminLogin) -> Token:
        admin = await self._db._db[self._admin_coll].find_one({"email": login_data.email})
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not self.verify_password(login_data.password, admin["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = self.create_token({"sub": str(admin["_id"]), "email": admin["email"]})
        return Token(access_token=token)
