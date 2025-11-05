from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime, timedelta
import uuid

dummy_db = {
    "navin": {
        "username": "navin",
        "email": "mail@log.in",
        "hashed_pass": "xxsecurexx",
        "task": "eat"
    },
    "sagar": {
        "username": "sagar", 
        "email": "sagar@gmail.com",
        "hashed_pass": "xxcryptxx",
        "task": "sleep"
    }
}

token_db = {}
token_expiray = {}

def create_token(username: str) -> str:
    token = uuid.uuid4()
    token_db[token] = username
    token_expiray[token] = datetime.now() + timedelta(minutes=1)
    return token

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def hash_pass(password: str) -> str: 
    return 2*'x' + password + 2*'x'

def is_valid_token(token: str) -> bool:
    if token not in token_db:
        return False
    if datetime.now() > token_expiray[token]:
        del token_db[token]
        del token_expiray[token]
        return False
    return True


@app.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username not in dummy_db:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username"
        )
    if dummy_db[form_data.username]["hashed_pass"] != hash_pass(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return {"access_token": create_token(form_data.username), "token_type": "bearer"}

@app.get("/todos/")
async def get_work(token: str = Depends(oauth_scheme)):
    if not is_valid_token(token):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expired or Invalid token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    username = token_db[token]
    return {"username": username, "task": dummy_db[username]["task"]}

@app.get("/public/")
async def get_public():
    return {"Message": "Join our Todo community"}
