from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.users import UserCreate , UserResponse ,UserLogin
from fastapi import HTTPException
from utils.security import hash_password
from utils.security import verify_password , create_access_token
from jose import JWTError, jwt
from config import settings


from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

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

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
        try:
            payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("user_id")

            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                    )
            
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="User not found"
                )        
            return user

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
                
    )    

@router.get("/user-context")
def get_user_context(
    current_user: User = Depends(get_current_user)
):
    return current_user


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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db:Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
        
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email":user.email,
            "role":user.role.value
            }
    )    
    
    return{
        "access_token":access_token,
        "token_type":"bearer"
    }