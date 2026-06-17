from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.users import UserCreate , UserResponse ,UserLogin
from fastapi import HTTPException
from utils.security import hash_password
from utils.security import verify_password , create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Users"]
)

def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db )
):
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )            
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login")
def login_user(
    user_data:UserLogin,
    db:Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
        
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )    
    
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }