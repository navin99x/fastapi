from fastapi import FastAPI, Path, Body, Form
from typing import Annotated, Any
from enum import Enum
from pydantic import BaseModel, EmailStr

class Tags(Enum):
    user = "user"
    items = "items"

class Item(BaseModel):
    item_id: int
    item_name: str | None = None
    item_price: float

class UserLogin(BaseModel):
    email: EmailStr
    user_name: str
    password: str

class UserInfo(BaseModel):
    email: EmailStr
    user_name: str

app = FastAPI()

@app.post("/items/", tags=[Tags.items], summary="Create an item")
async def create_item(item: Annotated[Item, Body()]):
    return item

@app.get("/items/", tags=[Tags.items], response_model= Item, summary="Retrive an item")
async def get_item() -> Item:
    return Item(item_id=10, item_price=100)

@app.post("/user/", response_model=UserInfo, tags=[Tags.user],
          summary="Create an user",
          description="Create an user with all the information: email, username and password",
          response_description="The created user info")  # Better to use function docstring for description
async def create_user(user: Annotated[UserLogin, Form()]) -> Any:
    return user