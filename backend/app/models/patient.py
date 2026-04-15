from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.utils.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    gender = Column(String)  # M, F, Other
    blood_type = Column(String)
    allergies = Column(Text)  # JSON or comma-separated
    medical_history = Column(Text)  # JSON or comma-separated
    current_medications = Column(Text)  # JSON
    emergency_contact = Column(String)
    emergency_phone = Column(String)
    assigned_doctor_id = Column(Integer, ForeignKey("doctors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
