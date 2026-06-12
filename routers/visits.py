from fastapi import APIRouter , Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.visit import Visit
from schemas.visit import VisitCreate , VisitResponse , VisitUpdate
from models.pet import Pet


router=APIRouter(
    prefix="/visits",
    tags=["visits"]
)

def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()

@router.post("/{pet_id}/visits",response_model=VisitResponse)
def create_visit(
    pet_id:int,
    visit: VisitCreate,
    db: Session = Depends(get_db)    
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )
    new_visit = Visit(
        pet_id=pet_id,
        reason=visit.reason,
        notes=visit.notes
    )

    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)

    return new_visit

@router.get("/{pet_id}/visits",response_model=list[VisitResponse])
def get_pet_visist(
    pet_id :int,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )
    
    visits = db.query(Visit).filter(
        Visit.pet_id == pet_id
    ).all()

    return visits

@router.put("/{visit_id}",response_model=VisitResponse)
def update_visit(
    visit_id:int,
    updated_visit:VisitUpdate,
    db: Session = Depends(get_db)
):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if not visit: 
        raise HTTPException(
            status_code=404,
            detail="visit not found"
        )
    
    visit.reason = updated_visit.reason
    visit.notes = updated_visit.notes
    visit.visit_date = updated_visit.visit_date

    db.commit()
    db.refresh(visit)

    return visit

@router.delete("/{visit_id}")
def deleted_visit(
    visit_id: int,
    db: Session = Depends(get_db)
):
    visit = db.query(Visit).filter(Visit.id == visit_id).first()

    if not visit:
        raise HTTPException(
            status_code=404,
            detail="visit not found"
        )
    
    db.delete(visit)
    db.commit()
    
    return {
        "message" : "Visit deleted Succesfully"
    }



