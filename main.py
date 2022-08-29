
from fastapi import FastAPI
from models import Stock,Transaction
from database import engine,create_db_and_table
from sqlmodel import SQLModel

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_table()

@app.on_event("shutdown")
def shutdown():
    print("welcome")

