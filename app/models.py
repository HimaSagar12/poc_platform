from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
    designation = Column(String)
    average_rating = Column(Float, default=0.0)

    pocs = relationship("POC", back_populates="owner")
    applications = relationship("Application", back_populates="applicant")
    comments = relationship("Comment", back_populates="author")
    reviews_given = relationship("Review", foreign_keys='Review.reviewer_id', back_populates="reviewer")
    reviews_received = relationship("Review", foreign_keys='Review.reviewee_id', back_populates="reviewee")
    notifications = relationship("Notification", back_populates="user")

class POC(Base):
    __tablename__ = "pocs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pocs")
    applications = relationship("Application", back_populates="poc")
    comments = relationship("Comment", back_populates="poc")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    poc_id = Column(Integer, ForeignKey("pocs.id"))
    applicant_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="Submitted") # Submitted, Under Review, Accepted, Rejected, Selected

    poc = relationship("POC", back_populates="applications")
    applicant = relationship("User", back_populates="applications")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    poc_id = Column(Integer, ForeignKey("pocs.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    poc = relationship("POC", back_populates="comments")
    author = relationship("User", back_populates="comments")
    replies = relationship("Comment", back_populates="parent")
    parent = relationship("Comment", back_populates="replies", remote_side=[id])

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    comment = Column(Text)
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    reviewee_id = Column(Integer, ForeignKey("users.id"))
    poc_id = Column(Integer, ForeignKey("pocs.id"))

    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewee = relationship("User", foreign_keys=[reviewee_id], back_populates="reviews_received")
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    link = Column(String, nullable=True)

    user = relationship("User", back_populates="notifications")
