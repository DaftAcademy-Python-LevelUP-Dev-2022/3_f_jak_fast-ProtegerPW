from fastapi import FastAPI, Response, status, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime, timedelta
from time import strptime

app = FastAPI()
templates = Jinja2Templates(directory="jinja_templates")

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
    
@app.post("/check", response_class=HTMLResponse)
async def check_age(name: str, date: str, response: Response):
    check_date = True
    try:
        check_date = bool(datetime.datetime.strptime(date, "%Y-%m-%d"))
    except ValueError:
        check_date = False
        
    if(not check_date):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return   
    
    given_date = datetime.strptime(date, "%Y-%m-%d")
    age_of_person = datetime.utcnow() - given_date
    if(age_of_person > timedelta(days=5840)):
        response.status_code = status.HTTP_200_OK
        return templates.TemplateResponse("check_age.html.j2", {
        "name": name, "date": age_of_person.year})
    else:
        response.status_code = status.HTTP_401_BAD_REQUEST
        return