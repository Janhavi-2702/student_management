

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import get_db
from auth import get_current_user
from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str

router = APIRouter(prefix="/students", tags=["Students"])

# ✅ Require authentication for modifying student data
@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.create_student(db=db, student=student)

@router.delete("/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    student = crud.delete_student(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

#router = APIRouter(prefix="/students", tags=["students"])

# ✅ Create a student with validation
@router.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_student(db=db, student=student)

# ✅ Get all students
@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = crud.get_students(db=db)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

# ✅ Get a student by ID with proper error handling
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ✅ Delete a student with validation
@router.delete("/{student_id}", response_model=schemas.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db=db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return crud.delete_student(db=db, student_id=student_id)
