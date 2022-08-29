
from fastapi import APIRouter,HTTPException
from models import Transaction
from sqlmodel import Session
from database import engine

router = APIRouter(prefix="/transaction",tags=['Transaction'])

# Create a transaction
@router.post("/",status_code=201,response_model=Transaction)
async def create_transaction(transaction:Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
