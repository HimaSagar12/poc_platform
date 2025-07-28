from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)

@router.post("/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_application(db=db, application=application, applicant_id=current_user.id)

@router.get("/poc/{poc_id}", response_model=List[schemas.Application])
def read_applications_for_poc(poc_id: int, db: Session = Depends(get_db)):
    applications = crud.get_applications_for_poc(db, poc_id=poc_id)
    return applications

@router.put("/{application_id}/status", response_model=schemas.Application)
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    poc = crud.get_poc(db, application.poc_id)
    if poc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this application")
    return crud.update_application_status(db, application_id, status)
