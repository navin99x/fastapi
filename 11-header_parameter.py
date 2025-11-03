from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class HeaderModel(BaseModel):
    user_agent: str
    accept: str
    host: str

    model_config = {"extra": "ignore"}

@app.get("/header/")
async def get_header(header: Annotated[HeaderModel, Header()]):
    return header