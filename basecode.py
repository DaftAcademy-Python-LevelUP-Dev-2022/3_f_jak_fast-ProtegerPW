from fastapi import FastAPI, Response, status, Request, Depends, Header, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from datetime import datetime, timedelta
from time import strptime

app = FastAPI()
templates = Jinja2Templates(directory="jinja_templates")
security = HTTPBasic()

list_of_paths = []

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
async def format_param(request:Request, response:Response, format: str | None = Query(default=None), user_agent: str | None = Header(default=None)):
    # request_json = await request.json()
    
    if format == "json":
        return {"user_agent": user_agent}
    elif format == "html":
        return templates.TemplateResponse("user_agent.html.j2", {
            "request": request, "user_agent": user_agent})
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return

@app.put("/save/{file_path:path}")
def save_put(file_path:str, response:Response):
    if file_path not in list_of_paths:
        list_of_paths.append(file_path)
        
    response.status_code = status.HTTP_200_OK
    return

@app.get("/save/{file_path:path}")
def save_get(file_path:str, response:Response):
    if file_path in list_of_paths:
        response.status_code = status.HTTP_301_MOVED_PERMANENTLY
        return RedirectResponse(url="/info", status_code=301)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return
    
@app.delete("/save/{file_path:path}")
def save_delete(file_path:str, response:Response):
    if file_path in list_of_paths:
        list_of_paths.remove(file_path)
    
    response.status_code = status.HTTP_200_OK
    return