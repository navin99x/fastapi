from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class UserType (str, Enum):
    admin = "admin"
    user = "user"

@app.get("/login/{user_type}")
async def get_user(user_type: UserType):
    if user_type is UserType.admin:
        return "Role: Privilege"
    
    if user_type is UserType.user:
        return "Role: Basic"