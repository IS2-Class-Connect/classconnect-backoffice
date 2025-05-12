import datetime
from pydantic import BaseModel, EmailStr, Field


class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)


class AdminOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    registration_date: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
