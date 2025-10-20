import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Simple Task Manager API работает!"}

def test_register_user_success():
    """Тест успешной регистрации пользователя"""
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_create_task():
    """Тест создания задачи"""
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] == False

def test_get_tasks():
    """Тест получения списка задач"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)