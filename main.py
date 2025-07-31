from fastapi import FastAPI , Request 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers.webs.user import userrouter

#make settings#
app = FastAPI()
tmp = Jinja2Templates(directory='templates')
app.mount(path='/assets' , app=StaticFiles(directory='./assets') , name = 'assets')
###############


#add routers#

app.include_router(userrouter)

#############




@app.get("/")
def index(request:Request,status:str = "ok"):    
    url = str(request.base_url)
    return(tmp.TemplateResponse(request=request , name='index.html' , context={
        "assets":url+"assets",
        "status":status
        }))

 


