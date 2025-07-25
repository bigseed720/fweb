from sqlmodel import SQLModel , Field , create_engine , Session , select
from random import choice



class User(SQLModel , table=True):
    id:int = Field(default = None ,primary_key=True)    
    username:str
    password:str
    email:str
    autentication:bool = Field(default = False)

class Token(SQLModel , table = True):
    id:int = Field(default = None ,primary_key = True)
    token:str
    user:int
    verified:bool = False



class UserManager():

    @staticmethod
    def crateuser(username,password,email):
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
        
    @staticmethod
    def generatetoken(session:Session):
        seed = list("abcdefghigklmnopqrstuvwxyz123456")
        token = "".join([choice(seed) for i in range(32)])
        statement = select(Token).where(Token.token == token)
        res = session.exec(statement).first()
        if res == None:
            return token
        else:
            return UserManager.generatetoken(session)
    

    @staticmethod
    def createtoken(username,password):
        try:
            with Session(engine) as session:
                statement = select(User).where(User.username == username , User.password == password)
                user = session.exec(statement=statement).first()
                if user != None:
                    gtoken = UserManager.generatetoken(session)
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





engine = create_engine("sqlite:///databases/user_database.db")
SQLModel.metadata.create_all(engine)




