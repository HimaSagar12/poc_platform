from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from ..dependencies import get_db

router = APIRouter(
    prefix="/reviews",
)

@router.get("/test")
def test_endpoint():
    return {"message": "test endpoint reached"}

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    print("create_review endpoint called")
    poc = crud.get_poc(db, review.poc_id)
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    
    application = db.query(models.Application).filter(
        models.Application.poc_id == review.poc_id,
        models.Application.applicant_id == review.reviewee_id
    ).first()

    if not application or application.status != "Selected":
        raise HTTPException(status_code=403, detail="Can only review applicants with 'Selected' status")

    return crud.create_review(db=db, review=review)

