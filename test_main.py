# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

# Create a TestClient instance using the app
@pytest.fixture
def client():
    client = TestClient(app)  # Create a test client instance for the FastAPI app
    return client

# Test case for the root endpoint
def test_home(client):
    response = client.get("/")  # Simulate a GET request to the root route
    assert response.status_code == 200  # Assert the response status is 200
    assert response.json() == {"message": "Student Management API is running!"}  # Assert the returned JSON

# Test case for GET /students (assuming student router has a route like this)
def test_get_students(client):
    response = client.get("/students")  # Simulate a GET request to the students route
    assert response.status_code == 200  # Assert the response status is 200
    assert isinstance(response.json(), list)  # Assert the response is a list (even if empty)

# Test case for POST /students (assuming student router has a route like this)
def test_add_student(client):
    student_data = {"id": 1, "name": "John Doe", "age": 20, "email": "john@gmail.com"}  # Example student data
    response = client.post("/students", json=student_data)  # Simulate a POST request to the root route "/"
    
    # Print the response content to help debug
    print(response.status_code)
    print(response.json())  # This will show any error message or success data
    
    assert response.status_code == 200  # Assert the response status code is 200
    assert response.json()["message"] == "Student added successfully"  # Assert success message
    assert response.json()["student"]["name"] == "John Doe"  # Assert the added student's name is correct

# Test case for GET /courses (assuming courses router has a route like this)
def test_get_courses(client):
    response = client.get("/courses")  # Simulate a GET request to get all courses
    assert response.status_code == 200  # Assert the response status is 200
    assert isinstance(response.json(), list)  # Assert the response is a list of courses

# Test case for GET /enrollments (assuming enrollments router has a route like this)
def test_get_enrollments(client):
    response = client.get("/enrollments")  # Simulate a GET request to get all enrollments
    assert response.status_code == 200  # Assert the response status is 200
    assert isinstance(response.json(), list)  # Assert the response is a list of enrollments

