from fastapi import FastAPI
from typing import Any, Annotated
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    email:EmailStr
    username: str

app = FastAPI()

@app.post("/user/", response_model= UserOut)
async def create_user(user: UserIn) -> Any:
    return user