from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta

app = FastAPI(title="Healthcare AI Agent MVP", version="0.1.0")


class Medication(BaseModel):
    name: str
    last_refill_date: Optional[str] = None
    days_supply: Optional[int] = None
    adherence_rate: Optional[float] = None


class LabResult(BaseModel):
    name: str
    value: Optional[str] = None
    last_date: Optional[str] = None


class PatientInput(BaseModel):
    patient_id: str
    age: int
    conditions: List[str] = []
    medications: List[Medication] = []
    last_visit_date: Optional[str] = None
    labs: List[LabResult] = []
    vaccinations: List[str] = []
    missed_appointments_last_12mo: int = 0


class CareGap(BaseModel):
    category: str
    severity: str
    urgency: str
    rationale: str


class CareGapResponse(BaseModel):
    patient_id: str
    status: str
    gaps: List[CareGap]
    risk_of_missed_followup: str


class Slot(BaseModel):
    start: str
    end: str
    provider: str


class AppointmentRequest(BaseModel):
    patient_id: str
    preferred_days: List[str] = []
    preferred_time: Optional[str] = None  # "morning" | "afternoon"
    available_slots: List[Slot] = []


class AppointmentResponse(BaseModel):
    patient_id: str
    recommended_slot: Optional[Slot] = None
    reason: str


class QARequest(BaseModel):
    patient_id: str
    question: str = Field(..., min_length=3)


class QAResponse(BaseModel):
    patient_id: str
    answer: str
    confidence: str
    sources: List[str]


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.post("/care-gaps", response_model=CareGapResponse)
def care_gaps(payload: PatientInput):
    gaps: List[CareGap] = []

    # Preventive care rule: annual visit overdue
    if payload.last_visit_date:
        try:
            last_visit = datetime.fromisoformat(payload.last_visit_date)
            if datetime.utcnow() - last_visit > timedelta(days=365):
                gaps.append(
                    CareGap(
                        category="Preventive care",
                        severity="medium",
                        urgency="routine",
                        rationale="Annual visit overdue (>12 months).",
                    )
                )
        except ValueError:
            pass
    else:
        gaps.append(
            CareGap(
                category="Preventive care",
                severity="medium",
                urgency="routine",
                rationale="No recent visit on record.",
            )
        )

    # Chronic disease monitoring rule: diabetes A1c
    if any("diabetes" in c.lower() for c in payload.conditions):
        has_a1c = any("a1c" in l.name.lower() for l in payload.labs)
        if not has_a1c:
            gaps.append(
                CareGap(
                    category="Chronic disease monitoring",
                    severity="high",
                    urgency="soon",
                    rationale="Diabetes without recent A1c lab.",
                )
            )

    # Medication refill/adherence rule
    for med in payload.medications:
        if med.adherence_rate is not None and med.adherence_rate < 0.8:
            gaps.append(
                CareGap(
                    category="Medication management",
                    severity="medium",
                    urgency="soon",
                    rationale=f"Adherence below 80% for {med.name}.",
                )
            )

    risk = "low"
    if payload.missed_appointments_last_12mo >= 2:
        risk = "high"
    elif payload.missed_appointments_last_12mo == 1:
        risk = "medium"

    status = "compliant" if not gaps else "at-risk"
    return CareGapResponse(
        patient_id=payload.patient_id,
        status=status,
        gaps=gaps,
        risk_of_missed_followup=risk,
    )


@app.post("/appointment/optimize", response_model=AppointmentResponse)
def optimize_appointment(payload: AppointmentRequest):
    if not payload.available_slots:
        return AppointmentResponse(
            patient_id=payload.patient_id,
            recommended_slot=None,
            reason="No available slots provided.",
        )

    # Simple heuristic: prefer day/time match, else first slot
    preferred = None
    for slot in payload.available_slots:
        if payload.preferred_days and slot.start[:10] not in payload.preferred_days:
            continue
        if payload.preferred_time:
            hour = int(slot.start[11:13])
            if payload.preferred_time == "morning" and hour >= 12:
                continue
            if payload.preferred_time == "afternoon" and hour < 12:
                continue
        preferred = slot
        break

    if not preferred:
        preferred = payload.available_slots[0]

    return AppointmentResponse(
        patient_id=payload.patient_id,
        recommended_slot=preferred,
        reason="Matched preferred day/time where possible.",
    )


@app.post("/qa", response_model=QAResponse)
def patient_doctor_qa(payload: QARequest):
    # Placeholder for retrieval + LLM layer
    answer = (
        "This is a draft response based on the question. "
        "For clinical accuracy, a clinician should review before sending."
    )
    return QAResponse(
        patient_id=payload.patient_id,
        answer=answer,
        confidence="low",
        sources=["internal-knowledge-base"],
    )
