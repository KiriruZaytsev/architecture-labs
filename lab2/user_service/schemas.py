from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    login: str
    email: EmailStr
