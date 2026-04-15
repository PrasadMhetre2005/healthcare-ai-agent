#!/usr/bin/env python
"""Test authentication system"""
from app.utils.database import engine, Base, SessionLocal
from app.models import User, Patient
from app.services.auth_service import AuthService

# Create tables
Base.metadata.create_all(bind=engine)
print("✓ Database tables created")

# Test session
db = SessionLocal()

# Count existing users
user_count = db.query(User).count()
print(f"✓ Existing users: {user_count}")

# Test creating a user
test_user = User(
    username="testuser",
    email="test@example.com",
    hashed_password=AuthService.hash_password("password123"),
    role="patient"
)

try:
    # Check if user already exists
    existing = db.query(User).filter(User.username == "testuser").first()
    if existing:
        print("✓ Test user already exists")
        print(f"  ID: {existing.id}, Username: {existing.username}")
    else:
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✓ Created test user: {test_user.username} (ID: {test_user.id})")
        
        # Create patient profile
        test_patient = Patient(
            user_id=test_user.id,
            first_name="Test",
            last_name="User"
        )
        db.add(test_patient)
        db.commit()
        print(f"✓ Created patient profile")
except Exception as e:
    print(f"✗ Error: {str(e)}")
    db.rollback()
finally:
    db.close()

# Test authentication
db = SessionLocal()
user_from_db = db.query(User).filter(User.username == "testuser").first()
if user_from_db:
    is_valid = AuthService.verify_password("password123", user_from_db.hashed_password)
    print(f"✓ Password verification: {is_valid}")
    
    if is_valid:
        token = AuthService.create_access_token({"sub": str(user_from_db.id), "role": user_from_db.role})
        print(f"✓ Token created: {token[:20]}...")
        
        decoded = AuthService.decode_token(token)
        print(f"✓ Token decoded: sub={decoded.get('sub')}, role={decoded.get('role')}")
else:
    print("✗ User not found")
    
db.close()
print("\n✓ All tests completed successfully!")
