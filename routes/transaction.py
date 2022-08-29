
from fastapi import APIRouter,HTTPException
from models import Transaction,Stock
from sqlmodel import Session,select
from database import engine
from typing import List

router = APIRouter(prefix="/transaction",tags=['Transaction'])

# Create a transaction
@router.post("/",status_code=201,response_model=Transaction)
async def create_transaction(transaction:Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

# Read ALL transaction 
@router.get("/",status_code=200,response_model=List[Transaction])
async def get_transaction():
    with Session(engine) as session:
        statement = select(Transaction)
        return session.exec(statement).all()