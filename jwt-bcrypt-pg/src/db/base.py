from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Example:
        class User(Base):
            __tablename__ = "users"
    """
    pass