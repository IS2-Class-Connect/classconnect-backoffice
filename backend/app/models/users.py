from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    uuid: str
    email: EmailStr
    name: str
    urlProfilePhoto: str
    description: str
    createdAt: str
    accountLockedByAdmins: bool