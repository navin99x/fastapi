# FastAPI Journey

My code snippets while learning FastAPI.

### Code Snippet

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {
        "Why’d the API redirect?": "Client kept chasing endpoints that moved on."
        }

```

**Run:** `pip install fastapi uvicorn && uvicorn main:app --reload`

**Docs:** http://localhost:8000/docs
