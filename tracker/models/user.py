from pydantic import BaseModel, ConfigDict


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    first_name: str
    last_name: str

class UserResponse(User):
    new_token: str

class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str
    

class UserLogin(BaseModel):
    username: str
    password: str