from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Correct for Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str


class CourseCreate(BaseModel):
    title: str
    description: str

class CourseResponse(CourseCreate):
    id: int

    class Config:
        from_attributes = True  # Ensures SQLAlchemy models work with Pydantic


class StudentBase(BaseModel):
    name: str
    age: int
    email: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(EnrollmentCreate):
    id: int

    class Config:
        from_attributes = True

class StudentCoursesResponse(BaseModel):
    enrolled_courses: List[int]
