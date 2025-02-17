

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, models
from database import get_db
from auth import get_current_user

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


router = APIRouter(prefix="/courses", tags=["courses"])

# ✅ Create a course with validation
@router.post("/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    # Check if course name already exists
    existing_course = db.query(models.Course).filter(models.Course.name == course.name).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course name already exists")

    return crud.create_course(db=db, course=course)

# ✅ Get all courses
@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = crud.get_courses(db=db)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses

# ✅ Get a single course by ID
@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db=db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ✅ Delete a course
@router.delete("/{course_id}", response_model=schemas.CourseResponse)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db=db, course_id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return crud.delete_course(db=db, course_id=course_id)
