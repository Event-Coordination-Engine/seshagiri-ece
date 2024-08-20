from database import Base
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime

class User(Base):
    __tablename__="user"

    user_id = Column(Integer, primary_key = True)
    user_name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    Role = Column(String, nullable = False, default="User")
    registered_date = Column(DateTime, nullable=False, default= datetime.now())
    