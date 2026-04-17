from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.services.auth_service import AuthService
import os

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    """Dependency for protected routes"""
    token = credentials.credentials
    payload = AuthService.decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    return int(user_id)

async def get_current_doctor(user_id: int = Depends(get_current_user)):
    """Dependency for doctor-only routes - returns doctor_id"""
    from app.services.doctor_service import DoctorService
    from app.utils.database import SessionLocal
    
    db = SessionLocal()
    try:
        doctor = DoctorService.get_doctor_by_user_id(db, user_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a doctor"
            )
        return doctor.id
    finally:
        db.close()

async def get_current_patient(user_id: int = Depends(get_current_user)):
    """Dependency for patient-only routes - returns patient_id"""
    from app.models.patient import Patient
    from app.utils.database import SessionLocal
    
    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.user_id == user_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a patient"
            )
        return patient.id
    finally:
        db.close()
