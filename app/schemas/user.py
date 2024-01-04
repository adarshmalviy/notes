from typing import Optional, List

from pydantic import BaseModel


# User registration request model
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


# User login request model
class UserLogin(BaseModel):
    username: str
    password: str
