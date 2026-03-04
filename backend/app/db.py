import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

# Utilise DATABASE_URL depuis l'environnement, fallback sqlite local
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./taskmanager.db")

engine_args = {}
if DATABASE_URL.startswith("sqlite"):  # Pour SQLite, threads
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    **engine_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
