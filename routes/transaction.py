
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
        exec(f"if stock.{bag} < qty:\n\traise HTTPException(status_code=400,detail='insufficient quantity')")
        exec(f"stock.{bag} -= qty")
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

# Read one transaction by id (this is required for testing)
@router.get("/{id}",status_code=200,response_model=Transaction)
async def get_transaction_by_id(id:int):
    with Session(engine) as session:
        transaction = session.get(Transaction,id)
        if transaction is None:
            raise HTTPException(status_code=404)
        return transaction

# Delete transaction By Id
@router.delete("/{id}",status_code=202)
async def delete_transaction(id:int):
    with Session(engine) as session:
        # Get transaction by Id
        transaction = session.get(Transaction,id)
        # If transaction not exist
        if transaction is None:
            raise HTTPException(status_code=404)
        # ________Update stock Table________
        stock_id = transaction.stock_id
        bags = {"5KILO":"small","10KILO":"medium","25KILO":"large"}
        bag = bags[transaction.bag]
        stock = session.get(Stock,stock_id)
        # print(stock)
        qty = transaction.quantity
        # If stock not exist (Very Optinal)
        if stock is None:
            raise HTTPException(status_code=404)
        exec(f"if qty > stock.{bag}:\n\traise HTTPException(status_code=400,detail='insufficient quantity')")
        exec(f"stock.{bag} += qty")
        # print(stock)
        session.add(stock)
        session.commit()
        # ________Update transaction table________
        session.delete(transaction)
        session.commit()
        return


