from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domains.auth import utils
from src.domains.auth.exceptions import InvalidToken
from src.core.dependencies import DbSession
from src.domains.users import service as users_service
from src.domains.users.models import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None:
        raise InvalidToken()
    user_id = utils.decode_access_token(credentials.credentials)
    return await users_service.get_by_id(db, user_id)


CurrentUser = Annotated[User, Depends(get_current_user)]
