from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.pet import Pet
from schemas.pet import PetCreate , PetResponse
from fastapi import HTTPException

router = APIRouter(
    prefix="/pets",
    tags=["Pets"]
)

def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PetResponse)
def create_pet(
    pet: PetCreate,
    db: Session = Depends(get_db )
):
    new_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        age=pet.age,
        owner_name=pet.owner_name,
        owner_phone=pet.owner_phone
    )            
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/",response_model=list[PetResponse])
def get_all_pets(
    db: Session = Depends(get_db)
):
    pets = db.query(Pet).all()

    return pets

@router.get("/{pet_id}",response_model=PetResponse)
def get_pet(
    pet_id:int,
    db: Session = Depends(get_db)
):
    pet = db.query(pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="pet not found"
        )
    
    return pet
