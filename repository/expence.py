from sqlmodel import SqlModel , create_engine , Session , Field
from datetime import datetime


class Expence(SqlModel , table = True):
    id:int = Field(default = None , primary_key=True)
    amount:int
    datetime:datetime
    text:str
    user:int

    