from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password:str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    created_at: datetime
    id: int

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostRespose(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

class PostOut(BaseModel):
    Post: PostRespose
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
