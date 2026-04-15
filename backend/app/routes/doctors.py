from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.models.doctor import Doctor
from app.utils.database import get_db
from app.utils.security import get_current_patient

router = APIRouter(prefix="/api/doctors", tags=["doctors"])

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
