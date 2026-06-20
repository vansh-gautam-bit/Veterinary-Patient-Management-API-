from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.owner import Owner
from schemas.owner import OwnerCreate , OwnerResponse , OwnerUpdate
from fastapi import HTTPException
from models.user import User
from routers.users import get_current_user
from models.pet import Pet

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
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
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
    owners = db.query(Owner).filter(Owner.is_deleted==False).all()

    return owners

@router.get("/{owner_id}",response_model=OwnerResponse)
def get_owner(
    owner_id:int,
    db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter(Owner.id == owner_id,Owner.is_deleted==False).first()

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
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    owner = db.query(Owner).filter(Owner.id == owner_id,Owner.is_deleted==False).first()

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    owner = db.query(Owner).filter(Owner.id == owner_id,Owner.is_deleted == False).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )
    
    active_pets = db.query(Pet).filter(
        Pet.owner_id == owner_id,
        Pet.is_deleted == False
    ).all()
    
    if active_pets:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete owner with pets"
        )

    owner.is_deleted = True

    db.commit()
    db.refresh(owner)

    return {
        "message": "owner deleted successfully"
    }

