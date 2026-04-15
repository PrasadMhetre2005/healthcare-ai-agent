from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.services.auth_service import AuthService
import os

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    """Dependency for protected routes"""
    token = credentials.credentials
    payload = AuthService.decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    return user_id

async def get_current_doctor(user_id: int = Depends(get_current_user)):
    """Dependency for doctor-only routes"""
    # In a real app, you'd check the database to verify the user is a doctor
    return user_id

async def get_current_patient(user_id: int = Depends(get_current_user)):
    """Dependency for patient-only routes"""
    # In a real app, you'd check the database to verify the user is a patient
    return user_id
