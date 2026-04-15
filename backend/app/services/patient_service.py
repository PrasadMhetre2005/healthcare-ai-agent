from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientService:
    
    @staticmethod
    def create_patient(db: Session, patient: PatientCreate, user_id: int) -> Patient:
        db_patient = Patient(
            user_id=user_id,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender,
            blood_type=patient.blood_type,
            allergies=patient.allergies,
            medical_history=patient.medical_history,
            emergency_contact=patient.emergency_contact,
            emergency_phone=patient.emergency_phone
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    
    @staticmethod
    def get_patient_by_id(db: Session, patient_id: int) -> Patient:
        return db.query(Patient).filter(Patient.id == patient_id).first()
    
    @staticmethod
    def get_patient_by_user_id(db: Session, user_id: int) -> Patient:
        return db.query(Patient).filter(Patient.user_id == user_id).first()
    
    @staticmethod
    def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate) -> Patient:
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if db_patient:
            update_data = patient_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_patient, field, value)
            db.commit()
            db.refresh(db_patient)
        return db_patient
    
    @staticmethod
    def get_all_patients(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Patient).offset(skip).limit(limit).all()
