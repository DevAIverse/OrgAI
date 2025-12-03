import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Optional

DATABASE_URL = os.getenv('DATABASE_URL') or f"sqlite:///./orgai_demo.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
