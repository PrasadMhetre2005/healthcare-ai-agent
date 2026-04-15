from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai_service import AIService
from app.services.patient_service import PatientService
from app.utils.database import get_db
from app.utils.security import get_current_patient
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/healthcare-consultant", response_model=ChatResponse)
def healthcare_consultant_chat(
    chat_input: ChatMessage,
    user_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """
    AI-powered healthcare consultant chat endpoint
    
    Provides personalized health advice based on user query and their health data
    """
    
    try:
        patient = PatientService.get_patient_by_user_id(db, user_id)
        
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient profile not found"
            )
        
        # Get user's recent health data context
        from app.services.health_data_service import HealthDataService
        health_records = HealthDataService.get_patient_health_records(db, patient.id, days=7)
        
        # Prepare context
        context = "Healthcare Consultant Mode\n\n"
        
        if health_records:
            latest = health_records[0]
            context += f"""
Latest Health Data:
- Blood Pressure: {latest.blood_pressure_systolic}/{latest.blood_pressure_diastolic} mmHg
- Heart Rate: {latest.heart_rate} bpm
- Temperature: {latest.temperature}°C
- Blood Glucose: {latest.blood_glucose} mg/dL
- Weight: {latest.weight} kg
"""
        
        context += f"""
Patient Info: {patient.first_name} {patient.last_name}
Blood Type: {patient.blood_type or 'Not specified'}
Allergies: {patient.allergies or 'None reported'}

User Query: {chat_input.message}

Provide helpful, personalized health advice considering the patient's data. Be empathetic and encourage them to consult their doctor for serious concerns.
"""
        
        # Generate response using Groq/Llama AI
        response_text = AIService.generate_chat_response(context)
        
        logger.info(f"Healthcare consultant chat - User: {user_id}, Query length: {len(chat_input.message)}")
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )
