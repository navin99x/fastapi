from pydantic import BaseModel
from fastapi import FastAPI, Body

class Data(BaseModel):
    id: int
    username: str
    gender: str | None = None

app = FastAPI()

@app.post('/items')
async def create_item(item: Data = Body()):
    item_data = item.model_dump()
    return {"username": item_data["username"], "gender": item_data["gender"]}
