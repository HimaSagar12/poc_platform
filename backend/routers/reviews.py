from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    poc = crud.get_poc(db, review.poc_id)
    if not poc:
        raise HTTPException(status_code=404, detail="POC not found")
    if poc.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to review for this POC")
    
    application = db.query(models.Application).filter(
        models.Application.poc_id == review.poc_id,
        models.Application.applicant_id == review.reviewee_id
    ).first()

    if not application or application.status != "Selected":
        raise HTTPException(status_code=403, detail="Can only review applicants with 'Selected' status")

    return crud.create_review(db=db, review=review, reviewer_id=current_user.id)
