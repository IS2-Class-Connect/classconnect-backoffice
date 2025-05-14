from typing import List
from pydantic import BaseModel, EmailStr

class CourseInEnrollment(BaseModel):
    id: int
    title: str
    startDate: str
    endDate: str

class EnrollmentOut(BaseModel):
    role: str
    course: CourseInEnrollment

class UserOut(BaseModel):
    uuid: str
    email: EmailStr
    name: str
    urlProfilePhoto: str
    description: str
    createdAt: str
    accountLockedByAdmins: bool
    enrollments: List[EnrollmentOut]