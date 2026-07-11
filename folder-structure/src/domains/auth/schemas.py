from pydantic import EmailStr

from src.core.schemas import BaseSchema


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
