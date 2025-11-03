from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: Annotated[int, Path(gt=1, lt=20)]):
    if item_id not in range(1,20):
        raise HTTPException(status_code=404, detail="Item not available")
    return {"item_id": item_id}
    