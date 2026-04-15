from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import PatientService
from app.utils.database import get_db
from app.utils.security import get_current_patient

router = APIRouter(prefix="/api/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Create patient profile"""
    
    # Check if patient already exists for this user
    existing = PatientService.get_patient_by_user_id(db, user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient profile already exists for this user"
        )
    
    db_patient = PatientService.create_patient(db, patient, user_id)
    return db_patient

@router.get("/me", response_model=PatientResponse)
def get_my_profile(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get current patient's profile"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient by ID"""
    patient = PatientService.get_patient_by_id(db, patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Update patient profile"""
    
    patient = PatientService.get_patient_by_id(db, patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Only allow patients to update their own profile
    if patient.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this patient"
        )
    
    updated_patient = PatientService.update_patient(db, patient_id, patient_update)
    return updated_patient
