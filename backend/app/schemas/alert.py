from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertResponse(BaseModel):
    id: int
    patient_id: int
    alert_type: str
    severity: str
    title: str
    message: str
    triggered_by: str
    is_resolved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
