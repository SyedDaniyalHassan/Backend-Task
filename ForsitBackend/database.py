from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get environment variables or use default values
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "Forsit.db")

# Determine the database URL based on the environment variables
if DB_TYPE == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})


sessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)


Base = declarative_base()


def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()