
from sqlmodel import SQLModel,create_engine


engine = create_engine(url="sqlite:///db/database.db",connect_args={'check_same_thread':False})


def create_db_and_table():
    SQLModel.metadata.create_all(bind=engine)
