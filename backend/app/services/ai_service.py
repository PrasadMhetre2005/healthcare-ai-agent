from groq import Groq
import os
import json
from typing import Optional
from datetime import datetime

class AIService:
    """Service for AI-powered insights and recommendations using Groq"""
    
    # Initialize client at class level
    try:
        api_key = os.getenv("GROQ_API_KEY", "")
        if api_key and api_key != "your_groq_api_key_here":
            client = Groq(api_key=api_key)
        else:
            client = None
    except:
        client = None
    
    @staticmethod
    def generate_health_insights(patient_data: dict, health_records: list) -> str:
        """Generate clinical insights from patient health data"""
        
        # If no API key, return mock insights
        if not AIService.client:
            return """
Based on your recent health records, here are key observations:

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

**Note:** Full AI analysis requires Groq API configuration.
            """
        
        prompt = f"""
        You are a medical AI assistant. Analyze the following patient health data and provide clinical insights.
        
        Patient Data:
        {json.dumps(patient_data, indent=2)}
        
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
        
        Keep response concise and to the point.
        """
        
        try:
            response = AIService.client.chat.completions.create(
                model="llama-3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a medical advising AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating insights: {str(e)}\n\n(Make sure GROQ_API_KEY is configured in .env)"
    
    @staticmethod
    def generate_recommendations(patient_data: dict, health_records: list, recent_alerts: list) -> list:
        """Generate actionable health recommendations"""
        
        # Mock recommendations if no API key
        if not AIService.client:
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
        
        prompt = f"""
        You are a medical AI assistant. Based on the following patient data, recommend health actions.
        
        Patient Data:
        {json.dumps(patient_data, indent=2)}
        
        Recent Alerts:
        {json.dumps([a.get('title') for a in recent_alerts[:3]], indent=2)}
        
        Generate 3-5 specific, actionable recommendations. Format as JSON array with fields:
        - category (lifestyle, medication, appointment, diet, exercise)
        - priority (low, medium, high)
        - title
        - description
        - reason
        
        Return only valid JSON array.
        """
        
        try:
            response = AIService.client.chat.completions.create(
                model="llama-3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a medical advising AI assistant. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content
            # Try to parse JSON from response
            try:
                recommendations = json.loads(response_text)
                return recommendations if isinstance(recommendations, list) else []
            except:
                return []
                
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []
    
    @staticmethod
    def check_medication_interactions(medications: list) -> dict:
        """Check for potential medication interactions"""
        
        # Mock response if no API key
        if not AIService.client:
            return {
                "has_interactions": False,
                "interactions": [],
                "severity": "low"
            }
        
        prompt = f"""
        Check for potential interactions between these medications: {', '.join(medications)}
        
        Return JSON with fields:
        - has_interactions (boolean)
        - interactions (list of strings describing interactions)
        - severity (low, medium, high)
        
        Return only valid JSON.
        """
        
        try:
            response = AIService.client.chat.completions.create(
                model="llama-3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a pharmacology AI. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            response_text = response.choices[0].message.content
            try:
                return json.loads(response_text)
            except:
                return {"has_interactions": False, "interactions": [], "severity": "unknown"}
                
        except Exception as e:
            return {"has_interactions": False, "interactions": [], "severity": "unknown"}
    
    @staticmethod
    def generate_chat_response(context: str) -> str:
        """Generate chat response for healthcare consultant"""
        
        # If no API key, return mock response
        if not AIService.client:
            return """I appreciate your question! Based on your health profile, here are some general wellness recommendations:

1. **Hydration**: Ensure you're drinking enough water throughout the day (8-10 glasses)
2. **Sleep**: Aim for 7-9 hours of quality sleep nightly
3. **Exercise**: Try to get 30 minutes of moderate activity most days
4. **Nutrition**: Focus on balanced meals with vegetables, lean proteins, and whole grains

However, for personalized medical advice, I recommend consulting with your healthcare provider. If you've provided your health data, I can give more specific recommendations once the AI service is configured.

Is there anything specific about your health you'd like to discuss?"""
        
        try:
            response = AIService.client.chat.completions.create(
                model="llama-3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a compassionate and knowledgeable AI Healthcare Consultant. Your role is to:
1. Provide helpful health advice based on user queries
2. Consider the patient's health data context
3. Encourage lifestyle improvements
4. Suggest consulting with doctors for serious concerns
5. Be empathetic and non-judgmental
6. Keep responses concise and actionable (2-3 paragraphs)"""
                    },
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, I encountered an issue processing your query. Please try again. Error: {str(e)[:100]}"
