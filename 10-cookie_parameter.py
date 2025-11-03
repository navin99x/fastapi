from typing import Annotated
from pydantic import BaseModel
from fastapi import Cookie, FastAPI

class Cookies(BaseModel):
    ads_id: int | None = None

    model_config = {"extra": "ignore"}

app = FastAPI()

@app.get("/")
async def root(ads_id: Annotated[Cookies, Cookie(alias="id")]):
    return {"ads_id": ads_id}