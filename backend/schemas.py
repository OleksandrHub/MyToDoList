from pydantic import BaseModel, Field
from typing import Annotated

class UserBase(BaseModel):
    name: str
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TaskBD(BaseModel):
    title: str
    description: str
    completed: bool
    date: str
    user_id: int


class TaskCreate(TaskBD): 
    completed: bool = False

class Task(TaskBD):
    id: int
    user: User

    class Config:
        orm_mode = True