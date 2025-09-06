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
    notifications: List['Notification'] = []
    reviews_received: List['Review'] = []

    class Config:
        orm_mode = True

class POCBase(BaseModel):
    title: str
    description: str

class POCCreate(POCBase):
    owner_id: Optional[int] = None

class POC(POCBase):
    id: int
    created_at: datetime.datetime
    owner: User

    class Config:
        orm_mode = True

class ApplicationBase(BaseModel):
    poc_id: int

class ApplicationCreate(ApplicationBase):
    applicant_id: Optional[int] = None

class Application(ApplicationBase):
    id: int
    applicant: User
    poc: POC  # Add this line
    status: str

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    text: str
    poc_id: int
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    author_id: Optional[int] = None

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
    reviewer_id: Optional[int] = None

class Review(ReviewBase):
    id: int
    reviewer: User

    class Config:
        orm_mode = True


class NotificationBase(BaseModel):
    message: str
    link: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


