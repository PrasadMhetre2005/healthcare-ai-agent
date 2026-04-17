from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from datetime import datetime
from app.utils.database import Base
import enum

class CareGapType(str, enum.Enum):
    NO_TEST = "no_test"  # No test done
    MISSED_FOLLOWUP = "missed_followup"  # Missed follow-up
    MEDICATION_NOT_TAKEN = "medication_not_taken"  # Medication not taken
    OVERDUE_CHECKUP = "overdue_checkup"  # Checkup overdue
    MISSING_VITALS = "missing_vitals"  # Missing vital signs

class CareGap(Base):
    __tablename__ = "care_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), index=True)
    gap_type = Column(Enum(CareGapType))
    description = Column(Text)
    severity = Column(String)  # "low", "medium", "high"
    days_since_gap = Column(Integer)  # How many days since this gap occurred
    resolved = Column(String, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
