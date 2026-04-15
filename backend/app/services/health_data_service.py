from sqlalchemy.orm import Session
from app.models.health_data import HealthData
from app.schemas.health_data import HealthDataCreate
from datetime import datetime, timedelta
import json

class HealthDataService:
    
    @staticmethod
    def create_health_record(db: Session, patient_id: int, health_data: HealthDataCreate) -> HealthData:
        # Calculate BMI if weight and height are provided
        bmi = None
        if health_data.weight and health_data.height:
            bmi = health_data.weight / ((health_data.height / 100) ** 2)
        
        db_health_data = HealthData(
            patient_id=patient_id,
            blood_pressure_systolic=health_data.blood_pressure_systolic,
            blood_pressure_diastolic=health_data.blood_pressure_diastolic,
            heart_rate=health_data.heart_rate,
            temperature=health_data.temperature,
            respiratory_rate=health_data.respiratory_rate,
            blood_glucose=health_data.blood_glucose,
            weight=health_data.weight,
            height=health_data.height,
            bmi=bmi,
            lab_results=health_data.lab_results,
            doctor_notes=health_data.doctor_notes,
            symptoms=health_data.symptoms,
            medications_taken=health_data.medications_taken,
            source=health_data.source
        )
        db.add(db_health_data)
        db.commit()
        db.refresh(db_health_data)
        return db_health_data
    
    @staticmethod
    def get_patient_health_records(db: Session, patient_id: int, days: int = 30):
        start_date = datetime.utcnow() - timedelta(days=days)
        return db.query(HealthData).filter(
            HealthData.patient_id == patient_id,
            HealthData.created_at >= start_date
        ).order_by(HealthData.created_at.desc()).all()
    
    @staticmethod
    def get_latest_health_record(db: Session, patient_id: int) -> HealthData:
        return db.query(HealthData).filter(
            HealthData.patient_id == patient_id
        ).order_by(HealthData.created_at.desc()).first()
    
    @staticmethod
    def get_health_trends(db: Session, patient_id: int, days: int = 30):
        """Get health data trends for the past N days"""
        records = HealthDataService.get_patient_health_records(db, patient_id, days)
        
        trends = {
            "blood_pressure": [],
            "heart_rate": [],
            "temperature": [],
            "blood_glucose": [],
            "weight": []
        }
        
        for record in reversed(records):
            if record.blood_pressure_systolic:
                trends["blood_pressure"].append({
                    "date": record.recorded_date,
                    "systolic": record.blood_pressure_systolic,
                    "diastolic": record.blood_pressure_diastolic
                })
            if record.heart_rate:
                trends["heart_rate"].append({
                    "date": record.recorded_date,
                    "value": record.heart_rate
                })
            if record.temperature:
                trends["temperature"].append({
                    "date": record.recorded_date,
                    "value": record.temperature
                })
            if record.blood_glucose:
                trends["blood_glucose"].append({
                    "date": record.recorded_date,
                    "value": record.blood_glucose
                })
            if record.weight:
                trends["weight"].append({
                    "date": record.recorded_date,
                    "value": record.weight
                })
        
        return trends
