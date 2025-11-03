from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/upload/")
async def create_file(file: UploadFile):
    contents = await file.read()
    with open(f"/home/navin/vn/fastapi/{file.filename}", "wb") as f:
        f.write(contents)
    return {"saved_as": file.filename}


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/upload/" enctype="multipart/form-data" method="post">
    <label for="file">Select File </label>
    <input id="file" type="file" name="file">
    <button type="submit">Submit</button>
    </form>
    </body>
"""

    return HTMLResponse(content=content)
