
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from models import Stock,Transaction
from database import create_db_and_table
from routes import (stock,transaction)
import uvicorn

description = """
## SandHiruApp
# _[sanda hiru rice mills](https://sanda-hiru-rice-mills.business.site/)_

![image](https://i.ibb.co/Rv3gRJL/Whats-App-Image-2021-04-12-at-1-29-29-PM-2-1.jpg)

"""

app = FastAPI(
    title="SandHiruApp",
    description=description,
    version="0.0.1",
    contact={
        "name": "Hasindu Sithmin",
        "url": "https://hasindusithmin.github.io",
        "email": "hasindusithmin64@gmail.com",
    },
    license_info={
        "name": "Github",
        "url": "https://github.com/hasindusithmin/sandahiru-rice-mill.git",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_db_and_table()

@app.get("/",status_code=200,tags=['Root'])
def root():
    return RedirectResponse("/docs")

app.include_router(stock.router)
app.include_router(transaction.router)

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)

