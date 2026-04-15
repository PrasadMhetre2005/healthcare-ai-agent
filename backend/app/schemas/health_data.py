from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthDataCreate(BaseModel):
    blood_pressure_systolic: Optional[float] = None
    blood_pressure_diastolic: Optional[float] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[float] = None
    blood_glucose: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    lab_results: Optional[str] = None  # JSON string
    doctor_notes: Optional[str] = None
    symptoms: Optional[str] = None  # JSON string
    medications_taken: Optional[str] = None  # JSON string
    source: str = "manual_entry"

class HealthDataResponse(BaseModel):
    id: int
    patient_id: int
    blood_pressure_systolic: Optional[float]
    blood_pressure_diastolic: Optional[float]
    heart_rate: Optional[float]
    temperature: Optional[float]
    blood_glucose: Optional[float]
    weight: Optional[float]
    bmi: Optional[float]
    lab_results: Optional[str]
    doctor_notes: Optional[str]
    source: str
    recorded_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
