from fastapi import FastAPI
import uvicorn
from core.settings import settings
from db import Base, engine

Base.metadata.create_all(bind=engine)

app:FastAPI = FastAPI(
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url=None,
    title="FastAPI Social Media API",
)

@app.get("/")
async def index():
    
    return dict(message="Welcome to fastapi-social-media-api")

if __name__ == "__main__":
    uvicorn.run(app, port=int(settings.PORT), reload=False)