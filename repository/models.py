from sqlmodel import SQLModel , Field , create_engine
from datetime import datetime as datetime_


class Expence(SQLModel , table = True):
    id:int = Field(default = None , primary_key=True)
    amount:float
    datetime:datetime_
    text:str
    user:int
    tag:str

    def update(self,amount:float,datetime:datetime_,text:str,tag:str):
        self.amount =amount
        self.datetime=datetime
        self.text=text
        self.tag=tag

class Income(SQLModel , table = True):
    id:int = Field(default = None , primary_key=True)
    amount:float
    datetime:datetime_
    text:str
    user:int
    tag:str


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

engine = create_engine("sqlite:///databases/main.db")
SQLModel.metadata.create_all(engine)