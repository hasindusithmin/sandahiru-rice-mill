
from sqlmodel import SQLModel,Field
from typing import Optional
from datetime import datetime
from pytz import timezone
from enum import Enum


class Bag(str,Enum):
    SMALL = "5 KILO"
    MEDIUM = "10 KILO"
    LARGE = "25 KILO"


class Stock(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str = Field(nullable=False)
    unit:float = Field(nullable=False)
    small:int = Field(default=None)
    medium:int = Field(default=None)
    large:int = Field(default=None)

class Transaction(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    date:Optional[datetime] = Field(default=datetime.now(tz=timezone("Asia/Colombo")))
    bag:Bag = Field(nullable=False)
    quantity:int = Field(nullable=False)
    stock_id:Optional[int] = Field(default=None,foreign_key="stock.id")