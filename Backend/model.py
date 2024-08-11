from database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__="user"

    user_id=Column(Integer,primary_key=True)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=True)
    email=Column(String,nullable=False)
    password=Column(String,nullable=False)