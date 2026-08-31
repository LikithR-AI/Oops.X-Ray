from sqlmodel import create_engine, SQLModel, Session
import os

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/db.sqlite")
engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread":False})

def init_db():
    from api.app import models
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)