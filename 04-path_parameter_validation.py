from typing import Annotated
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_number}")
def read_items(item_number: Annotated[str | None, Path(title="Query string",
                                              max_length=20,
                                              min_length=3,
                                              pattern="[a-zA-Z]{3, 20}",
                                              alias="q"
                                              )] = None):
    if item_number:
        return {"q": item_number}
    
# def read_items(q: str | None = Path(defalt=None)):