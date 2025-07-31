from fastapi import APIRouter , Request , Form 
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from core.Core import CheckIsMobile
from repository.user import UserManager
from fastapi.responses import RedirectResponse
from datetime import datetime
from repository.expence import ExpenceManager
from repository.income import IncomeManager
import json
getbalance = lambda l : sum([ i['amount'] for i in l])

#TODO:make a protocol to show incomes , expences , income balance and expence balance in dashboard page



userrouter = APIRouter(prefix="/user")

tmp = Jinja2Templates("templates")






@userrouter.get('/login')
def login(request:Request):
    url = str(request.base_url)
    assets = url+"assets"
    if not CheckIsMobile(request):
        return tmp.TemplateResponse(request=request , name = 'acounts/login.html' , context={"assets":assets})
    else:
        return tmp.TemplateResponse(request=request , name = 'acounts/login_mobile.html' , context={"assets":assets})

@userrouter.post('/login')
def login(request:Request , username:str = Form(...) , password:str = Form(...)):
    url = str(request.base_url)
    assets = url+"assets"
    res = UserManager.createtoken(username=username,password=password)
    if res['status'] != "ok":
        if not CheckIsMobile(request):
            return tmp.TemplateResponse(request=request , name = 'acounts/login.html' , context={"assets":assets})
        else:
            return tmp.TemplateResponse(request=request , name = 'acounts/login_mobile.html' , context={"assets":assets})
    return(RedirectResponse(url+f"user/dashboard/{res['token']}"))

@userrouter.get('/sinup')
def sinup(request:Request):
    url = str(request.base_url)
    assets = url+"assets"
    if not CheckIsMobile(request):
        return tmp.TemplateResponse(request=request , name = 'acounts/sinup.html' , context={"assets":assets,"status":"ok"})
    else:
        return tmp.TemplateResponse(request=request , name = 'acounts/sinup_mobile.html' , context={"assets":assets,"status":"ok"})

@userrouter.post("/sinup")
def sinup(request:Request , username:str = Form(...) , password:str = Form(...) , email:str = Form(...)):
    url = str(request.base_url)
    assets = url+"assets"
    res = UserManager.createuser(username,password,email)
    if res["status"] != "ok":
        if not CheckIsMobile(request):
            return tmp.TemplateResponse(request=request , name = 'acounts/sinup.html' , context={"assets":assets,"status":res["status"]})
        else:
            return tmp.TemplateResponse(request=request , name = 'acounts/sinup_mobile.html' , context={"assets":assets,"status":res["status"]})
    res = UserManager.createtoken(username=username,password=password)
    return RedirectResponse(url+f"user/dashboard/{res['token']}")





@userrouter.post("/dashboard/{token}")
def dashboard(request:Request,token:str):
    assets = str(request.base_url)+"assets"
    res = UserManager.getuserbytoken(token)
    if res['status'] != 'ok':
        return RedirectResponse(str(request.base_url)+f"?status={res['status']}")
    expences = ExpenceManager.getexpences(res['user']['id'])['expences']
    incomes = IncomeManager.getincomes(res['user']['id'])['incomes']
    return tmp.TemplateResponse(request=request,name = "dashboard.html",context = {
        'token':token ,
        "assets":assets,
        "expences":expences,
        "incomes":incomes,
        "income_balance":getbalance(incomes),
        "expence_balance":getbalance(expences)
        })

@userrouter.get("/dashboard/{token}")
def dashboard(request:Request,token:str):
    assets = str(request.base_url)+"assets"
    res = UserManager.getuserbytoken(token)
    if res['status'] != 'ok':
        return RedirectResponse(str(request.base_url)+f"?status={res['status']}")
    expences = ExpenceManager.getexpences(res['user']['id'])['expences']
    incomes = IncomeManager.getincomes(res['user']['id'])['incomes']
    return tmp.TemplateResponse(request=request,name = "dashboard.html",context = {
        'token':token ,
        "assets":assets,
        "expences":expences,
        "incomes":incomes,
        "income_balance":getbalance(incomes),
        "expence_balance":getbalance(expences)
        })







@userrouter.get("/expence/add")
def exadd(request:Request , token:str):
    assets = str(request.base_url) + "assets"
    return tmp.TemplateResponse(request = request , name = "actions/expence_add.html" , context = {
        "token":token,
        "assets":assets,
        "status":"ok"
    })

@userrouter.post("/expence/add")
def exadd(request:Request , token:str = Form(...) , amount:int = Form(...) , text:str = Form(...), my_date: datetime = Form(...) , tag:str = Form(...)):
    assets = str(request.base_url) + "assets"
    res = UserManager.getuserbytoken(token)
    if res['status'] != "ok":
        return tmp.TemplateResponse(request = request , name = "actions/expence_add.html" , context = {
            "token":token,
            "assets":assets,
            "status":res['status']
        })
    res = ExpenceManager.createexpence(amount = amount , datetime = my_date , text = text , user = res['user']['id'],tag=tag)
    if res['status'] != "ok":
        return tmp.TemplateResponse(request = request , name = "actions/expence_add.html" , context = {
            "token":token,
            "assets":assets,
            "status":res['status']
        })
    return(RedirectResponse(f"{request.base_url}user/dashboard/{token}"))

@userrouter.get("/income/add")
def exadd(request:Request , token:str):
    assets = str(request.base_url) + "assets"
    return tmp.TemplateResponse(request = request , name = "actions/income_add.html" , context = {
        "token":token,
        "assets":assets,
        "status":"ok"
    })

@userrouter.post("/income/add")
def exadd(request:Request , token:str = Form(...) , amount:int = Form(...) , text:str = Form(...), my_date: datetime = Form(...) , tag:str = Form(...)):
    assets = str(request.base_url) + "assets"
    res = UserManager.getuserbytoken(token)
    if res['status'] != "ok":
        return tmp.TemplateResponse(request = request , name = "actions/income_add.html" , context = {
            "token":token,
            "assets":assets,
            "status":res['status']
        })
    res = IncomeManager.createincome(amount = amount , datetime = my_date , text = text , user = res['user']['id'],tag=tag)
    if res['status'] != "ok":
        return tmp.TemplateResponse(request = request , name = "actions/income_add.html" , context = {
            "token":token,
            "assets":assets,
            "status":res['status']
        })
    return(RedirectResponse(f"{request.base_url}user/dashboard/{token}"))


@userrouter.post("/expence/manage")
def expence_manage(request:Request,status:str = "ok",token:str=Form(...),id:int=Form(...)):
    assets = str(request.base_url)+"assets"
    res = ExpenceManager.getexencebyid(id)
    expence = res['expence']
    return(tmp.TemplateResponse(request=request,name="actions/expence_manage.html",context={
        "assets":assets,
        "status":status,
        "token":token,
        "expence":expence
    }))
