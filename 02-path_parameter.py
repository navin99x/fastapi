from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    return {"Hello": "world"}

@app.get("/detail/{name}")
async def get_detail(name:str):
    return {"name": name.upper()}
