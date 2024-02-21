from pydantic import BaseModel

class Signup(BaseModel):
    name: str
    username: str
    phoneNumber: str
    email: str
    password: str

class User(BaseModel):
    username: str
    password: str