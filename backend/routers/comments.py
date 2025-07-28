from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

@router.post("/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_comment(db=db, comment=comment, author_id=current_user.id)

@router.get("/poc/{poc_id}", response_model=List[schemas.Comment])
def read_comments_for_poc(poc_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments_for_poc(db, poc_id=poc_id)
    return comments
