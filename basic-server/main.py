import json

from fastapi import FastAPI,Request
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}   

@app.get("/items/{item_id}")
async def read_item(item_id: int, p: int, q: str = None,s:int = 0):
    return {"item_id": item_id, "p": p, "q": q, "s": s}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id}

@app.post('/users')
async def create_user(request: Request):
    body=await request.body()
    print(request.headers.get('authorization'))
    return {"status": "success", "message": "User created successfully"}