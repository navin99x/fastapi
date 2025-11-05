from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated, Any
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext

SECRET_KEY = "secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = 30

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

dummy_db = {
    "navin": {
        "username": "navin",
        "email": "mail@log.in",
        "hashed_pass": pwd_context.hash("navin1223"),
        "task": "eat"
    },
    "sagar": {
        "username": "sagar", 
        "email": "sagar@gmail.com",
        "hashed_pass": pwd_context.hash("sagar123"),
        "task": "sleep"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username:str):
    return dummy_db.get(username)

def authenticate_user(username: str, password:str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_pass"]):
        return False
    return True

def is_valid_token(token: str) -> Any:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        if payload["user"] in dummy_db:
            # jwt automatically validates token expiration
            # if datetime.now().timestamp() > payload["exp"]:
            #     raise ExpiredSignatureError("Token has expired, please relogin")
            return {"username": payload["user"]}
    except ExpiredSignatureError:
        raise ExpiredSignatureError("The token has expired, please re-login")
    except InvalidTokenError:
        raise InvalidTokenError("Invalid token")

    return None

async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authorization": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except InvalidTokenError:
        raise credential_exception
    user = get_user(username)
    if user is None:
        raise credential_exception
    return user

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos/")
async def get_todos(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"username": current_user["username"], "task": current_user["task"]}

@app.get("/public/")
async def get_public():
    return {"Message": "Join our Todo community"}
