from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.health_data import HealthDataCreate, HealthDataResponse
from app.services.health_data_service import HealthDataService
from app.services.alert_service import AlertService
from app.services.patient_service import PatientService
from app.utils.database import get_db
from app.utils.security import get_current_patient

router = APIRouter(prefix="/api/health-data", tags=["health-data"])

@router.post("/", response_model=HealthDataResponse)
def log_health_data(
    health_data: HealthDataCreate,
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Log health data for current patient"""
    
    # Get patient ID from user_id
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    # Create health record
    db_health_data = HealthDataService.create_health_record(db, patient.id, health_data)
    
    # Check for anomalies and create alerts
    AlertService.check_health_anomalies(db, patient.id, db_health_data)
    
    return db_health_data

@router.get("/me/latest", response_model=HealthDataResponse)
def get_my_latest_health_record(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get current user's latest health record"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    record = HealthDataService.get_latest_health_record(db, patient.id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found"
        )
    
    return record

@router.get("/me", response_model=list[HealthDataResponse])
def get_my_health_records(
    user_id: int = Depends(get_current_patient),
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get current user's health records"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    records = HealthDataService.get_patient_health_records(db, patient.id, days)
    return records

@router.get("/me/trends")
def get_my_health_trends(
    user_id: int = Depends(get_current_patient),
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get current user's health trends"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    trends = HealthDataService.get_health_trends(db, patient.id, days)
    return trends

@router.get("/patient/{patient_id}", response_model=list)
def get_patient_health_records(
    patient_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get health records for a patient"""
    records = HealthDataService.get_patient_health_records(db, patient_id, days)
    return records

@router.get("/patient/{patient_id}/latest", response_model=HealthDataResponse)
def get_latest_health_record(patient_id: int, db: Session = Depends(get_db)):
    """Get latest health record for a patient"""
    record = HealthDataService.get_latest_health_record(db, patient_id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found"
        )
    
    return record

@router.get("/patient/{patient_id}/trends")
def get_health_trends(patient_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get health trends for a patient"""
    trends = HealthDataService.get_health_trends(db, patient_id, days)
    return trends
