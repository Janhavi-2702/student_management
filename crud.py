from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

# Create a new student
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, age=student.age, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Get all students
def get_students(db: Session):
    return db.query(models.Student).all()

# Get a specific student by ID
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# Update an existing student
def update_student(db: Session, student_id: int, student_data: schemas.StudentCreate):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = student_data.name
    student.age = student_data.age
    student.email = student_data.email
    db.commit()
    db.refresh(student)
    return student

# Delete a student
def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return student

# Get all courses
def get_courses(db: Session):
    return db.query(models.Course).all()

# Get a specific course by ID
def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

# Delete a course
def delete_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return course

# Enroll a student in a course
def enroll_student(db: Session, enrollment_data: schemas.EnrollmentCreate):
    enrollment = models.Enrollment(
        student_id=enrollment_data.student_id,
        course_id=enrollment_data.course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {"message": "Enrollment successful"}

# Get courses for a specific student
def get_student_courses(db: Session, student_id: int):
    courses = db.query(models.Enrollment.course_id).filter(models.Enrollment.student_id == student_id).all()
    return {"enrolled_courses": [course[0] for course in courses]}
