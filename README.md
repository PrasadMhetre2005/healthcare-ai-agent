# Healthcare AI Agent MVP

Minimal MVP for:
- Care gap alerts
- Appointment optimization
- Patient-doctor Q&amp;A

**Repo layout**
- `api/` FastAPI backend
- `web/` Minimal web UI
- `care-gap-architecture.svg` Architecture diagram

**Quick start (local)**
1. Backend
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r api\\requirements.txt
python api\\app.py
```

2. Frontend (React)
```
cd web
npm install
npm run dev
```

**API endpoints**
- `POST /care-gaps`
- `POST /appointment/optimize`
- `POST /qa`
- `POST /alerts/sms`
- `GET /health`

Sample payloads: `api/sample_payloads.json`

**Twilio SMS setup**
1. Copy `.env.example` to `.env` and fill your Twilio credentials.
2. Install dependencies:
```
pip install -r api\\requirements.txt
```
3. Send an SMS:
```
curl -X POST http://127.0.0.1:8000/alerts/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"to\":\"+15551234567\",\"message\":\"Care gap: annual exam overdue.\"}"
```

**SMS templates**
Send a template by passing `template` and `data`:
```
curl -X POST http://127.0.0.1:8000/alerts/sms ^
  -H "Content-Type: application/json" ^
  -d "{\"to\":\"+15551234567\",\"template\":\"care_gap\",\"data\":{\"patient_name\":\"Sarah\",\"gap\":\"Annual exam\",\"due\":\"this week\"}}"
```
