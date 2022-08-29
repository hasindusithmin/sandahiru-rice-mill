
from fastapi import FastAPI
from models import Stock,Transaction
from database import engine,create_db_and_table


app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_table()

