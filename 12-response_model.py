from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Annotated, Any

class Item(BaseModel):
    item_id: int
    item_name: str | None
    item_price: float

dummy_db: list[Item] = list()
dummy_db.append(Item(item_id=1, item_name="gadget", item_price=100))

app = FastAPI()

@app.post("/items/", response_model=Item)
def create_item(item: Annotated[Item, Body()]):
    dummy_db.append(item)
    return item

@app.get("/items/{id}", response_model=Item)
def read_item(id: int) -> Any:
    for item in dummy_db:
        if item.item_id == id:
            return item
    raise HTTPException(status_code=404, detail="Item Not found")