
from sqlmodel import SQLModel,Field
from typing import Optional


class Stock(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name:str = Field(nullable=False)
    unit:float = Field(nullable=False)
    small:int = Field(default=None)
    medium:int = Field(default=None)
    large:int = Field(default=None)
