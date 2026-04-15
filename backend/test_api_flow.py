#!/usr/bin/env python
"""Test complete authentication flow"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=== Testing Healthcare AI Backend ===\n")

# Test 1: Root endpoint
print("1. Testing root endpoint...")
try:
    resp = requests.get(f"{BASE_URL}/")
    print(f"   ✓ Status: {resp.status_code}")
    print(f"   ✓ Response: {resp.json()['message']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 2: Register new user
print("2. Testing user registration...")
test_user = {
    "username": f"testuser_{int(time.time())}",
    "email": f"test_{int(time.time())}@example.com",
    "password": "password123",
    "role": "patient"
}

try:
    resp = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
    print(f"   ✓ Status: {resp.status_code}")
    if resp.status_code == 200:
        user_data = resp.json()
        print(f"   ✓ Registered: {user_data['username']} (ID: {user_data['id']})")
        print(f"   ✓ Role: {user_data['role']}")
    else:
        print(f"   ✗ Response: {resp.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 3: Login with credentials
print("3. Testing user login...")
login_creds = {
    "username": test_user["username"],
    "password": test_user["password"]
}

try:
    resp = requests.post(f"{BASE_URL}/api/auth/login", json=login_creds)
    print(f"   ✓ Status: {resp.status_code}")
    if resp.status_code == 200:
        login_data = resp.json()
        print(f"   ✓ Token received: {login_data['access_token'][:20]}...")
        print(f"   ✓ User: {login_data['user']['username']} (ID: {login_data['user']['id']})")
        token = login_data['access_token']
    else:
        print(f"   ✗ Response: {resp.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 4: Get patient profile with token
print("4. Testing protected endpoint (get patient profile)...")
if 'token' in locals():
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{BASE_URL}/api/patients/me", headers=headers)
        print(f"   ✓ Status: {resp.status_code}")
        if resp.status_code == 200:
            patient_data = resp.json()
            print(f"   ✓ Patient ID: {patient_data['id']}")
            print(f"   ✓ User ID: {patient_data['user_id']}")
        else:
            print(f"   ✗ Response: {resp.json()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
else:
    print("   ✗ Skipped (no token from login)")

print()
print("=== Test Complete ===")
