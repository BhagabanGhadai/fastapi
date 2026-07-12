from .user import user_router
from fastapi import APIRouter
api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    
    return dict(message="This is healthy")

api_router.include_router(user_router)
# api_router.include_router(orders_router)
