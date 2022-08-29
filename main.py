
from fastapi import FastAPI
from models import Stock,Transaction
from database import create_db_and_table
from routes import stock

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_table()

@app.get("/",status_code=200,tags=['Root'])
def root():
    return

app.include_router(stock.router)




