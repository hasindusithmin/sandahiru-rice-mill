
from fastapi import APIRouter,HTTPException
from sqlmodel import Session,select
from models import Stock
from database import engine
from typing import List

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/",status_code=200,response_model=List[Stock])
async def get_stock_details():
    with Session(engine) as session:
        statement = select(Stock)
        return session.exec(statement).all()