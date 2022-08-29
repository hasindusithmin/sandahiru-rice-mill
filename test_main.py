
from fastapi.testclient import TestClient
from main import app
from models import Stock
from sqlmodel import Session,select
from database import engine

# Create Test Client 
client = TestClient(app)

def test_get_stock_details():
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

