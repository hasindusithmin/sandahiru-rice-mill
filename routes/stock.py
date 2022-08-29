
from fastapi import APIRouter,HTTPException
from sqlmodel import Session,select
from models import Stock
from database import engine

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/",status_code=200)
async def get_stock_details():
    with Session(engine) as session:
        statement = select(Stock)
        return session.exec(statement).all()