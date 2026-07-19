from db import get_db
from fastapi import status, APIRouter,Depends
from sqlalchemy.orm import Session
from schemas import UserBaseResponse
from schemas import UserBaseRequest
from services.user import UserService

user_router=APIRouter(
    prefix="/users",
    tags=["user"]
)

@user_router.post("/",response_model=UserBaseResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user_data:UserBaseRequest, db:Session =Depends(get_db)):
    user_service=UserService(db)
    new_user=user_service.create_user(user_data.model_dump())
    return new_user

