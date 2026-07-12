from fastapi import FastAPI
import uvicorn
from core import settings
from db import Base, engine
from api import api_router

Base.metadata.create_all(bind=engine)

app:FastAPI = FastAPI(
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url=None,
    title="FastAPI Social Media API",
)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, port=int(settings.PORT), reload=False)