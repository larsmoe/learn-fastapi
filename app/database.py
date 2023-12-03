from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
only for documentation purposes (in case of pure sql)
while True:
    try:
        conn = psycopg.connect(host='localhost', dbname='learn-fastapi', user='postgres', password='Msvduisburg.94', row_factory=dict_row)
        cursor = conn.cursor()
        print('Database Connection successful')
        break
    except Exception as error:
        print("Connectiing to Database failed")
        print(f'Error: {error}')
        sleep(5)
'''