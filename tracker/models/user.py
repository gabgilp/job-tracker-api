from pydantic import BaseModel, EmailStr, ConfigDict


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str

class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)
    hashed_password: str
    