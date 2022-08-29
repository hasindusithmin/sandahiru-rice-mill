
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
        # ____________Update stock table____________
        # Fetch Stock instance to 'stock'
        stock = session.get(Stock,transaction.stock_id)
        # If stock is None
        if stock is None:
            raise HTTPException(status_code=404,detail="stock not found")
        # Bag Type and Quantity
        bag, qty = transaction.bag.name, transaction.quantity
        cmd = f"if stock.{bag} < qty:\n\traise HTTPException(status_code=400,detail='insufficient quantity')"
        exec(cmd)
        cmd = f"stock.{bag} -= qty"
        exec(cmd)
        session.add(stock)
        session.commit()
        # ____________Create Transaction____________ 
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