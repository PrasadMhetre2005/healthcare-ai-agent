# Healthcare AI Monitoring Agent - Backend API

A FastAPI-based backend for real-time patient health monitoring with AI-powered insights and alerts.

## 📋 Features

- **User Management**: Register and authenticate patients and doctors
- **Patient Profiles**: Comprehensive patient health information
- **Health Monitoring**: Track vital signs, lab results, symptoms
- **Smart Alerts**: Automatic alerts for abnormal readings
- **AI Insights**: GPT-powered health analysis and recommendations
- **Doctor Dashboard**: Physicians can monitor assigned patients
- **Real-time Trends**: Visual health trends over time

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Authentication**: JWT (JSON Web Tokens)
- **AI**: OpenAI GPT-3.5-turbo
- **ORM**: SQLAlchemy
- **Async**: AsyncIO

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9+
- PostgreSQL (optional, SQLite for development)
- OpenAI API Key

### 2. Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./healthcare.db  # For development
# DATABASE_URL=postgresql://user:password@localhost:5432/healthcare_db

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# Server
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 4. Initialize Database

```bash
python -c "from app.main import app; print('Database initialized')"
```

### 5. Run the Server

```bash
python run.py
# or
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token

### Patients
- `POST /api/patients/` - Create patient profile
- `GET /api/patients/me` - Get current patient profile
- `GET /api/patients/{patient_id}` - Get patient by ID
- `PUT /api/patients/{patient_id}` - Update patient profile

### Health Data
- `POST /api/health-data/` - Log health data
- `GET /api/health-data/patient/{patient_id}` - Get health records
- `GET /api/health-data/patient/{patient_id}/latest` - Get latest record
- `GET /api/health-data/patient/{patient_id}/trends` - Get health trends

### Alerts
- `GET /api/alerts/patient/{patient_id}` - Get patient alerts
- `GET /api/alerts/patient/{patient_id}/unresolved` - Get unresolved alerts
- `PUT /api/alerts/{alert_id}/resolve` - Resolve an alert

### Recommendations
- `GET /api/recommendations/patient/{patient_id}/generate` - Generate recommendations
- `GET /api/recommendations/patient/{patient_id}` - Get recommendations
- `GET /api/recommendations/patient/{patient_id}/insights` - Get health insights

### Doctors
- `POST /api/doctors/` - Register doctor
- `GET /api/doctors/{doctor_id}` - Get doctor profile
- `GET /api/doctors/` - List all doctors
- `GET /api/doctors/specialization/{specialization}` - Get doctors by specialization

## 📝 Example Usage

### 1. Register a Patient

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword",
    "role": "patient"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword"
  }'
```

### 3. Create Patient Profile

```bash
curl -X POST "http://localhost:8000/api/patients/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "gender": "M",
    "blood_type": "O+",
    "allergies": "Penicillin",
    "medical_history": "Hypertension"
  }'
```

### 4. Log Health Data

```bash
curl -X POST "http://localhost:8000/api/health-data/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "blood_pressure_systolic": 130,
    "blood_pressure_diastolic": 85,
    "heart_rate": 72,
    "temperature": 36.8,
    "blood_glucose": 95,
    "weight": 75,
    "height": 180,
    "source": "manual_entry"
  }'
```

## 🚀 Deployment

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t healthcare-api .
docker run -p 8000:8000 --env-file .env healthcare-api
```

## 📂 Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities (DB, security)
│   └── main.py          # FastAPI app
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
└── run.py              # Entry point
```

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS middleware configured
- Environment variables for secrets
- HTTPS ready

## 🤖 AI Integration

The backend integrates with OpenAI API for:

- **Health Insights**: Analyze patient data patterns
- **Recommendations**: Generate personalized care suggestions
- **Medication Interactions**: Check for drug interactions
- **Risk Assessment**: Identify potential health risks

## 📊 Alert Thresholds

Health data is monitored against these thresholds:

- Blood Pressure: High (≥140/90), Low (≤90/60)
- Heart Rate: High (≥100), Low (<60)
- Temperature: High (≥38°C), Low (<36°C)
- Blood Glucose: High (≥200), Low (≤70)

Custom thresholds can be configured per patient.

## 🐛 Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- For SQLite: ensure write permissions for app directory

### OpenAI API Error
- Verify OPENAI_API_KEY is valid
- Check API quota and billing
- Network connectivity issues?

### Token Expiration
- Tokens expire after 30 minutes (configurable)
- Login again to get new token
- Frontend should refresh tokens automatically

## 📝 Future Enhancements

- [ ] Wearable device integration
- [ ] Mobile app backend
- [ ] Real-time WebSocket notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] FHIR compliance
- [ ] Telemedicine integration

## 📄 License

MIT License - See LICENSE file

## 👥 Support

For issues and questions, please open an issue in the repository.
