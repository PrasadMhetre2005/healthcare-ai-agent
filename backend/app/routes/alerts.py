from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService
from app.services.patient_service import PatientService
from app.utils.database import get_db
from app.utils.security import get_current_patient

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("/me", response_model=list[AlertResponse])
def get_my_alerts(
    user_id: int = Depends(get_current_patient),
    unresolved_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get current user's alerts"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    alerts = AlertService.get_patient_alerts(db, patient.id, unresolved_only)
    return alerts

@router.get("/me/unresolved", response_model=list[AlertResponse])
def get_my_unresolved_alerts(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get current user's unresolved alerts"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    alerts = AlertService.get_patient_alerts(db, patient.id, unresolved_only=True)
    return alerts

@router.get("/patient/{patient_id}", response_model=list)
def get_patient_alerts(
    patient_id: int,
    unresolved_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get alerts for a patient"""
    alerts = AlertService.get_patient_alerts(db, patient_id, unresolved_only)
    return alerts

@router.get("/patient/{patient_id}/unresolved", response_model=list)
def get_unresolved_alerts(patient_id: int, db: Session = Depends(get_db)):
    """Get unresolved alerts for a patient"""
    alerts = AlertService.get_patient_alerts(db, patient_id, unresolved_only=True)
    return alerts

@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Mark an alert as resolved"""
    alert = AlertService.mark_alert_resolved(db, alert_id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert
