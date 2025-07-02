import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to FastAPI Jumpstart!"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_user():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_user():
    # First registration
    client.post(
        "/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword"
        }
    )
    
    # Duplicate registration
    response = client.post(
        "/register",
        json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 400

def test_login():
    # Register user first
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword"
        }
    )
    
    # Login
    response = client.post(
        "/login",
        data={
            "username": "loginuser",
            "password": "loginpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/login",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_protected_route_without_token():
    response = client.get("/users/me")
    assert response.status_code == 403

def test_protected_route_with_token():
    # Register and login
    client.post(
        "/register",
        json={
            "username": "protecteduser",
            "email": "protected@example.com",
            "password": "protectedpassword"
        }
    )
    
    login_response = client.post(
        "/login",
        data={
            "username": "protecteduser",
            "password": "protectedpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # Access protected route
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "protecteduser"

def test_create_task():
    # Register and login
    client.post(
        "/register",
        json={
            "username": "taskuser",
            "email": "task@example.com",
            "password": "taskpassword"
        }
    )
    
    login_response = client.post(
        "/login",
        data={
            "username": "taskuser",
            "password": "taskpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # Create task
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert not data["completed"]

def test_get_tasks():
    # Register and login
    client.post(
        "/register",
        json={
            "username": "gettaskuser",
            "email": "gettask@example.com",
            "password": "gettaskpassword"
        }
    )
    
    login_response = client.post(
        "/login",
        data={
            "username": "gettaskuser",
            "password": "gettaskpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    # Create a task first
    client.post(
        "/tasks",
        json={
            "title": "Get Test Task",
            "description": "Get Test Description",
            "completed": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get tasks
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Get Test Task"
