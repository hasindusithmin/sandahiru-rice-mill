
from fastapi import APIRouter,HTTPException
from sqlmodel import Session,select
from models import Stock
from database import engine
from typing import Optional,List
from pydantic import BaseModel

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/",status_code=200,response_model=List[Stock])
async def get_stock():
    with Session(engine) as session:
        statement = select(Stock)
        return session.exec(statement).all()

class StocK(BaseModel):
    unit:Optional[float]
    small:Optional[int]
    medium:Optional[float]
    large:Optional[float]

@router.put("/{id}",status_code=202,response_model=Stock)
async def update_stock(id:int,stock:StocK):
    with Session(engine) as session:
        # Get By Id 
        db = session.get(Stock, id)
        # If `db` is None 
        if db is None:
            raise HTTPException(status_code=404)
        for k,v in stock.__dict__.items():
            # Filter Empty value
            if v is None:
                continue
            exec(f"db.{k} = '{v}'")
        session.add(db)
        session.commit()
        session.refresh(db)
        return db

        