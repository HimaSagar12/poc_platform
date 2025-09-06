from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from app.dependencies import get_db

router = APIRouter()

@router.post("", response_model=schemas.POC)
def create_poc(poc: schemas.POCCreate, db: Session = Depends(get_db)):
    return crud.create_poc(db=db, poc=poc)

@router.get("", response_model=List[schemas.POC])
def read_pocs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pocs = crud.get_pocs(db, skip=skip, limit=limit)
    return pocs

@router.get("/{poc_id}", response_model=schemas.POC)
def read_poc(poc_id: int, db: Session = Depends(get_db)):
    db_poc = crud.get_poc(db, poc_id=poc_id)
    if db_poc is None:
        raise HTTPException(status_code=404, detail="POC not found")
    return db_poc

@router.get("/owner/{owner_id}", response_model=List[schemas.POC])
def read_pocs_by_owner(owner_id: int, db: Session = Depends(get_db)):
    pocs = crud.get_pocs_by_owner(db, owner_id=owner_id)
    return pocs

@router.delete("/{poc_id}")
def delete_poc(poc_id: int, owner_id: int, db: Session = Depends(get_db)):
    db_poc = crud.get_poc(db, poc_id=poc_id)
    if db_poc is None:
        raise HTTPException(status_code=404, detail="POC not found")
    if db_poc.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this POC")
    crud.delete_poc(db, poc_id=poc_id)
    return {"message": "POC deleted successfully"}
