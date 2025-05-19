from typing import List
from pydantic import BaseModel, EmailStr

class Course(BaseModel):
    id: int
    title: str

class Enrollment(BaseModel):
    role: str
    userId: str
    course: Course

class EnrollmentUsers(BaseModel):
    data: List[Enrollment]

class EnrollmentUpdate(BaseModel):
    role: str

class UserOut(BaseModel):
    uuid: str
    email: EmailStr
    name: str
    urlProfilePhoto: str
    description: str
    createdAt: str
    accountLockedByAdmins: bool
