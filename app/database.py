from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config

DB_USER = config("POSTGRES_USER")
DB_PASS = config("POSTGRES_PASSWORD")
DB_HOST = config("POSTGRES_HOST", default="localhost")
DB_PORT = config("POSTGRES_PORT", default="5432")
DB_NAME = config("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
