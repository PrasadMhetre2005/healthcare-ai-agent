from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.models.patient import Patient
from app.services.auth_service import AuthService
from app.services.doctor_service import DoctorService
from app.utils.database import get_db
from app.utils.security import get_current_doctor
import os
import shutil
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads/licenses")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/register")
def register_doctor(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    medical_license: str = Form(...),
    specialization: str = Form(...),
    years_of_experience: int = Form(0),
    hospital_name: str = Form(None),
    office_address: str = Form(None),
    bio: str = Form(None),
    license_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Register a new doctor with license upload"""
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if doctor email/phone already exists
        existing_doctor = db.query(Doctor).filter(
            (Doctor.email == email) | (Doctor.phone == phone) | (Doctor.medical_license == medical_license)
        ).first()
        
        if existing_doctor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email, phone, or license already registered"
            )
        
        # Save license file
        license_file_path = None
        if license_file:
            file_extension = Path(license_file.filename).suffix
            filename = f"license_{medical_license}_{int(time.time())}{file_extension}"
            file_path = UPLOAD_DIR / filename
            
            with open(file_path, "wb") as f:
                shutil.copyfileobj(license_file.file, f)
            
            license_file_path = str(file_path)
            logger.info(f"License file saved: {file_path}")
        
        # Create user
        db_user = User(
            username=email,  # Use email as username
            email=email,
            hashed_password=AuthService.hash_password(password),
            role="doctor"
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Doctor user created: {email} (ID: {db_user.id})")
        
        # Create doctor profile
        db_doctor = Doctor(
            user_id=db_user.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            medical_license=medical_license,
            license_file_path=license_file_path,
            license_verified=False,  # Admin will verify later
            specialization=specialization,
            years_of_experience=years_of_experience,
            hospital_name=hospital_name,
            office_address=office_address,
            bio=bio,
            is_active=True
        )
        
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        logger.info(f"Doctor profile created: {email} (ID: {db_doctor.id})")
        
        return {
            "message": "Registration successful. Your license will be verified by admin.",
            "doctor_id": db_doctor.id,
            "email": db_doctor.email
        }
    
    except Exception as e:
        logger.error(f"Doctor registration error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login")
def login_doctor(credentials: dict, db: Session = Depends(get_db)):
    """Login doctor - can use email or phone"""
    
    try:
        email = credentials.get("email")
        phone = credentials.get("phone")
        username = credentials.get("username")
        password = credentials.get("password")
        
        # Find user by email or phone
        db_user = None
        if email:
            db_user = db.query(User).filter(User.email == email).first()
        elif phone:
            db_doctor = DoctorService.get_doctor_by_phone(db, phone)
            if db_doctor:
                db_user = db.query(User).filter(User.id == db_doctor.user_id).first()
        elif username:
            db_user = db.query(User).filter(User.username == username).first()
        
        if not db_user or not AuthService.verify_password(password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if db_user.role != "doctor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a doctor"
            )
        
        # Get doctor profile
        doctor = DoctorService.get_doctor_by_user_id(db, db_user.id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor profile not found"
            )
        
        # Create access token
        access_token = AuthService.create_access_token(
            data={"sub": str(db_user.id), "role": "doctor"}
        )
        
        logger.info(f"Doctor logged in: {db_user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "doctor": {
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "email": doctor.email,
                "specialization": doctor.specialization,
                "hospital_name": doctor.hospital_name
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Doctor login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/dashboard/stats")
def get_dashboard_stats(
    doctor_id: int = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get dashboard overview statistics"""
    stats = DoctorService.get_dashboard_stats(db, doctor_id)
    return stats

@router.get("/patients")
def get_patients(
    doctor_id: int = Depends(get_current_doctor),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get list of patients for doctor"""
    patients = DoctorService.get_doctor_patients(db, doctor_id, limit, offset)
    return {"patients": patients}

@router.get("/alerts")
def get_alerts(
    doctor_id: int = Depends(get_current_doctor),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get alerts for doctor's patients"""
    alerts = DoctorService.get_doctor_alerts(db, doctor_id, limit)
    return {"alerts": alerts}

@router.get("/care-gaps")
def get_care_gaps(
    doctor_id: int = Depends(get_current_doctor),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get care gaps for doctor's patients"""
    gaps = DoctorService.get_care_gaps(db, doctor_id, limit)
    return {"care_gaps": gaps}

@router.get("/appointments")
def get_appointments(
    doctor_id: int = Depends(get_current_doctor),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get upcoming appointments"""
    appointments = DoctorService.get_upcoming_appointments(db, doctor_id, limit)
    return {"appointments": appointments}

@router.get("/patients/{patient_id}")
def get_patient_profile(
    patient_id: int,
    doctor_id: int = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get patient profile for doctor"""
    profile = DoctorService.get_patient_profile(db, doctor_id, patient_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found or you don't have access"
        )
    
    return profile

@router.get("/profile")
def get_doctor_profile(
    doctor_id: int = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get doctor's own profile"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found"
        )
    
    return {
        "id": doctor.id,
        "first_name": doctor.first_name,
        "last_name": doctor.last_name,
        "email": doctor.email,
        "phone": doctor.phone,
        "specialization": doctor.specialization,
        "hospital_name": doctor.hospital_name,
        "office_address": doctor.office_address,
        "bio": doctor.bio,
        "years_of_experience": doctor.years_of_experience,
        "patients_count": doctor.patients_count,
        "license_verified": doctor.license_verified
    }

# Keep old endpoints for compatibility
@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    """Create doctor profile (admin only in production)"""
    
    # Check if doctor already exists (by license)
    existing = db.query(Doctor).filter(
        Doctor.medical_license == doctor.medical_license
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this license already exists"
        )
    
    db_doctor = Doctor(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        medical_license=doctor.medical_license,
        specialization=doctor.specialization,
        hospital_name=doctor.hospital_name,
        phone=doctor.phone,
        bio=doctor.bio
    )
    
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    
    return db_doctor

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor by ID"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    return doctor

@router.get("/", response_model=list)
def get_all_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all doctors"""
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors

@router.get("/specialization/{specialization}", response_model=list)
def get_doctors_by_specialization(
    specialization: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get doctors by specialization"""
    doctors = db.query(Doctor).filter(
        Doctor.specialization.ilike(f"%{specialization}%")
    ).offset(skip).limit(limit).all()
    
    return doctors
