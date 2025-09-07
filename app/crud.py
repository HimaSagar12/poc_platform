from sqlalchemy.orm import Session
from app import models, schemas

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password, full_name=user.full_name, designation=user.designation)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# POC CRUD
def get_poc(db: Session, poc_id: int):
    return db.query(models.POC).filter(models.POC.id == poc_id).first()

def get_pocs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.POC).offset(skip).limit(limit).all()

def create_poc(db: Session, poc: schemas.POCCreate):
    db_poc = models.POC(**poc.dict())
    db.add(db_poc)
    db.commit()
    db.refresh(db_poc)
    # Notify POC owner
    create_notification(db, user_id=db_poc.owner_id, message=f"New POC '{db_poc.title}' has been created.", link=f"/pocs/{db_poc.id}")
    return db_poc

def get_pocs_by_owner(db: Session, owner_id: int):
    return db.query(models.POC).filter(models.POC.owner_id == owner_id).all()

def delete_poc(db: Session, poc_id: int):
    db_poc = db.query(models.POC).filter(models.POC.id == poc_id).first()
    if db_poc:
        db.delete(db_poc)
        db.commit()
    return db_poc


# Application CRUD
def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

from sqlalchemy.orm import Session, joinedload
from app import models, schemas

# Application CRUD
def get_applications_for_poc(db: Session, poc_id: int):
    return db.query(models.Application).options(joinedload(models.Application.poc), joinedload(models.Application.applicant)).filter(models.Application.poc_id == poc_id).all()

def create_application(db: Session, application: schemas.ApplicationCreate):
    application_data = application.dict()
    db_application = models.Application(**application_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    # Notify POC owner
    poc = get_poc(db, application.poc_id)
    create_notification(db, user_id=poc.owner_id, message=f"A new application has been submitted for your POC '{poc.title}'.", link=f"/pocs/{poc.id}/applications")
    return db_application

def update_application_status(db: Session, application_id: int, status: str):
    db_application = get_application(db, application_id)
    if db_application:
        db_application.status = status
        db.commit()
        db.refresh(db_application)
        # Notify applicant
        create_notification(db, user_id=db_application.applicant_id, message=f"The status of your application for POC '{db_application.poc.title}' has been updated to '{status}'.", link=f"/applications/{db_application.id}")
    return db_application

def get_applications_by_applicant(db: Session, applicant_id: int):
    applications = db.query(models.Application).options(joinedload(models.Application.poc), joinedload(models.Application.applicant)).filter(models.Application.applicant_id == applicant_id).all()
    for app in applications:
        if app.poc is None:
            print(f"WARNING: Application ID {app.id} has a missing POC relationship.")
    return applications

# Comment CRUD
def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    # Notify POC owner
    poc = get_poc(db, comment.poc_id)
    if poc.owner_id != comment.author_id:
        create_notification(db, user_id=poc.owner_id, message=f"A new comment has been posted on your POC '{poc.title}'.", link=f"/pocs/{poc.id}")
    # Notify parent comment author
    if comment.parent_id:
        parent_comment = db.query(models.Comment).filter(models.Comment.id == comment.parent_id).first()
        if parent_comment and parent_comment.author_id != comment.author_id:
            create_notification(db, user_id=parent_comment.author_id, message=f"Someone has replied to your comment on POC '{poc.title}'.", link=f"/pocs/{poc.id}")
    return db_comment

def get_comments_for_poc(db: Session, poc_id: int):
    return db.query(models.Comment).filter(models.Comment.poc_id == poc_id, models.Comment.parent_id.is_(None)).all()

# Review CRUD
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()

    # Update average rating
    reviewee = get_user(db, review.reviewee_id)
    reviews = db.query(models.Review).filter(models.Review.reviewee_id == review.reviewee_id).all()
    if reviews:
        total_rating = sum([r.rating for r in reviews])
        reviewee.average_rating = total_rating / len(reviews)
    else:
        reviewee.average_rating = 0.0
    db.commit()
    db.refresh(db_review)

    # Notify reviewee
    create_notification(db, user_id=review.reviewee_id, message=f"You have received a new review.", link=f"/users/{review.reviewee_id}")

    return db_review

# Notification CRUD
def create_notification(db: Session, user_id: int, message: str, link: str = None):
    db_notification = models.Notification(user_id=user_id, message=message, link=link)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications_for_user(db: Session, user_id: int):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.created_at.desc()).all()

def mark_notification_as_read(db: Session, notification_id: int):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)
    return db_notification
