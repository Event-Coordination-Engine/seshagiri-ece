from model import User
from pydantic import BaseModel

#create a DTO for user signup
class User_signupDTO(BaseModel):
    user_name : str = None
    email : str = None
    password : str = None
   
