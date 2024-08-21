from fastapi import FastAPI,Depends,HTTPException
import model
from database import Base,engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import Base,User
from DTOS import User_signupDTO
import re

app=FastAPI()

#create a tables provided metadata
model.Base.metadata.create_all(bind=engine)

#fetch database and Make a local session as long as we work on database
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

#set up database Dependency
db_dependency = Annotated[Session,Depends(get_db)]


#create a user signup function that post to database
@app.post("/signup/", status_code=201)
def user_signup(user_obj : User_signupDTO,db :db_dependency):

    #define a user DTO object you want to pass
    user_obj = User(user_name = user_obj.user_name.strip(), 
                    email = user_obj.email,
                    password = user_obj.password)
                    

    #check if the email exists or not
    email_check = db.query(User).filter(User.email == user_obj.email).first()

    if email_check:
        raise HTTPException(status_code=400, detail= "this Email already exists")
    
    #User signup details validation
    if not user_obj.email :
        raise HTTPException(status_code=400, detail= "Email can not be empty")
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",user_obj.email) : 
        raise HTTPException(status_code=400, detail= "Invalid Email format")
    
    if not user_obj.user_name.strip() :
        raise HTTPException(status_code=400, detail= "user name is mandatory")
    

    #validation password
    if not user_obj.password or len(user_obj.password.strip()) == 0:
       raise HTTPException(status_code=400, detail = "Please Provide Password")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@#$%^&+=]+$", user_obj.password):
        raise HTTPException(status_code=400, detail = "Weak Password detected. Use combination of Uppercase, lowercase and numbers")
    if len(user_obj.password) < 7 :
        raise HTTPException(status_code=400, detail = "Password should be atleast 7 characters")  
              
    db.add(user_obj)
    db.commit()
    return {"status_code" : 201 , "message" : "User Successfully Registered"}
    


