from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from enum import Enum

TOKEN_EXPIRATION_TIME = 10
SECRET_KEY = "c33796ead763e48e3a24deec85e795"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth_schema = OAuth2PasswordBearer(tokenUrl="token")

dummy_user_db = {
    "ram": {
        "username": "ram",
        "hashed_password": pwd_context.hash("ram123"),
        "role": "editor"
    },
    "hari": {
        "username": "hari",
        "hashed_password": pwd_context.hash("hari123"),
        "role": "visitor"
    }
}

dummy_document_db = [{
        "isbn": 111,
        "title": "Project Blue",
        "description": "Project Blue is a novel by ....",
        "access_level": "private"
    },
    {
        "isbn": 222,
        "title": "The Weapon",
        "description": "The Weapon covers the story of ....",
        "access_level": "public"
    }
]

class User(BaseModel):
    username: str
    hashed_password: str
    role: str

class AccessLevel(Enum):
    private = "private"
    public = "public"

class Document(BaseModel):
    isbn: int
    title: str
    description: str
    access_level: AccessLevel

class DocumentOut(BaseModel):
    isbn: int
    title: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

def verify_hash_password(plain_pass: str, hashed_pass) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)

def fetch_user_data(username: str):
    return dummy_user_db.get(username)
      
def authenticate_user(username: str, password: str):
    user = fetch_user_data(username)
    if user and verify_hash_password(password, user["hashed_password"]):
        return user
    return None

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    exp_date = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    to_encode.update({"exp": exp_date.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth_schema)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authorization": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username= payload["sub"]

        if username is None:
            raise credential_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired, please re-login",
            headers={"WWw-Authorization": "Bearer"}
        )
    except InvalidTokenError:
        raise credential_exception
    
    user = fetch_user_data(username)
    if user is None:
        raise credential_exception
    return user

async def get_current_editor_user(user: Annotated[dict, Depends(get_current_user)]):
    if user["role"] != "editor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action require editor privileges"
        )
    return user

app = FastAPI()

@app.post("/token", response_model=AccessToken)
async def token_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user: dict| None = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token({"sub": user["username"], "role": user["role"]})
    return AccessToken(access_token=access_token, token_type="bearer")

@app.get("/documents/")
async def get_doc(user: Annotated[dict, Depends(get_current_user)]):
    if user.get("role") == "visitor":
        return [doc for doc in dummy_document_db if doc["access_level"] == "public"]
    elif user.get("role") == "editor":
        return dummy_document_db

@app.post("/documents/", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_doc(doc: Annotated[Document, Body()], 
                     user: Annotated[dict, Depends(get_current_editor_user)]
                     ) -> DocumentOut:

    new_doc_data = doc.model_dump()
    dummy_document_db.append(new_doc_data)
    return DocumentOut(**new_doc_data)
