from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_BD_URL = "sqlite:///./todolist.db"

engine = create_engine(SQL_BD_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

Base = declarative_base()