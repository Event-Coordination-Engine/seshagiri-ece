from fastapi import FastAPI,Depends,HTTPException
import model
from database import Base,engine,SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import Base,User
from DTOS import User_signupDTO,UserLoginDTO,UserResponseDTO
import re
from auth import get_password_hash, verify_password

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
@app.post("/signup", status_code=201)
def user_signup(user_obj : User_signupDTO,db :db_dependency):
                    

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

    #Encrpt the password
    encrypted_pwd = get_password_hash(user_obj.password)

    #define a user DTO object you want to pass
    user_obj = User(user_name = user_obj.user_name.strip(), 
                    email = user_obj.email,
                    password = encrypted_pwd) 
              
    db.add(user_obj)
    db.commit()
    return {"status_code" : 201 , "message" : "User Successfully Registered"}
    
@app.post("/login",status_code=200)
def login_user(user_login_obj : UserLoginDTO, db : db_dependency) :
    db_user = db.query(User).filter(User.email == user_login_obj.email).first()
    
    if not db_user :
        raise HTTPException(status_code=401, detail= "Unregistered Email")
    if not verify_password(user_login_obj.password, db_user.password) :
        raise HTTPException(status_code=401, detail="invalid Credentials")
    user_passon_dto = UserResponseDTO(email = db_user.email,
                                      user_id = db_user.user_id,
                                      name = db_user.user_name,
                                      Role = db_user.Role)
    return {"status code ": 200, "message" : "sucessfully Logged in....!", "body" : user_passon_dto}
                                      


