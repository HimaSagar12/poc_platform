from pydantic import BaseModel
from typing import List, Optional
import datetime
from enum import Enum

class Designation(str, Enum):
    i07 = "i07"
    i08 = "i08"
    i09 = "i09"
    i10 = "i10"
    i11 = "i11"
    i12 = "i12"
    i13 = "i13"
    i14 = "i14"
    i15 = "i15"
    i16 = "i16"

class UserBase(BaseModel):
    email: str
    full_name: str
    designation: Designation

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    average_rating: float
    notifications: List['Notification'] = []
    reviews_received: List['Review'] = []

    class Config:
        from_attributes = True

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
        from_attributes = True

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
        from_attributes = True

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
        from_attributes = True

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
        from_attributes = True


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
        from_attributes = True


