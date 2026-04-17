from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.models.user import User
from app.models.appointment import Appointment
from app.models.care_gap import CareGap
from app.models.patient import Patient
from app.models.health_data import HealthData
from app.models.alert import Alert
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DoctorService:
    
    @staticmethod
    def get_doctor_by_user_id(db: Session, user_id: int) -> Doctor:
        """Get doctor profile by user ID"""
        return db.query(Doctor).filter(Doctor.user_id == user_id).first()
    
    @staticmethod
    def get_doctor_by_email(db: Session, email: str) -> Doctor:
        """Get doctor by email"""
        return db.query(Doctor).filter(Doctor.email == email).first()
    
    @staticmethod
    def get_doctor_by_phone(db: Session, phone: str) -> Doctor:
        """Get doctor by phone"""
        return db.query(Doctor).filter(Doctor.phone == phone).first()
    
    @staticmethod
    def get_dashboard_stats(db: Session, doctor_id: int) -> dict:
        """Get dashboard overview stats for doctor"""
        # Get patients assigned to this doctor
        patients = db.query(Patient).filter(Patient.assigned_doctor_id == doctor_id).all()
        total_patients = len(patients)
        patient_ids = [p.id for p in patients]
        
        # Get critical alerts
        critical_alerts = db.query(Alert).filter(
            Alert.patient_id.in_(patient_ids) if patient_ids else False,
            Alert.severity == "critical"
        ).count()
        
        # Get pending appointments
        pending_appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
            Appointment.appointment_date > datetime.utcnow()
        ).count()
        
        # Get care gaps
        care_gaps = db.query(CareGap).filter(
            CareGap.doctor_id == doctor_id,
            CareGap.resolved == False
        ).count()
        
        return {
            "total_patients": total_patients,
            "critical_alerts": critical_alerts,
            "pending_appointments": pending_appointments,
            "care_gaps": care_gaps
        }
    
    @staticmethod
    def get_doctor_patients(db: Session, doctor_id: int, limit: int = 50, offset: int = 0):
        """Get list of patients for a doctor"""
        patients = db.query(Patient).filter(
            Patient.assigned_doctor_id == doctor_id
        ).offset(offset).limit(limit).all()
        
        result = []
        for patient in patients:
            # Calculate age
            if patient.date_of_birth:
                try:
                    dob = datetime.strptime(patient.date_of_birth, "%Y-%m-%d")
                    age = (datetime.utcnow() - dob).days // 365
                except:
                    age = 0
            else:
                age = 0
            
            # Get last visit
            last_health_data = db.query(HealthData).filter(
                HealthData.patient_id == patient.id
            ).order_by(HealthData.recorded_date.desc()).first()
            
            last_visit = last_health_data.recorded_date if last_health_data else None
            
            # Check for critical alerts
            critical_alert = db.query(Alert).filter(
                Alert.patient_id == patient.id,
                Alert.severity == "critical"
            ).first()
            
            status = "Critical" if critical_alert else "Normal"
            
            result.append({
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "age": age,
                "condition": patient.medical_history or "Not specified",
                "last_visit": last_visit,
                "status": status
            })
        
        return result
    
    @staticmethod
    def get_doctor_alerts(db: Session, doctor_id: int, limit: int = 20):
        """Get alerts for doctor's patients"""
        patients = db.query(Patient).filter(Patient.assigned_doctor_id == doctor_id).all()
        patient_ids = [p.id for p in patients]
        
        if not patient_ids:
            return []
        
        alerts = db.query(Alert).filter(
            Alert.patient_id.in_(patient_ids)
        ).order_by(Alert.created_at.desc()).limit(limit).all()
        
        result = []
        for alert in alerts:
            patient = db.query(Patient).filter(Patient.id == alert.patient_id).first()
            result.append({
                "id": alert.id,
                "patient_name": f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
                "message": alert.message,
                "severity": alert.severity,  # "critical", "warning", "info"
                "created_at": alert.created_at
            })
        
        return result
    
    @staticmethod
    def get_care_gaps(db: Session, doctor_id: int, limit: int = 20):
        """Get care gaps for doctor's patients"""
        care_gaps = db.query(CareGap).filter(
            CareGap.doctor_id == doctor_id,
            CareGap.resolved == False
        ).order_by(CareGap.created_at.desc()).limit(limit).all()
        
        result = []
        for gap in care_gaps:
            patient = db.query(Patient).filter(Patient.id == gap.patient_id).first()
            result.append({
                "id": gap.id,
                "patient_name": f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
                "gap_type": gap.gap_type,
                "description": gap.description,
                "severity": gap.severity,
                "days_since": gap.days_since_gap,
                "created_at": gap.created_at
            })
        
        return result
    
    @staticmethod
    def get_upcoming_appointments(db: Session, doctor_id: int, limit: int = 10):
        """Get upcoming appointments for doctor"""
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "scheduled",
            Appointment.appointment_date > datetime.utcnow()
        ).order_by(Appointment.appointment_date.asc()).limit(limit).all()
        
        result = []
        for apt in appointments:
            patient = db.query(Patient).filter(Patient.id == apt.patient_id).first()
            result.append({
                "id": apt.id,
                "patient_name": f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
                "appointment_date": apt.appointment_date,
                "notes": apt.notes
            })
        
        return result
    
    @staticmethod
    def get_patient_profile(db: Session, doctor_id: int, patient_id: int):
        """Get full patient profile for a doctor"""
        # Verify this patient is assigned to this doctor
        patient = db.query(Patient).filter(
            Patient.id == patient_id,
            Patient.assigned_doctor_id == doctor_id
        ).first()
        
        if not patient:
            return None
        
        # Get health data
        health_records = db.query(HealthData).filter(
            HealthData.patient_id == patient_id
        ).order_by(HealthData.recorded_date.desc()).limit(30).all()
        
        # Get alerts
        alerts = db.query(Alert).filter(
            Alert.patient_id == patient_id
        ).order_by(Alert.created_at.desc()).limit(10).all()
        
        return {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth,
            "gender": patient.gender,
            "blood_type": patient.blood_type,
            "allergies": patient.allergies,
            "medical_history": patient.medical_history,
            "current_medications": patient.current_medications,
            "emergency_contact": patient.emergency_contact,
            "emergency_phone": patient.emergency_phone,
            "health_records": [
                {
                    "date": h.recorded_date,
                    "blood_pressure": f"{h.blood_pressure_systolic}/{h.blood_pressure_diastolic}",
                    "heart_rate": h.heart_rate,
                    "temperature": h.temperature,
                    "blood_glucose": h.blood_glucose,
                    "weight": h.weight
                } for h in health_records
            ],
            "alerts": [
                {
                    "id": a.id,
                    "message": a.message,
                    "severity": a.severity,
                    "created_at": a.created_at
                } for a in alerts
            ]
        }
