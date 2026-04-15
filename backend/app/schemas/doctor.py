from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    medical_license: str
    specialization: str
    hospital_name: Optional[str]
    phone: Optional[str]
    patients_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
