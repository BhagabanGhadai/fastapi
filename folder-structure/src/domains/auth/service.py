from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auth import utils
from src.domains.auth.exceptions import InvalidCredentials
from src.domains.users import service as users_service


async def authenticate(db: AsyncSession, email: str, password: str) -> str:
    user = await users_service.get_by_email(db, email)
    if user is None or not user.is_active or not utils.verify_password(
        password, user.hashed_password
    ):
        raise InvalidCredentials()
    return utils.create_access_token(user.id)
