from fastapi import FastAPI, Response, status, Request, Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime, timedelta
from time import strptime

app = FastAPI()
templates = Jinja2Templates(directory="jinja_templates")
security = HTTPBasic()

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
def check_age(request: Request, response: Response, credentials: HTTPBasicCredentials=Depends(security)):
    
    check_date = True
    try:
        check_date = bool(datetime.strptime(credentials.password, "%Y-%m-%d"))
    except ValueError:
        check_date = False
        
    if(not check_date):
        response.status_code = status.HTTP_401_BAD_REQUEST
        return   
    
    given_date = datetime.strptime(credentials.password, "%Y-%m-%d")
    age_of_person = datetime.utcnow().year - given_date.year
    if(age_of_person > 16):
        response.status_code = status.HTTP_200_OK
        return templates.TemplateResponse("check_age.html.j2", {
            "request": request, "name": credentials.username, "age": age_of_person})
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return
    
    
@app.get("/info")
async def format_param(request:Request, response:Response, user_agent: str | None = Header(default=None)):
    request_json = await request.json()
    
    if request_json["format"] == "json":
        return {"user_agent": user_agent}
    elif request_json["format"] == "html":
        return templates.TemplateResponse("user_agent.html.j2", {
            "request": request, "user_agent": user_agent})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return