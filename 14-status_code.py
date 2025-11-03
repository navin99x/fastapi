from fastapi import FastAPI, status

app = FastAPI()

@app.get("/items/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "hello world"}