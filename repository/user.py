from sqlmodel import SQLModel , Field , create_engine , Session , select
from random import choice
from repository.models import User , Token , engine





class UserManager():
    #this ethod used for create a new row in database for users
    @staticmethod
    def createuser(username,password,email):
        statement = select(User).where(User.username == username)
        try:
            with Session(engine) as session:
                user = session.exec(statement).first()
                if user == None:
                    user = User(username=username,password=password,email=email)
                    session.add(user)
                    session.commit()
                    return({"status":"ok"})
                return({"status":"username is alredy exist"})
        except:
            return({"status":"there are some error"})
    
    #this method used for generate a random text  and check is there
    @staticmethod
    def __generatetoken(session:Session):
        seed = list("abcdefghigklmnopqrstuvwxyz123456")
        token = "".join([choice(seed) for i in range(32)])
        statement = select(Token).where(Token.token == token)
        res = session.exec(statement).first()
        if res == None:
            return token
        else:
            return UserManager.generatetoken(session)
    
    #this method used __generatetoken to generate a random text  and check is there
    #and make a communication between token and user
    @staticmethod
    def createtoken(username,password):
        try:
            with Session(engine) as session:
                statement = select(User).where(User.username == username , User.password == password)
                user = session.exec(statement=statement).first()
                if user != None:
                    gtoken = UserManager.__generatetoken(session)
                    statement = select(Token).where(Token.user == user.id)
                    stoken:Token = session.exec(statement).first()
                    if stoken == None:
                        token = Token(token = gtoken , user = user.id)
                        print(token.id)
                        session.add(token)
                        session.commit()
                        return({"token":token.token,"status":"ok"})
                    else:
                        stoken.token = gtoken
                        print(stoken.id)
                        session.add(stoken)
                        session.commit()
                        return({"token":stoken.token,"status":"ok"})
                else:
                    return({"status":"password or username is not corect"})
        except:
            return({"status":"there are some errors"})
        
    #this method is searching in database for users by their id
    @staticmethod
    def getuserbyid(id , session:Session = None):
        if session:
            statement = select(User).where(User.id == id)
            user = session.exec(statement).first()
            return({"user":user,"status":"ok"})
        else:
            with Session(engine) as session:
                statement = select(User).where(User.id == id)
                user = session.exec(statement).first()
                return({"user":user,"status":"ok"})

    #this method firs finde tken and get user id and use getuserbyid to finde user
    def getuserbytoken(token:str):
        try:
            with Session(engine) as session:
                statement = select(Token).where(Token.token == token)
                token = session.exec(statement).first()
                if token != None:
                    user = UserManager.getuserbyid(token.id)
                    return({
                        "status":"ok",
                        "user":dict(user['user'])
                    })
                return({"status":"token is invalig pleas login again"})
        except:
            return({"status":"there are some error"})



