from pydantic import BaseModel, ConfigDict


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

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