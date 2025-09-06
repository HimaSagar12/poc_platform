from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()

@router.get("/{user_id}", response_model=List[schemas.Notification])
def read_notifications_for_user(user_id: int, db: Session = Depends(get_db)):
    notifications = crud.get_notifications_for_user(db, user_id=user_id)
    return notifications

@router.put("/{notification_id}/read", response_model=schemas.Notification)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db)):
    db_notification = crud.mark_notification_as_read(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification
