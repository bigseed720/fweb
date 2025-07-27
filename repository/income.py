from sqlmodel import SQLModel , Session , select
from datetime import datetime
from repository.models import Income , engine


class IncomeManager():
    #this method used for create a new row for income in database
    @staticmethod
    def createincome(amount:int,datetime:datetime,text:str,user:int,tag:str):
        
            income = Income(amount = amount , datetime = datetime , text = text , user = user , tag = tag)
            with Session(engine) as session:
                session.add(income)
                session.commit()
            return({
                "status":"ok"
            })

    #this method used for finde income wich communicated to user
    @staticmethod
    def getincome(user):
            statement = select(Income).where(Income.user == user)
            with Session(engine) as session:
                incomes = [dict(income) for income in session.exec(statement)]
                return({
                    "status":"ok",
                    "expences":incomes
                })
        
