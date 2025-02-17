from fastapi import FastAPI
from database import engine, Base
from routes import student, courses, enrollments

# Initialize FastAPI app
app = FastAPI()

# Include routers for different modules
app.include_router(student.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
from auth import router as auth_router  # Import the auth router

# Add the router to the app
app.include_router(auth_router)

# Root endpoint
@app.get("/")
def home():
    return {"message": "Student Management API is running!"}

# Create tables in the database
Base.metadata.create_all(bind=engine)
