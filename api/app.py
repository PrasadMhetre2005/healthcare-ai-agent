from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
app = Flask(__name__)
CORS(app)


def _parse_iso_date(value: str):
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


@app.get("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"})


@app.post("/care-gaps")
def care_gaps():
    payload = request.get_json(force=True) or {}
    gaps = []

    last_visit_date = payload.get("last_visit_date")
    if last_visit_date:
        last_visit = _parse_iso_date(last_visit_date)
        if last_visit and datetime.utcnow() - last_visit > timedelta(days=365):
            gaps.append(
                {
                    "category": "Preventive care",
                    "severity": "medium",
                    "urgency": "routine",
                    "rationale": "Annual visit overdue (>12 months).",
                }
            )
    else:
        gaps.append(
            {
                "category": "Preventive care",
                "severity": "medium",
                "urgency": "routine",
                "rationale": "No recent visit on record.",
            }
        )

    conditions = payload.get("conditions", [])
    if any("diabetes" in c.lower() for c in conditions):
        labs = payload.get("labs", [])
        has_a1c = any("a1c" in (l.get("name", "").lower()) for l in labs)
        if not has_a1c:
            gaps.append(
                {
                    "category": "Chronic disease monitoring",
                    "severity": "high",
                    "urgency": "soon",
                    "rationale": "Diabetes without recent A1c lab.",
                }
            )

    for med in payload.get("medications", []):
        adherence = med.get("adherence_rate")
        if adherence is not None and adherence < 0.8:
            gaps.append(
                {
                    "category": "Medication management",
                    "severity": "medium",
                    "urgency": "soon",
                    "rationale": f"Adherence below 80% for {med.get('name', 'medication')}.",
                }
            )

    missed = int(payload.get("missed_appointments_last_12mo", 0))
    if missed >= 2:
        risk = "high"
    elif missed == 1:
        risk = "medium"
    else:
        risk = "low"

    status = "compliant" if not gaps else "at-risk"
    return jsonify(
        {
            "patient_id": payload.get("patient_id"),
            "status": status,
            "gaps": gaps,
            "risk_of_missed_followup": risk,
        }
    )


@app.post("/appointment/optimize")
def optimize_appointment():
    payload = request.get_json(force=True) or {}
    slots = payload.get("available_slots", [])
    if not slots:
        return jsonify(
            {
                "patient_id": payload.get("patient_id"),
                "recommended_slot": None,
                "reason": "No available slots provided.",
            }
        )

    preferred_days = set(payload.get("preferred_days", []))
    preferred_time = payload.get("preferred_time")

    preferred = None
    for slot in slots:
        start = slot.get("start", "")
        if preferred_days and start[:10] not in preferred_days:
            continue
        if preferred_time:
            hour = int(start[11:13])
            if preferred_time == "morning" and hour >= 12:
                continue
            if preferred_time == "afternoon" and hour < 12:
                continue
        preferred = slot
        break

    if not preferred:
        preferred = slots[0]

    return jsonify(
        {
            "patient_id": payload.get("patient_id"),
            "recommended_slot": preferred,
            "reason": "Matched preferred day/time where possible.",
        }
    )


@app.post("/qa")
def patient_doctor_qa():
    payload = request.get_json(force=True) or {}
    answer = (
        "This is a draft response based on the question. "
        "For clinical accuracy, a clinician should review before sending."
    )
    return jsonify(
        {
            "patient_id": payload.get("patient_id"),
            "answer": answer,
            "confidence": "low",
            "sources": ["internal-knowledge-base"],
        }
    )


@app.post("/alerts/sms")
def send_sms_alert():
    payload = request.get_json(force=True) or {}
    to_number = payload.get("to")
    body = payload.get("message")
    template = payload.get("template")
    template_data = payload.get("data", {})

    if template and not body:
        body = build_sms_message(template, template_data)

    if not to_number or not body:
        return jsonify({"error": "Missing 'to' or 'message'"}), 400

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not account_sid or not auth_token or not from_number:
        return (
            jsonify(
                {
                    "error": "Twilio credentials not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER."
                }
            ),
            500,
        )

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number,
    )

    return jsonify({"status": "sent", "sid": message.sid, "message": body})


def build_sms_message(template: str, data: dict) -> str:
    patient = data.get("patient_name", "Patient")
    if template == "care_gap":
        gap = data.get("gap", "preventive care")
        due = data.get("due", "soon")
        return (
            f"Hi {patient}, your care gap alert: {gap} is due {due}. "
            "Please schedule your visit."
        )
    if template == "appointment":
        date = data.get("date", "an upcoming date")
        provider = data.get("provider", "your clinician")
        return (
            f"Hi {patient}, reminder: appointment with {provider} on {date}. "
            "Reply to confirm or reschedule."
        )
    return data.get("message", "Healthcare notification.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
