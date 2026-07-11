from fastapi import APIRouter

from src.domains.auth import service
from src.domains.auth.schemas import LoginRequest, TokenResponse
from src.core.dependencies import DbSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DbSession):
    token = await service.authenticate(db, data.email, data.password)
    return TokenResponse(access_token=token)
