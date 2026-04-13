from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
