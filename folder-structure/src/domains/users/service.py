from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auth import utils as auth_utils
from src.domains.users.exceptions import EmailAlreadyRegistered, UserNotFound
from src.domains.users.models import User
from src.domains.users.schemas import UserCreate


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_by_id(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise UserNotFound()
    return user


async def create(db: AsyncSession, data: UserCreate) -> User:
    if await get_by_email(db, data.email) is not None:
        raise EmailAlreadyRegistered()
    user = User(email=data.email, hashed_password=auth_utils.hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
