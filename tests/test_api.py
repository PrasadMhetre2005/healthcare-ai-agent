from api.app import app


client = app.test_client()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_care_gaps_basic_rules():
    payload = {
        "patient_id": "P-1",
        "age": 55,
        "conditions": ["Type 2 Diabetes"],
        "medications": [
            {
                "name": "Metformin",
                "adherence_rate": 0.7,
            }
        ],
        "last_visit_date": "2024-01-01",
        "labs": [],
        "vaccinations": [],
        "missed_appointments_last_12mo": 2,
    }
    res = client.post("/care-gaps", json=payload)
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "at-risk"
    assert body["risk_of_missed_followup"] == "high"
    # Expect diabetes A1c gap + adherence gap + overdue visit
    categories = {g["category"] for g in body["gaps"]}
    assert "Chronic disease monitoring" in categories
    assert "Medication management" in categories
    assert "Preventive care" in categories


def test_appointment_optimize_prefers_matching_slot():
    payload = {
        "patient_id": "P-2",
        "preferred_days": ["2026-04-15"],
        "preferred_time": "morning",
        "available_slots": [
            {
                "start": "2026-04-15T09:00:00",
                "end": "2026-04-15T09:20:00",
                "provider": "Dr. Patel",
            },
            {
                "start": "2026-04-15T13:00:00",
                "end": "2026-04-15T13:20:00",
                "provider": "Dr. Patel",
            },
        ],
    }
    res = client.post("/appointment/optimize", json=payload)
    assert res.status_code == 200
    body = res.get_json()
    assert body["recommended_slot"]["start"] == "2026-04-15T09:00:00"


def test_qa_response_shape():
    payload = {
        "patient_id": "P-3",
        "question": "Can I take my meds with food?",
    }
    res = client.post("/qa", json=payload)
    assert res.status_code == 200
    body = res.get_json()
    assert body["patient_id"] == "P-3"
    assert body["confidence"] in {"low", "medium", "high"}
    assert isinstance(body["sources"], list)
