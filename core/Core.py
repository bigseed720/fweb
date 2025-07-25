from fastapi import Request



def CheckIsMobile(request:Request):
    agent = request.headers.get('user-agent')
    keys = ["Android","Iphone","Mobile","Ipad"]
    for key in keys:
        if key in agent:
            return True
    return False

