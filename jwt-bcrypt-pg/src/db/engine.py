from sqlalchemy import create_engine

from core import settings


engine = create_engine(
    settings.DB_CONNECTION_STRING,

    # Connection Pool
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,

    # Debug
    echo=True,

    # Future SQLAlchemy API
    future=True,

    # Check stale connections
    pool_pre_ping=True,
)