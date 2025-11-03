from fastapi import FastAPI

fake_data = [{"name": "ram"}, {"name": "gita"}, {"name": "sita"}]

app = FastAPI()

@app.get('/names/')
async def read_items(skip: int = 0, limit: int = 1):
    return fake_data[skip:skip+limit]