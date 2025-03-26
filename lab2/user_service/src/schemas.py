from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    name: str
    login: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None