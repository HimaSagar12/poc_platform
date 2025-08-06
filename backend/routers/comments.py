from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..dependencies import get_db

router = APIRouter()

@router.post("/comments", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, author_id=comment.author_id)

@router.get("/comments/poc/{poc_id}", response_model=List[schemas.Comment])
def read_comments_for_poc(poc_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments_for_poc(db, poc_id=poc_id)
    return comments
