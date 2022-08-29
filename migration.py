
from sqlmodel import Session
from models import Stock
from database import engine,create_db_and_table
from time import sleep
from random import randint

def create(r):
    with Session(engine) as session:
        stock = Stock(name=r[0],unit=r[1],small=r[2],medium=r[3],large=r[4])
        session.add(stock)
        session.commit()
        session.refresh(stock)
        sleep(1)
        return stock.__dict__
        

def migration():
    create_db_and_table()
    name = ['සුදු කැකුලු','නාඩු', 'කිරි කැකුලු' ,'සම්බා කැකුලු', 'රතු කැකුලු' ,'රොස කැකුලු', 'කිරි සම්බා (තම්බපු)', 'සම්බා (තම්බපු )' ,'කැඩුණු හාල්' ,'බාස්මති','ආටාකාරිය','සුවදැල්','පච්චපෙරුමාල්','බටපොලාඇල්']
    price = [206,215,245,215,210,210,260,220,210,245,300,300,300,300]
    small,medium,large = [randint(0, 100) for i in range(14)], [randint(0, 100) for i in range(14)], [randint(0, 100) for i in range(14)]
    rows = list(zip(name,price,small,medium,large))
    instances =  [create(row) for row in rows]
    print(instances)

migration()