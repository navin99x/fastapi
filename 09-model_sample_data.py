from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

class Data(BaseModel):
    id: int = Field(gt=10, le= 100, title="id of the item")
    name: str | None= Field(default=None,min_length=3, max_length=50, title="name of the item")

    model_config= {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 11,
                    "name": "Gadget"
                }
            ]
        }
    }

app = FastAPI()

@app.put("/items/")
async def update_item(item: Annotated[Data, Body()]):
    return item