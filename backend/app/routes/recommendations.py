from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.recommendation import RecommendationResponse
from app.models.recommendation import Recommendation
from app.services.ai_service import AIService
from app.services.health_data_service import HealthDataService
from app.services.alert_service import AlertService
from app.services.patient_service import PatientService
from app.utils.database import get_db
from app.utils.security import get_current_patient

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

@router.get("/me/generate")
def generate_my_recommendations(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Generate AI-powered health recommendations for current user"""
    
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    # Get patient health data
    health_records = HealthDataService.get_patient_health_records(db, patient.id, days=30)
    alerts = AlertService.get_patient_alerts(db, patient.id, unresolved_only=True)
    
    if not health_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found for this patient"
        )
    
    # Prepare data for AI
    health_data = {
        "latest": {
            "blood_pressure": f"{health_records[0].blood_pressure_systolic}/{health_records[0].blood_pressure_diastolic}",
            "heart_rate": health_records[0].heart_rate,
            "temperature": health_records[0].temperature,
            "blood_glucose": health_records[0].blood_glucose,
        }
    }
    
    records_data = [{
        "recorded_date": str(r.recorded_date),
        "blood_pressure_systolic": r.blood_pressure_systolic,
        "blood_pressure_diastolic": r.blood_pressure_diastolic,
        "heart_rate": r.heart_rate,
        "temperature": r.temperature,
        "blood_glucose": r.blood_glucose,
        "weight": r.weight
    } for r in health_records[:5]]
    
    alerts_data = [{"title": a.title, "message": a.message} for a in alerts[:3]]
    
    # Generate recommendations using AI
    ai_recommendations = AIService.generate_recommendations(health_data, records_data, alerts_data)
    
    # Save recommendations to database
    saved_recommendations = []
    for rec in ai_recommendations:
        db_rec = Recommendation(
            patient_id=patient.id,
            category=rec.get("category", "general"),
            priority=rec.get("priority", "medium"),
            title=rec.get("title", ""),
            description=rec.get("description", ""),
            reason=rec.get("reason", ""),
            generated_by="AI"
        )
        db.add(db_rec)
        saved_recommendations.append(db_rec)
    
    db.commit()
    
    return {
        "patient_id": patient.id,
        "recommendations": saved_recommendations,
        "generated_at": str(__import__('datetime').datetime.utcnow())
    }

@router.get("/me", response_model=list[RecommendationResponse])
def get_my_recommendations(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get recommendations for current user"""
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    recommendations = db.query(Recommendation).filter(
        Recommendation.patient_id == patient.id
    ).order_by(Recommendation.created_at.desc()).all()
    
    return recommendations

@router.get("/me/insights")
def get_my_health_insights(
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get AI-generated health insights for current user"""
    
    patient = PatientService.get_patient_by_user_id(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    health_records = HealthDataService.get_patient_health_records(db, patient.id, days=30)
    
    if not health_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found for this patient"
        )
    
    # Prepare data for AI
    health_data = {
        "latest": {
            "blood_pressure": f"{health_records[0].blood_pressure_systolic}/{health_records[0].blood_pressure_diastolic}",
            "heart_rate": health_records[0].heart_rate,
            "temperature": health_records[0].temperature,
        }
    }
    
    records_data = [{
        "recorded_date": str(r.recorded_date),
        "blood_pressure_systolic": r.blood_pressure_systolic,
        "blood_pressure_diastolic": r.blood_pressure_diastolic,
        "heart_rate": r.heart_rate,
    } for r in health_records[:5]]
    
    # Generate insights using AI
    insights = AIService.generate_health_insights(health_data, records_data)
    
    return {
        "patient_id": patient.id,
        "insights": insights,
        "generated_at": str(__import__('datetime').datetime.utcnow())
    }

@router.get("/patient/{patient_id}/generate")
def generate_recommendations(patient_id: int, db: Session = Depends(get_db)):
    """Generate AI-powered health recommendations for a patient"""
    
    # Get patient health data
    health_records = HealthDataService.get_patient_health_records(db, patient_id, days=30)
    alerts = AlertService.get_patient_alerts(db, patient_id, unresolved_only=True)
    
    if not health_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found for this patient"
        )
    
    # Prepare data for AI
    health_data = {
        "latest": {
            "blood_pressure": f"{health_records[0].blood_pressure_systolic}/{health_records[0].blood_pressure_diastolic}",
            "heart_rate": health_records[0].heart_rate,
            "temperature": health_records[0].temperature,
            "blood_glucose": health_records[0].blood_glucose,
        }
    }
    
    records_data = [{
        "recorded_date": str(r.recorded_date),
        "blood_pressure_systolic": r.blood_pressure_systolic,
        "blood_pressure_diastolic": r.blood_pressure_diastolic,
        "heart_rate": r.heart_rate,
        "temperature": r.temperature,
        "blood_glucose": r.blood_glucose,
        "weight": r.weight
    } for r in health_records[:5]]
    
    alerts_data = [{"title": a.title, "message": a.message} for a in alerts[:3]]
    
    # Generate recommendations using AI
    ai_recommendations = AIService.generate_recommendations(health_data, records_data, alerts_data)
    
    # Save recommendations to database
    saved_recommendations = []
    for rec in ai_recommendations:
        db_rec = Recommendation(
            patient_id=patient_id,
            category=rec.get("category", "general"),
            priority=rec.get("priority", "medium"),
            title=rec.get("title", ""),
            description=rec.get("description", ""),
            reason=rec.get("reason", ""),
            generated_by="AI"
        )
        db.add(db_rec)
        saved_recommendations.append(db_rec)
    
    db.commit()
    
    return {
        "patient_id": patient_id,
        "recommendations": saved_recommendations,
        "generated_at": str(__import__('datetime').datetime.utcnow())
    }

@router.get("/patient/{patient_id}", response_model=list)
def get_patient_recommendations(patient_id: int, db: Session = Depends(get_db)):
    """Get recommendations for a patient"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.patient_id == patient_id
    ).order_by(Recommendation.created_at.desc()).all()
    
    return recommendations

@router.get("/patient/{patient_id}/insights")
def get_health_insights(patient_id: int, db: Session = Depends(get_db)):
    """Get AI-generated health insights for a patient"""
    
    health_records = HealthDataService.get_patient_health_records(db, patient_id, days=30)
    
    if not health_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No health records found for this patient"
        )
    
    # Prepare data for AI
    health_data = {
        "latest": {
            "blood_pressure": f"{health_records[0].blood_pressure_systolic}/{health_records[0].blood_pressure_diastolic}",
            "heart_rate": health_records[0].heart_rate,
            "temperature": health_records[0].temperature,
        }
    }
    
    records_data = [{
        "recorded_date": str(r.recorded_date),
        "blood_pressure_systolic": r.blood_pressure_systolic,
        "blood_pressure_diastolic": r.blood_pressure_diastolic,
        "heart_rate": r.heart_rate,
    } for r in health_records[:5]]
    
    # Generate insights using AI
    insights = AIService.generate_health_insights(health_data, records_data)
    
    return {
        "patient_id": patient_id,
        "insights": insights,
        "generated_at": str(__import__('datetime').datetime.utcnow())
    }
