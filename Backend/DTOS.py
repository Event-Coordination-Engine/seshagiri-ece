from pydantic import BaseModel

#create a DTO for user signup
class User_signupDTO(BaseModel):
    user_name : str = None
    email : str = None
    password : str = None
   
class UserLoginDTO(BaseModel):
    email : str = None
    password : str = None

class UserResponseDTO(BaseModel) :
    email : str
    user_id : int
    name : str
    Role : str

