from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.pet import Pet
from schemas.pet import PetCreate , PetResponse , PetUpdate
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
        owner_id=pet.owner_id
    )            
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return new_pet

@router.get("/",response_model=list[PetResponse])
def get_all_pets(
    species: str = None,
    breed: str = None,
    min_age: int = None,
    max_age: int = None,
    search : str = None,
    sort_by : str =None,
    sort_order : str = None,
    limit : int = 10,
    page : int = 1,
    db: Session = Depends(get_db)
):
    query = db.query(Pet).filter(Pet.is_deleted == False)

    if  species:
        query = query.filter(Pet.species == species)

    if breed:
        query = query.filter(Pet.breed == breed)

    if min_age:
        query= query.filter(Pet.age >= min_age)

    if max_age:
        query = query.filter(Pet.age <= max_age)  

    if search:
        query = query.filter(Pet.name.ilike(f"%{search}%"))   

    if sort_by == "name":

        if sort_order == "desc":
            query = query.order_by(Pet.name.desc())

        else:
            query = query.order_by(Pet.name)   

    elif sort_by == "age":

        if sort_order == "desc":
            query = query.order_by(Pet.age.desc())

        else:
            query = query.order_by(Pet.age)  

    elif sort_by == "created_at":

        if sort_order == "desc":
            query = query.order_by(Pet.created_at.desc())

        else:
            query = query.order_by(Pet.created_at)                           

    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)     

    pets = query.all()          

    return pets

@router.get("/{pet_id}",response_model=PetResponse)
def get_pet(
    pet_id:int,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.is_deleted == False).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="pet not found"
        )
    
    return pet

@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id:int,
    updated_pet: PetUpdate,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            stauts_code=404,
            detail="pet not found"
        )
    pet.name = updated_pet.name
    pet.species = updated_pet.species
    pet.breed = updated_pet.breed
    pet.age = updated_pet.age
    pet.owner_id = updated_pet.owner_id
    

    db.commit()
    db.refresh(pet)

    return pet

@router.delete("/{pet_id}")
def delete_pet(
    pet_id:int,
    db: Session = Depends(get_db)
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if not pet:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    pet.is_deleted = True
    db.commit()
    db.refresh(pet)

    return {
        "message": "Pet deleted successfully"
    }