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
uvicorn api.app:app --reload
```

2. Frontend
Open `web/index.html` in a browser.

**API endpoints**
- `POST /care-gaps`
- `POST /appointment/optimize`
- `POST /qa`
- `GET /health`

Sample payloads: `api/sample_payloads.json`
