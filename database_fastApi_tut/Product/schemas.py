from pydantic import BaseModel, Field
from typing import List, Optional

class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    name: str
    description: str
    price: int

class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: Optional[List[DisplaySeller]] 

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
