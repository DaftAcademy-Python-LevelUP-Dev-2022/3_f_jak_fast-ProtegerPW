from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/start", response_class=HTMLResponse)
async def hello():
    return """
        <html>
            <head>
                <title>HTML Title</title>
            </head>
            <body>
                <h1>The unix epoch started at 1970-01-01</h1>
            </body>
        </html>
    """
    