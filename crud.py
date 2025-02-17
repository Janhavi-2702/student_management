from sqlalchemy.orm import Session
import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(name=student.name, age=student.age, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session):
    return db.query(models.Student).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student

def get_courses(db: Session):
    return db.query(models.Course).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def delete_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
    return course
def enroll_student(db: Session, enrollment_data: schemas.EnrollmentCreate):
    enrollment = models.Enrollment(
        student_id=enrollment_data.student_id,
        course_id=enrollment_data.course_id
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return {"message": "Enrollment successful"}

def get_student_courses(db: Session, student_id: int):
    courses = db.query(models.Enrollment.course_id).filter(models.Enrollment.student_id == student_id).all()
    return {"enrolled_courses": [course[0] for course in courses]}