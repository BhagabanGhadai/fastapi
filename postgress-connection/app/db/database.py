from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from core.settings import settings
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine(settings.DB_CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

