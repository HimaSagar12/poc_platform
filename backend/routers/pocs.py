from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    tags=["pocs"],
)

@router.post("/", response_model=schemas.POC)
def create_poc(poc: schemas.POCCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_poc(db=db, poc=poc, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.POC])
def read_pocs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pocs = crud.get_pocs(db, skip=skip, limit=limit)
    return pocs

@router.get("/{poc_id}", response_model=schemas.POC)
def read_poc(poc_id: int, db: Session = Depends(get_db)):
    db_poc = crud.get_poc(db, poc_id=poc_id)
    if db_poc is None:
        raise HTTPException(status_code=404, detail="POC not found")
    return db_poc
