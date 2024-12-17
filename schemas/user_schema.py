from models.user_model import User
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

UserGet = pydantic_model_creator(User, name="UserGet")


class UserPost(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(min_length=4, max_length=150)
    last_name: Optional[str] = Field(min_length=4, max_length=150)
    password_hash: str = Field(alias="password", min_length=8, max_length=150)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=150)



