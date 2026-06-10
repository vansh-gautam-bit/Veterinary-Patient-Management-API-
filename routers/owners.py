from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.owner import Owner
from schemas.owner import OwnerCreate , OwnerResponse , OwnerUpdate
from fastapi import HTTPException

router = APIRouter(
    prefix="/owners",
    tags=["Owners"]
)

def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OwnerResponse)
def create_owner(
    owner: OwnerCreate,
    db: Session = Depends(get_db )
):
    new_owner = Owner(
        name= owner.name,
        phone= owner.phone,
        email= owner.email
    )            
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    return new_owner

@router.get("/",response_model=list[OwnerResponse])
def get_all_owners(
    db: Session = Depends(get_db)
):
    owners = db.query(Owner).all()

    return owners

@router.get("/{owner_id}",response_model=OwnerResponse)
def get_owner(
    owner_id:int,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="owner not found"
        )
    
    return owner

@router.put("/{owner_id}", response_model=OwnerResponse)
def update_owner(
    owner_id:int,
    updated_owner: OwnerUpdate,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="owner not found"
        )
    owner.name = updated_owner.name,
    owner.phone = updated_owner.phone,
    owner.email = updated_owner.email

    db.commit()
    db.refresh(owner)

    return owner

@router.delete("/{owner_id}")
def delete_owner(
    owner_id:int,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    db.delete(owner)
    db.commit()

    return {
        "message": "owner deleted successfully"
    }
    