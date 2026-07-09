from fastapi import FastAPI
from pydantic import AliasChoices, BaseModel, Field ,field_validator, model_validator
from typing import Optional, Self


app = FastAPI()


class User(BaseModel):
    username: str = Field(validation_alias=AliasChoices("username", "user"))
    password: str = Field(min_length=8, max_length=20)
    is_active: Optional[bool] = None


@app.post("/")
async def root(user: User):
    print(user)
    print(type(user.password))
    return {"message": "Hello World", "username": user.username}

# how to validate nested json

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str = Field(..., min_length=6,max_length=6)  # Validates US ZIP codes

class Person(BaseModel):
    name: str
    age: int
    address: Address


@app.post("/person")
async def create_person(person: Person):
    return person

# how to validate list and dictionary in json
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: dict[str, float]
    faq:list[str] = []
    queries: list[dict[str, str]] = []


@app.post("/items/")
async def create_item(item: Item):
    return item

# custom validators
class CustomUser(BaseModel):
    age: int
    @field_validator("age")
    @classmethod
    def validate_age(cls, value):

        if value < 18:
            raise ValueError("Must be 18+")

        return value
    
@app.post("/custom_user/")
async def create_custom_user(user: CustomUser):
    return user

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self