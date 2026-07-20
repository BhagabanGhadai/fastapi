from db import get_db
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserBaseResponse, UserBaseRequest, TokenResponse
from services.user import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["user"]
)

@user_router.post("/register", response_model=UserBaseResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserBaseRequest, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        new_user = user_service.create_user(user_data.model_dump())
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user_data: UserBaseRequest, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        token_data = user_service.login(user_data.model_dump())
        return token_data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))