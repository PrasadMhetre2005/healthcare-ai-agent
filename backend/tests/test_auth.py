"""
Test suite for authentication endpoints
"""

import pytest
from app.schemas.user import UserCreate


def test_register_user(test_db):
    """Test user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "patient"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_register_duplicate_username(test_db):
    """Test duplicate username registration"""
    # Register first user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "patient"
        }
    )
    
    # Try to register with same username
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpass123",
            "role": "patient"
        }
    )
    assert response.status_code == 400


def test_login(test_db):
    """Test user login"""
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "patient"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(test_db):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
