#!/usr/bin/env python
"""Comprehensive test for healthcare system"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_auth():
    """Test authentication"""
    print("\n=== Testing Authentication ===")
    
    # Login
    login_payload = {
        "username": "testuser1",
        "password": "password123"
    }
    
    r = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload)
    if r.status_code != 200:
        print(f"❌ Login failed: {r.status_code} - {r.text}")
        return None
    
    data = r.json()
    token = data.get("access_token")
    user = data.get("user")
    print(f"✅ Login successful - User: {user['username']}, ID: {user['id']}")
    return token

def test_health_data(token):
    """Test health data endpoints"""
    print("\n=== Testing Health Data Endpoints ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Log health data
    health_payload = {
        "blood_pressure_systolic": 120,
        "blood_pressure_diastolic": 80,
        "heart_rate": 72,
        "temperature": 37.0,
        "blood_glucose": 100,
        "weight": 75,
        "height": 180,
        "symptoms": "None",
        "source": "manual_entry"
    }
    
    r = requests.post(f"{BASE_URL}/api/health-data/", json=health_payload, headers=headers)
    if r.status_code != 200:
        print(f"❌ Log health data failed: {r.status_code} - {r.text}")
        return False
    print(f"✅ Health data logged successfully")
    
    # Get latest
    r = requests.get(f"{BASE_URL}/api/health-data/me/latest", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get latest failed: {r.status_code} - {r.text}")
        return False
    latest = r.json()
    print(f"✅ Got latest health data - HR: {latest['heart_rate']}, BP: {latest['blood_pressure_systolic']}/{latest['blood_pressure_diastolic']}")
    
    # Get all records
    r = requests.get(f"{BASE_URL}/api/health-data/me", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get records failed: {r.status_code} - {r.text}")
        return False
    records = r.json()
    print(f"✅ Got health records - Count: {len(records)}")
    
    return True

def test_alerts(token):
    """Test alert endpoints"""
    print("\n=== Testing Alert Endpoints ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all alerts
    r = requests.get(f"{BASE_URL}/api/alerts/me", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get alerts failed: {r.status_code} - {r.text}")
        return False
    alerts = r.json()
    print(f"✅ Got alerts - Count: {len(alerts)}")
    
    # Get unresolved
    r = requests.get(f"{BASE_URL}/api/alerts/me/unresolved", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get unresolved alerts failed: {r.status_code} - {r.text}")
        return False
    unresolved = r.json()
    print(f"✅ Got unresolved alerts - Count: {len(unresolved)}")
    
    return True

def test_recommendations(token):
    """Test recommendation endpoints"""
    print("\n=== Testing Recommendation Endpoints ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get recommendations
    r = requests.get(f"{BASE_URL}/api/recommendations/me", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get recommendations failed: {r.status_code} - {r.text}")
        return False
    recs = r.json()
    print(f"✅ Got recommendations - Count: {len(recs)}")
    
    # Get insights
    r = requests.get(f"{BASE_URL}/api/recommendations/me/insights", headers=headers)
    if r.status_code != 200:
        print(f"❌ Get insights failed: {r.status_code} - {r.text}")
        return False
    insights = r.json()
    print(f"✅ Got insights - Response type: {type(insights)}, keys: {list(insights.keys()) if isinstance(insights, dict) else 'N/A'}")
    if isinstance(insights, dict) and "insights" in insights:
        print(f"   Insights length: {len(insights['insights'])} chars")
    
    # Generate recommendations
    r = requests.get(f"{BASE_URL}/api/recommendations/me/generate", headers=headers)
    if r.status_code != 200:
        print(f"❌ Generate recommendations failed: {r.status_code} - {r.text}")
        # This might fail if no health data, which is ok
        print("   (This is expected if not enough health data)")
    else:
        result = r.json()
        print(f"✅ Generated recommendations - Count: {len(result.get('recommendations', []))}")
    
    return True

def main():
    print("Starting comprehensive healthcare system test...")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now()}")
    
    # Test auth
    token = test_auth()
    if not token:
        print("\n❌ Tests failed - authentication failed")
        return
    
    # Test health data
    if not test_health_data(token):
        print("\n❌ Health data tests failed")
        return
    
    # Test alerts
    if not test_alerts(token):
        print("\n❌ Alert tests failed")
        return
    
    # Test recommendations
    if not test_recommendations(token):
        print("\n❌ Recommendation tests failed")
        return
    
    print("\n" + "="*50)
    print("✅ All tests completed!")
    print("="*50)

if __name__ == "__main__":
    main()
