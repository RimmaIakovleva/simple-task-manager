from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Создаем приложение FastAPI
app = FastAPI(
    title="Simple Task Manager API",
    description="Простое API для управления задачами",
    version="1.0.0"
)

# Временное хранилище в памяти
tasks_db = {}
users_db = {}

# Модели данных
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: str
    username: str
    email: str

# Базовый endpoint для проверки
@app.get("/")
def read_root():
    return {"message": "Simple Task Manager API работает!"}

# Регистрация пользователя
@app.post("/register", response_model=User)
def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        username=user.username,
        email=user.email
    )
    users_db[user.username] = {"user": new_user, "password": user.password}
    return new_user

# Получить все задачи
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return list(tasks_db.values())

# Создать задачу
@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    task_id = str(uuid.uuid4())
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        created_at=datetime.now().isoformat()
    )
    tasks_db[task_id] = new_task
    return new_task