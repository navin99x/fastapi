from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def index():
    content = '''
<html>
<body>
<h2>Welcome to the site</h2>
<p>Here you will find amazing resources.<p>
</body>
</html>
'''

    return HTMLResponse(content= content)