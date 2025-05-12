from pydantic import BaseModel, ConfigDict

class UserToModify(BaseModel):
    first_name: str
    last_name: str 
    username: str 

class UserIn(UserToModify):
    password: str

class User(UserToModify):
    id: int

class UserResponse(BaseModel):
    new_token: str
    token_type: str
    user: User


class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str
    

class UserLogin(BaseModel):
    username: str
    password: str