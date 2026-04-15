from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.models.user import User
from app.models.patient import Patient
from app.services.auth_service import AuthService
from app.utils.database import get_db
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create new user
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=AuthService.hash_password(user.password),
            role=user.role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered: {db_user.username} (ID: {db_user.id})")
        
        # Automatically create a patient profile for patient users
        if user.role == "patient":
            db_patient = Patient(
                user_id=db_user.id,
                first_name="",
                last_name="",
                date_of_birth="",
                gender="",
                blood_type="",
                allergies="",
                medical_history="",
                current_medications="",
                emergency_contact="",
                emergency_phone=""
            )
            db.add(db_patient)
            db.commit()
            logger.info(f"Patient profile created for user: {db_user.username}")
        
        return db_user
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        
        if not db_user:
            logger.warning(f"Login attempt with non-existent user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not AuthService.verify_password(user.password, db_user.hashed_password):
            logger.warning(f"Login attempt with wrong password for user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create access token
        access_token = AuthService.create_access_token(
            data={"sub": str(db_user.id), "role": db_user.role}
        )
        
        logger.info(f"User logged in: {db_user.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
                "role": db_user.role
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
