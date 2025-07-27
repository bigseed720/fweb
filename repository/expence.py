from sqlmodel import SQLModel , Session , select
from datetime import datetime
from repository.models import Expence , engine



class ExpenceManager():
    #this method used for create a new row for expence in database
    @staticmethod
    def createexpence(amount:int,datetime:datetime,text:str,user:int,tag:str):
        
            expence = Expence(amount = amount , datetime = datetime , text = text , user = user , tag = tag)
            with Session(engine) as session:
                session.add(expence)
                session.commit()
            return({
                "status":"ok"
            })

    #this method used for finde expences wich communicated to user
    @staticmethod
    def getexpences(user):
        
            statement = select(Expence).where(Expence.user == user)
            with Session(engine) as session:
                expences = [dict(expence) for expence in session.exec(statement)]
                return({
                    "status":"ok",
                    "expences":expences
                })
        
