from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class DoctorRegister(BaseModel):
    """Doctor registration schema"""
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    medical_license: str
    years_of_experience: Optional[int] = 0
    specialization: str
    hospital_name: Optional[str] = None
    office_address: Optional[str] = None
    bio: Optional[str] = None
    # license file is handled via multipart form data

class DoctorLogin(BaseModel):
    """Doctor login schema - can use email, phone, or username+password"""
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    medical_license: str
    specialization: str
    hospital_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

class DoctorResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    medical_license: str
    specialization: str
    license_verified: bool
    hospital_name: Optional[str]
    bio: Optional[str]
    years_of_experience: int
    patients_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DoctorDashboardStats(BaseModel):
    """Doctor dashboard overview stats"""
    total_patients: int
    critical_alerts: int
    pending_appointments: int
    care_gaps_count: int

class DoctorPatientListItem(BaseModel):
    """Patient item in doctor's patient list"""
    id: int
    first_name: str
    last_name: str
    age: int
    condition: Optional[str]
    last_visit: Optional[datetime]
    status: str  # "Normal", "Critical"
