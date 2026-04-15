from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.health_data import HealthData
from datetime import datetime

class AlertService:
    
    # Define alert thresholds
    ALERT_THRESHOLDS = {
        "blood_pressure_high": {"systolic": 140, "diastolic": 90},
        "blood_pressure_low": {"systolic": 90, "diastolic": 60},
        "heart_rate_high": 100,
        "heart_rate_low": 60,
        "temperature_high": 38,
        "temperature_low": 36,
        "blood_glucose_high": 200,
        "blood_glucose_low": 70,
    }
    
    @staticmethod
    def create_alert(db: Session, patient_id: int, alert_type: str, severity: str, 
                    title: str, message: str, triggered_by: str) -> Alert:
        alert = Alert(
            patient_id=patient_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            triggered_by=triggered_by
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    
    @staticmethod
    def check_health_anomalies(db: Session, patient_id: int, health_data: HealthData) -> list:
        """Check for anomalies in health data and create alerts"""
        alerts_created = []
        
        # Check blood pressure
        if health_data.blood_pressure_systolic and health_data.blood_pressure_diastolic:
            if health_data.blood_pressure_systolic >= AlertService.ALERT_THRESHOLDS["blood_pressure_high"]["systolic"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="high",
                    title="High Blood Pressure Detected",
                    message=f"Your blood pressure is {health_data.blood_pressure_systolic}/{health_data.blood_pressure_diastolic} mmHg",
                    triggered_by="blood_pressure"
                )
                alerts_created.append(alert)
            elif health_data.blood_pressure_systolic <= AlertService.ALERT_THRESHOLDS["blood_pressure_low"]["systolic"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="medium",
                    title="Low Blood Pressure Detected",
                    message=f"Your blood pressure is {health_data.blood_pressure_systolic}/{health_data.blood_pressure_diastolic} mmHg",
                    triggered_by="blood_pressure"
                )
                alerts_created.append(alert)
        
        # Check heart rate
        if health_data.heart_rate:
            if health_data.heart_rate >= AlertService.ALERT_THRESHOLDS["heart_rate_high"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="medium",
                    title="Elevated Heart Rate",
                    message=f"Your heart rate is {health_data.heart_rate} bpm",
                    triggered_by="heart_rate"
                )
                alerts_created.append(alert)
        
        # Check body temperature
        if health_data.temperature:
            if health_data.temperature >= AlertService.ALERT_THRESHOLDS["temperature_high"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="high",
                    title="Fever Detected",
                    message=f"Your body temperature is {health_data.temperature}°C",
                    triggered_by="temperature"
                )
                alerts_created.append(alert)
        
        # Check blood glucose
        if health_data.blood_glucose:
            if health_data.blood_glucose >= AlertService.ALERT_THRESHOLDS["blood_glucose_high"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="high",
                    title="High Blood Sugar",
                    message=f"Your blood glucose level is {health_data.blood_glucose} mg/dL",
                    triggered_by="blood_glucose"
                )
                alerts_created.append(alert)
            elif health_data.blood_glucose <= AlertService.ALERT_THRESHOLDS["blood_glucose_low"]:
                alert = AlertService.create_alert(
                    db, patient_id,
                    alert_type="abnormal_reading",
                    severity="critical",
                    title="Low Blood Sugar",
                    message=f"Your blood glucose level is {health_data.blood_glucose} mg/dL. Seek immediate help.",
                    triggered_by="blood_glucose"
                )
                alerts_created.append(alert)
        
        return alerts_created
    
    @staticmethod
    def get_patient_alerts(db: Session, patient_id: int, unresolved_only: bool = False):
        query = db.query(Alert).filter(Alert.patient_id == patient_id)
        if unresolved_only:
            query = query.filter(Alert.is_resolved == False)
        return query.order_by(Alert.created_at.desc()).all()
    
    @staticmethod
    def mark_alert_resolved(db: Session, alert_id: int) -> Alert:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            db.commit()
            db.refresh(alert)
        return alert
