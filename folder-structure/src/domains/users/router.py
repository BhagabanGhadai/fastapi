from fastapi import APIRouter, status

from src.domains.auth.dependencies import CurrentUser
from src.core.dependencies import DbSession
from src.domains.users import service
from src.domains.users.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(data: UserCreate, db: DbSession):
    return await service.create(db, data)


@router.get("/me", response_model=UserOut)
async def read_me(current_user: CurrentUser):
    return current_user


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: DbSession, _: CurrentUser):
    return await service.get_by_id(db, user_id)
