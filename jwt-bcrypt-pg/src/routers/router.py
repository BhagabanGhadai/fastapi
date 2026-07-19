from fastapi import APIRouter
from .user import user_router

api_router = APIRouter()

api_router.include_router(user_router)

@api_router.get("/health")
async def health_check():
    return {"message": "This app is healthy"}
