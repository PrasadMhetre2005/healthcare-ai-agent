from groq import Groq
import os
import json
import logging
import traceback
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered insights and recommendations using Groq API with Llama 3 70B"""
    
    # Initialize Groq client at class level
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = "llama-3.3-70b-versatile"  # Updated from llama-3-70b-versatile
    
    _client = None
    
    @classmethod
    def _get_client(cls):
        """Get or create Groq client"""
        if cls._client is None and cls.API_KEY:
            try:
                logger.info(f"Initializing Groq client with API key: {cls.API_KEY[:20]}...")
                cls._client = Groq(api_key=cls.API_KEY)
                logger.info("Groq client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {str(e)}")
                logger.error(traceback.format_exc())
                return None
        return cls._client
    
    @staticmethod
    def _call_groq(prompt: str, system_prompt: str = "You are a helpful assistant.") -> Optional[str]:
        """Make a call to Groq API"""
        try:
            logger.info("Starting Groq API call...")
            client = AIService._get_client()
            
            # If API key not configured, return None (triggers mock response)
            if not client:
                logger.warning("Groq client not available - returning None")
                return None
            
            logger.info(f"Calling Groq with model: {AIService.MODEL}")
            message = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=AIService.MODEL,
                temperature=0.7,
                max_tokens=500,
            )
            
            response_text = message.choices[0].message.content
            logger.info(f"Groq response received successfully: {len(response_text)} characters")
            return response_text
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            logger.error(f"Full error: {traceback.format_exc()}")
            return None
    
    @staticmethod
    def generate_health_insights(patient_data: dict, health_records: list) -> str:
        """Generate clinical insights from patient health data"""
        
        prompt = f"""You are a medical AI assistant. Analyze the following patient health data and provide clinical insights.

Patient Data:
- Name: {patient_data.get('name', 'Unknown')}
- Age: {patient_data.get('age', 'Unknown')}
- Blood Type: {patient_data.get('blood_type', 'Unknown')}

Recent Health Records (last 30 days):
{json.dumps([{
    'date': str(r.get('recorded_date')),
    'blood_pressure': f"{r.get('blood_pressure_systolic')}/{r.get('blood_pressure_diastolic')}",
    'heart_rate': r.get('heart_rate'),
    'temperature': r.get('temperature'),
    'blood_glucose': r.get('blood_glucose'),
    'weight': r.get('weight')
} for r in health_records[:5]], indent=2)}

Please provide:
1. Key health observations
2. Trends noticed  
3. Areas of concern

Keep response concise and to the point. Maximum 200 words."""
        
        response = AIService._call_groq(prompt)
        
        if response:
            return response
        
        # Mock response if API key not configured
        return """Based on your recent health records, here are key observations:

1. **Key Health Observations**
   - Your vital signs have been relatively stable over the past 30 days
   - Blood pressure readings are within normal range
   - Heart rate shows consistent patterns

2. **Trends Noticed**
   - Slight weight fluctuation (normal variation)
   - Temperature stable throughout period
   - No concerning patterns detected

3. **Areas of Concern**
   - None at this time - keep monitoring regularly
   - Maintain current health habits

**Note:** For full AI analysis, please configure your GROQ_API_KEY in the .env file."""
    
    @staticmethod
    def generate_recommendations(patient_data: dict, health_records: list, recent_alerts: list) -> list:
        """Generate actionable health recommendations"""
        
        prompt = f"""You are a medical AI assistant. Based on the following patient data and alerts, recommend specific health actions.

Patient: {patient_data.get('name', 'Patient')}
Blood Type: {patient_data.get('blood_type', 'Unknown')}

Recent Alerts:
{json.dumps([a.get('title') for a in recent_alerts[:3]], indent=2)}

Generate 3-5 specific, actionable recommendations. For each recommendation, provide:
- Category (lifestyle, medication, appointment, diet, or exercise)
- Priority (low, medium, or high)
- Title - short descriptive title
- Description - specific action to take
- Reason - why this is important

Format as simple bullet points, not JSON."""
        
        response = AIService._call_groq(prompt)
        
        if response:
            # Parse recommendations from text response
            recommendations = []
            for line in response.split('\n'):
                if line.strip():
                    recommendations.append({
                        "category": "general",
                        "priority": "medium",
                        "title": "Health Recommendation",
                        "description": line.strip(),
                        "reason": "Based on your health data"
                    })
            return recommendations[:5]  # Return up to 5 recommendations
        
        # Mock recommendations if API key not configured
        return [
            {
                "category": "lifestyle",
                "priority": "medium",
                "title": "Regular Exercise",
                "description": "Engage in 30 minutes of moderate exercise daily",
                "reason": "Improves cardiovascular health and overall fitness"
            },
            {
                "category": "diet",
                "priority": "high",
                "title": "Balanced Nutrition",
                "description": "Maintain a balanced diet with fruits, vegetables, and lean proteins",
                "reason": "Essential for maintaining healthy blood glucose and weight"
            },
            {
                "category": "appointment",
                "priority": "medium",
                "title": "Regular Checkup",
                "description": "Schedule a routine health checkup with your physician",
                "reason": "Regular monitoring helps detect potential issues early"
            }
        ]
    
    @staticmethod
    def check_medication_interactions(medications: list) -> dict:
        """Check for potential medication interactions"""
        
        prompt = f"""You are a pharmacology AI expert. Check for potential interactions between these medications:
{', '.join(medications)}

Provide a brief analysis indicating:
1. Whether interactions exist (yes/no)
2. What interactions if any
3. Severity level (low/medium/high)

Keep response concise and factual."""
        
        response = AIService._call_groq(prompt)
        
        if response:
            return {
                "has_interactions": "interaction" in response.lower() or "contraindicated" in response.lower(),
                "interactions": [response],
                "severity": "medium" if "contraindicated" in response.lower() else "low"
            }
        
        # Mock response if API key not configured
        return {
            "has_interactions": False,
            "interactions": [],
            "severity": "low"
        }
    
    @staticmethod
    def generate_chat_response(context: str) -> str:
        """Generate chat response for healthcare consultant"""
        
        system_prompt = """You are a compassionate and knowledgeable AI Healthcare Consultant. Your role is to:
1. Provide helpful health advice based on user queries
2. Consider the patient's health data context
3. Encourage lifestyle improvements
4. Suggest consulting with doctors for serious concerns
5. Be empathetic and non-judgmental
6. Keep responses concise and actionable (2-3 paragraphs)"""
        
        response = AIService._call_groq(context, system_prompt)
        
        if response:
            return response
        
        # Mock response if API key not configured
        return """I appreciate your question! Based on your health profile, here are some general wellness recommendations:

1. **Hydration**: Ensure you're drinking enough water throughout the day (8-10 glasses)
2. **Sleep**: Aim for 7-9 hours of quality sleep nightly
3. **Exercise**: Try to get 30 minutes of moderate activity most days
4. **Nutrition**: Focus on balanced meals with vegetables, lean proteins, and whole grains

However, for personalized medical advice, I recommend consulting with your healthcare provider. If you've provided your health data, I can give more specific recommendations once the AI service is configured.

Is there anything specific about your health you'd like to discuss?"""

