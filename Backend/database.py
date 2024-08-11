from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL="postgresql+psycopg2://postgres:seshu123@localhost/ECE_DB"

engine=create_engine(URL)

Base=declarative_base()

SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)