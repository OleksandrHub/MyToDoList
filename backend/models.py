from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  

    tasks = relationship("Task", back_populates="user")  # ← виправлено

class Task(Base): 
    __tablename__ = "tasks" 

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String, index=True)  
    description = Column(String, index=True)  
    completed = Column(Integer, default=0)  
    date = Column(String)  
    user_id = Column(Integer, ForeignKey("users.id"))  

    user = relationship("User", back_populates="tasks")