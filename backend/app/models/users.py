from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    email: EmailStr
    name: str
    urlProfilePhoto: str
    description: str