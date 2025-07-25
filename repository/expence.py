from sqlmodel import SQLModel , create_engine , Session , Field , select
from datetime import datetime


class Expence(SQLModel , table = True):
    id:int = Field(default = None , primary_key=True)
    amount:int
    datetime:datetime
    text:str
    user:int

class ExpenceManager():
    @staticmethod
    def createexpence(amount:int,datetime:datetime,text:str,user:int):
        
            expence = Expence(amount = amount , datetime = datetime , text = text , user = user)
            with Session(engine) as session:
                session.add(expence)
                session.commit()
            return({
                "status":"ok"
            })

    @staticmethod
    def getexpences(user):
        
            statement = select(Expence).where(Expence.user == user)
            with Session(engine) as session:
                expences = [dict(expence) for expence in session.exec(statement)]
                return({
                    "status":"ok",
                    "expences":expences
                })
        
engine = create_engine("sqlite:///databases/expence_database.db")
SQLModel.metadata.create_all(engine)