from pydantic import BaseModel
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    designation: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    average_rating: float

    class Config:
        orm_mode = True

class POCBase(BaseModel):
    title: str
    description: str

class POCCreate(POCBase):
    pass

class POC(POCBase):
    id: int
    created_at: datetime.datetime
    owner: User

    class Config:
        orm_mode = True

class ApplicationBase(BaseModel):
    poc_id: int

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    applicant: User
    status: str

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    text: str
    poc_id: int
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: datetime.datetime
    author: User
    replies: List['Comment'] = []

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: float
    comment: str
    reviewee_id: int
    poc_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    reviewer: User

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
