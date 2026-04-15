from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.utils.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    category = Column(String)  # lifestyle, medication, appointment, diet, exercise, etc.
    priority = Column(String)  # low, medium, high
    title = Column(String)
    description = Column(Text)
    reason = Column(Text)  # Why this recommendation was made
    generated_by = Column(String)  # AI, Doctor, System
    is_acknowledged = Column(String, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
