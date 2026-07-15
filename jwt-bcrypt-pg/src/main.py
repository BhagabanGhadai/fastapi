from routers import api_router
from db import Base,engine
from fastapi import FastAPI
import uvicorn
from core.setting import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JWT-Bcrypt-PG",
    version="1.0.0",
    description="JWT-Bcrypt-PG",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":

    uvicorn.run(app, port=int(settings.PORT), reload=False)