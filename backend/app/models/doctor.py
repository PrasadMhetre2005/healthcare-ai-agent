from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from datetime import datetime
from app.utils.database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    phone_verified = Column(Boolean, default=False)
    medical_license = Column(String, unique=True, index=True)
    license_file_path = Column(String)  # Store uploaded license path
    license_verified = Column(Boolean, default=False)
    years_of_experience = Column(Integer, default=0)
    specialization = Column(String)  # Cardiology, Neurology, etc.
    hospital_name = Column(String)
    office_address = Column(Text)
    bio = Column(Text)
    patients_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
