from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends # type: ignore 
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi.middleware.cors import CORSMiddleware # type: ignore
from models import User, Task, Base 
from database import engine, session_local 
from schemas import UserCreate, TaskCreate, Task as TaskSchema, User as UserSchema

app = FastAPI()

# origins = [
#     "http://localhost:8080",
#     "http://127.0.0.1:8000",
#     "http://192.168.110.55:8080",
#     "http://192.168.110.55:8081"

# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/sign_up", response_model=UserSchema)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)) -> UserSchema:
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = User(name=user.name, username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{email}", response_model=UserSchema)
async def login_user(email: str, db: Session = Depends(get_db)) -> UserSchema:
    db_user = db.query(User).filter(and_(User.username == email)).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect username")
    return db_user

@app.post("/tasks", response_model=TaskSchema)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskSchema:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{user_id}", response_model=List[TaskSchema])
async def read_tasks(user_id: int, db: Session = Depends(get_db)) -> List[TaskSchema]:
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks

@app.put("/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)) -> TaskSchema:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}