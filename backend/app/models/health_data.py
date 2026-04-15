from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from datetime import datetime
from app.utils.database import Base

class HealthData(Base):
    __tablename__ = "health_data"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Vital Signs
    blood_pressure_systolic = Column(Float, nullable=True)
    blood_pressure_diastolic = Column(Float, nullable=True)
    heart_rate = Column(Float, nullable=True)  # bpm
    temperature = Column(Float, nullable=True)  # Celsius
    respiratory_rate = Column(Float, nullable=True)  # breaths/min
    blood_glucose = Column(Float, nullable=True)  # mg/dL
    weight = Column(Float, nullable=True)  # kg
    height = Column(Float, nullable=True)  # cm
    bmi = Column(Float, nullable=True)
    
    # Lab Results
    lab_results = Column(Text)  # JSON: {test_name: value, ...}
    
    # Doctor Notes
    doctor_notes = Column(Text)
    symptoms = Column(Text)  # JSON: [symptom1, symptom2, ...]
    
    # Medication Log
    medications_taken = Column(Text)  # JSON: {med_name: dose_taken, ...}
    
    # Source
    source = Column(String)  # manual_entry, wearable, lab_report, doctor_input
    
    recorded_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
