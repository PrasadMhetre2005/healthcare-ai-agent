from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecommendationResponse(BaseModel):
    id: int
    patient_id: int
    category: str
    priority: str
    title: str
    description: str
    reason: str
    generated_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True
