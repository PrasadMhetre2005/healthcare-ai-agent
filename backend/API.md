# Healthcare AI Agent Backend - API Documentation

## Quick Start

### Option 1: Local Development (SQLite)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py
```

Visit: http://localhost:8000/docs

### Option 2: Docker (PostgreSQL + API)

```bash
cd backend
docker-compose up
```

Visit: http://localhost:8000/docs

---

## API Overview

### 1. **Authentication**

All protected endpoints require `Authorization: Bearer {token}` header

#### Register
```http
POST /api/auth/register
```

**Payload:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "role": "patient"  // or "doctor"
}
```

#### Login
```http
POST /api/auth/login
```

**Payload:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "patient"
  }
}
```

---

### 2. **Patient Management**

#### Create Patient Profile
```http
POST /api/patients/
Authorization: Bearer {token}
```

**Payload:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "gender": "M",
  "blood_type": "O+",
  "allergies": "Penicillin, Sulfa drugs",
  "medical_history": "Hypertension, Type 2 Diabetes",
  "emergency_contact": "Jane Doe",
  "emergency_phone": "+1234567890"
}
```

#### Get My Profile
```http
GET /api/patients/me
Authorization: Bearer {token}
```

---

### 3. **Health Data Logging**

#### Log Health Metrics
```http
POST /api/health-data/
Authorization: Bearer {token}
```

**Payload:**
```json
{
  "blood_pressure_systolic": 130,
  "blood_pressure_diastolic": 85,
  "heart_rate": 72,
  "temperature": 36.8,
  "respiratory_rate": 16,
  "blood_glucose": 110,
  "weight": 75.5,
  "height": 180,
  "lab_results": "{\"hemoglobin\": 14.5, \"hematocrit\": 43}",
  "doctor_notes": "Patient reports feeling well",
  "symptoms": "[\"fatigue\", \"headache\"]",
  "source": "manual_entry"
}
```

#### Get Health Records (Last 30 days)
```http
GET /api/health-data/patient/{patient_id}?days=30
```

#### Get Latest Record
```http
GET /api/health-data/patient/{patient_id}/latest
```

#### Get Health Trends
```http
GET /api/health-data/patient/{patient_id}/trends?days=30
```

**Response:**
```json
{
  "blood_pressure": [
    {"date": "2024-01-10T10:00:00", "systolic": 130, "diastolic": 85}
  ],
  "heart_rate": [
    {"date": "2024-01-10T10:00:00", "value": 72}
  ],
  "temperature": [],
  "blood_glucose": [],
  "weight": []
}
```

---

### 4. **Alerts & Notifications**

#### Get Patient Alerts
```http
GET /api/alerts/patient/{patient_id}
```

#### Get Unresolved Alerts
```http
GET /api/alerts/patient/{patient_id}/unresolved
```

#### Resolve an Alert
```http
PUT /api/alerts/{alert_id}/resolve
```

**Alert Types:**
- `abnormal_reading` - Vital signs outside normal range
- `medication_interaction` - Drug interaction warning
- `appointment_reminder` - Upcoming appointment
- `critical_condition` - Emergency alert

**Severity Levels:**
- `low` - Informational
- `medium` - Monitor closely
- `high` - Requires attention
- `critical` - Immediate action needed

---

### 5. **AI Insights & Recommendations**

#### Generate Recommendations
```http
GET /api/recommendations/patient/{patient_id}/generate
```

**Response:**
```json
{
  "patient_id": 1,
  "recommendations": [
    {
      "id": 1,
      "category": "lifestyle",
      "priority": "high",
      "title": "Increase Physical Activity",
      "description": "Aim for 30 minutes of moderate exercise daily",
      "reason": "Blood pressure elevated over past week",
      "generated_by": "AI",
      "created_at": "2024-01-10T10:00:00"
    }
  ],
  "generated_at": "2024-01-10T10:00:00"
}
```

#### Get Health Insights
```http
GET /api/recommendations/patient/{patient_id}/insights
```

**Response:**
```json
{
  "patient_id": 1,
  "insights": "Based on your data from the past 30 days, your blood pressure shows an upward trend. This is concerning. We recommend...",
  "generated_at": "2024-01-10T10:00:00"
}
```

---

### 6. **Doctor Management**

#### List Doctors by Specialization
```http
GET /api/doctors/specialization/Cardiology
```

#### Get Doctor Profile
```http
GET /api/doctors/{doctor_id}
```

---

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Email address
- `hashed_password`: Bcrypt hash
- `role`: "patient", "doctor", or "admin"
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Patient
- Inherits from User
- `date_of_birth`, `gender`, `blood_type`
- `allergies`, `medical_history`, `current_medications`
- `assigned_doctor_id`: Foreign key to Doctor

### HealthData
- `patient_id`: Foreign key
- Vitals: blood_pressure, heart_rate, temperature, respiratory_rate
- Labs: lab_results (JSON), blood_glucose, BMI
- Clinical: doctor_notes, symptoms, medications_taken
- Metadata: source (manual, wearable, lab)

### Alert
- `patient_id`: Foreign key
- `alert_type`: Category of alert
- `severity`: low, medium, high, critical
- `is_resolved`: Boolean flag
- `triggered_by`: What caused the alert

### Recommendation
- `patient_id`: Foreign key
- `category`: lifestyle, medication, appointment, diet, exercise
- `priority`: low, medium, high
- `generated_by`: "AI", "Doctor", "System"

### Doctor
- Inherits from User
- `medical_license`: Unique license number
- `specialization`: Medical specialty
- `hospital_name`: Affiliated hospital
- `patients_count`: Number of assigned patients

---

## Authentication Flow

```
1. User registers: POST /api/auth/register
2. System creates User + Patient/Doctor profile
3. User logs in: POST /api/auth/login
4. System validates credentials & returns JWT token
5. User includes token in Authorization header: "Bearer {token}"
6. System validates token for protected routes
7. Token expires in 30 minutes (configurable)
8. User logs in again to refresh token
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid credentials or expired token)
- `403` - Forbidden (not authorized for this resource)
- `404` - Not Found
- `500` - Server Error

---

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=app
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./healthcare.db` | Database connection string |
| `SECRET_KEY` | (required) | JWT secret key |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration |
| `OPENAI_API_KEY` | (required) | OpenAI API key for AI features |
| `DEBUG` | `False` | Debug mode |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8000` | Server port |

---

## Load Testing Example

```bash
# Using Apache Bench
ab -n 1000 -c 100 http://localhost:8000/health

# Using Hey
hey -n 1000 -c 100 http://localhost:8000/health
```

---

## Security Best Practices

✅ **Implemented:**
- Password hashing with bcrypt
- JWT token-based auth
- CORS middleware
- Environment variable secrets
- Input validation (Pydantic)
- Database parameterized queries

⚠️ **Recommended for Production:**
- HTTPS/TLS encryption
- Rate limiting
- API key rotation
- Database backups
- Monitoring & logging
- Firewall rules
- DDoS protection

---

## Support & Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Database Connection Failed
- Check DATABASE_URL
- Ensure PostgreSQL is running (if using PostgreSQL)
- Check credentials

### Token Expired
- Login again to get new token
- Implement token refresh endpoint for better UX

### OpenAI API Errors
- Verify API key
- Check API quota
- Ensure stable internet connection

---

## Next Steps

1. ✅ Backend API complete
2. ⏭️ Frontend Dashboard (React/Vue)
3. ⏭️ Mobile App (React Native/Flutter)
4. ⏭️ Wearable Device Integration
5. ⏭️ Advanced Analytics Dashboard
