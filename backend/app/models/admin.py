from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


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


class LockStatusUpdate(BaseModel):
    locked: bool


class RuleCreate(BaseModel):
    title: str
    description: str
    effective_date: str
    applicable_conditions: List[str]


class RuleOut(RuleCreate):
    id: str


class RuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    effective_date: Optional[str] = None
    applicable_conditions: Optional[List[str]] = None


class RuleUpdateWithAdminName(BaseModel):
    admin_name: str
    update: RuleUpdate


class RulePacket(BaseModel):
    rules: List[RuleOut]
