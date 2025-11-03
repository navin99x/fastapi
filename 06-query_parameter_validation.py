from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    item_id: Annotated[
        int | None, 
        Query(
            title="ID of the item to fetch",
            description="Must be greater than 10 and less than or equal to 100",
            gt=10,
            le=100,
        )
    ] = None
):
    return {"item_id": item_id}
