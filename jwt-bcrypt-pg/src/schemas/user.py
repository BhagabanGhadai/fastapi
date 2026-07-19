from datetime import datetime
from pydantic import BaseModel

class UserBaseRequest(BaseModel):
    username:str
    password:str

class UserBaseResponse(BaseModel):
    id:int
    username:str
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attributes = True

class TokenPayload(BaseModel):
    sub:int
    token_type:str
    exp:datetime

class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str

    class Config:
        from_attributes = True