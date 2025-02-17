from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import get_db

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

# ✅ Enroll a student in a course with validation
@router.post("/", response_model=schemas.EnrollmentResponse)
def enroll_student(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    # 📌 Check if Student Exists
    student = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 📌 Check if Course Exists
    course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 📌 Prevent Duplicate Enrollment
    existing_enrollment = (
        db.query(models.Enrollment)
        .filter(
            models.Enrollment.student_id == enrollment.student_id,
            models.Enrollment.course_id == enrollment.course_id
        )
        .first()
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    # 📌 Create Enrollment
    new_enrollment = models.Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

# ✅ Fetch all enrollments
@router.get("/", response_model=list[schemas.EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    enrollments = db.query(models.Enrollment).all()
    if not enrollments:
        raise HTTPException(status_code=404, detail="No enrollments found")
    return enrollments

# ✅ Get Student's Enrolled Courses
@router.get("/students/{student_id}/courses", response_model=schemas.StudentCoursesResponse)
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    # 📌 Check if Student Exists
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # 📌 Fetch Enrolled Courses
    enrolled_courses = (
        db.query(models.Enrollment.course_id)
        .filter(models.Enrollment.student_id == student_id)
        .all()
    )

    if not enrolled_courses:
        raise HTTPException(status_code=404, detail="No enrolled courses found for this student")

    return {"student_id": student_id, "enrolled_courses": [course_id for (course_id,) in enrolled_courses]}
