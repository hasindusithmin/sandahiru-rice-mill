
from fastapi.testclient import TestClient
from main import app
from models import (Stock,Transaction)
from sqlmodel import Session,select
from database import engine
from random import randint

#########################################

# Create Test Client 
client = TestClient(app)

def test_get_stock():
    res = client.get(url="/stock")
    # Check Status Code 
    assert res.status_code == 200
    # Check Response Body
    with Session(engine) as session:
        statement = select(Stock)
        # Data On database 
        db = session.exec(statement).all()
        # Data on Response Body(bd) 
        bd = res.json()
        bd  = [Stock(**b) for b in bd]
        
        # Check Length 
        assert len(db) == len(bd)

        for i in range(len(db)):
            obj_db = db[i]
            obj_bd = bd[i]
            # Check id
            assert obj_db.id == obj_bd.id
            # Check name
            assert obj_db.name == obj_bd.name
            # Check unit
            assert obj_db.unit == obj_bd.unit
            # Check small
            assert obj_db.small == obj_bd.small
            # Check medium
            assert obj_db.medium == obj_bd.medium
            # Check large
            assert obj_db.large == obj_bd.large

def test_update_stock():
    id = 1
    data = {
        'unit':randint(200, 300),
        'small':randint(0, 100),
        'medium':randint(0, 100),
        'large':randint(0, 100)
    }
    res = client.put(url=f"/stock/{id}",json=data)

    # Check status code 
    assert res.status_code == 202

    # Check data 
    with Session(engine) as session:
        # Data in database 
        db = session.get(Stock,id)
        # Data in response body(bd)
        bd = res.json()
        # `bd:dict` to `bd:Stock` 
        bd = Stock(**bd)    
        # Check id
        assert db.id == bd.id
        # Check name
        assert db.name == bd.name
        # Check unit
        assert db.unit == bd.unit
        # Check small
        assert db.small == bd.small
        # Check medium
        assert db.medium == bd.medium
        # Check large
        assert db.large == bd.large

def test_update_stock_not_found():
    id = 100
    data = {
        "unit":randint(200, 300)
    }
    res = client.put(url=f"/stock/{id}",json=data)
    # Check status code is 404
    assert res.status_code == 404

def test_update_stock_unprocessable_entity():
    id = 1
    data = {
        "unit":"2hundred"
    }
    res = client.put(url=f"/stock/{id}",json=data)
    # Check status code is 422
    assert res.status_code == 422

def test_create_transaction():

    data = {
        'bag':'25KILO',
        'quantity':1,
        'stock_id':3
    }
    # Fire the request
    res = client.post(url="/transaction",json=data,allow_redirects=True)
    # Response body as bd
    bd = res.json()
    # Check status code 
    assert res.status_code == 201

    with Session(engine) as session:
        # Fetch data from database 
        db = session.get(Transaction,bd['id'])
        # bd:Dict -> bd:Transaction 
        bd = Transaction(**bd)

        # Check id 
        assert db.id == bd.id
        # Check date 
        assert db.date == bd.date
        # Check bag 
        assert db.bag == bd.bag
        # Check quantity 
        assert db.quantity == bd.quantity
        # Check price 
        assert db.price == bd.price
        # Check stock id 
        assert db.stock_id == bd.stock_id


def test_create_transaction_404_status():

    data = {
        'bag':'10KILO',
        'quantity':2,
        'stock_id':20
    }

    res = client.post(url="/transaction",json=data,allow_redirects=True)

    assert res.status_code == 404

def test_create_transaction_bad_requets():

    data = {
        'bag':'10KILO',
        'quantity':100,
        'stock_id':6
    }

    res = client.post(url="/transaction",json=data,allow_redirects=True)

    assert res.status_code == 400

def test_get_transaction():

    res = client.get(url="/transaction",allow_redirects=True)

    # Response body as bd 
    bd = res.json()

    with Session(engine) as session:

        statement = select(Transaction)
        results =  session.exec(statement).all()
        db = [result.__dict__ for result in results]

        assert len(bd) == len(db)

        for i in range(len(db)):

            # Check id 
            assert db[i]['id'] == bd[i]['id']
            # Check bag 
            assert db[i]['bag'] == bd[i]['bag']
            # Check quantity 
            assert db[i]['quantity'] == bd[i]['quantity']
            # Check price 
            assert db[i]['price'] == bd[i]['price']
            # Check stock id 
            assert db[i]['stock_id'] == bd[i]['stock_id']

        
            


