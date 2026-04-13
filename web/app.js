const API_BASE = "http://localhost:8000";

const careGapsInput = document.getElementById("careGapsInput");
const careGapsOutput = document.getElementById("careGapsOutput");
const careGapsBtn = document.getElementById("careGapsBtn");

const apptInput = document.getElementById("apptInput");
const apptOutput = document.getElementById("apptOutput");
const apptBtn = document.getElementById("apptBtn");

const qaInput = document.getElementById("qaInput");
const qaOutput = document.getElementById("qaOutput");
const qaBtn = document.getElementById("qaBtn");

const defaults = {
  care_gaps_example: {
    patient_id: "P-1001",
    age: 56,
    conditions: ["Type 2 Diabetes", "Hypertension"],
    medications: [
      {
        name: "Metformin",
        last_refill_date: "2025-11-15",
        days_supply: 30,
        adherence_rate: 0.72
      }
    ],
    last_visit_date: "2024-12-01",
    labs: [{ name: "LDL", value: "130", last_date: "2025-09-10" }],
    vaccinations: ["Flu 2024"],
    missed_appointments_last_12mo: 2
  },
  appointment_opt_example: {
    patient_id: "P-1001",
    preferred_days: ["2026-04-15", "2026-04-16"],
    preferred_time: "morning",
    available_slots: [
      {
        start: "2026-04-15T09:00:00",
        end: "2026-04-15T09:20:00",
        provider: "Dr. Patel"
      },
      {
        start: "2026-04-15T13:00:00",
        end: "2026-04-15T13:20:00",
        provider: "Dr. Patel"
      }
    ]
  },
  qa_example: {
    patient_id: "P-1001",
    question: "Is it safe to take metformin if I missed a dose yesterday?"
  }
};

careGapsInput.value = JSON.stringify(defaults.care_gaps_example, null, 2);
apptInput.value = JSON.stringify(defaults.appointment_opt_example, null, 2);
qaInput.value = JSON.stringify(defaults.qa_example, null, 2);

async function callApi(path, payload) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}

careGapsBtn.addEventListener("click", async () => {
  careGapsOutput.textContent = "Loading...";
  try {
    const payload = JSON.parse(careGapsInput.value);
    const data = await callApi("/care-gaps", payload);
    careGapsOutput.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    careGapsOutput.textContent = `Error: ${err.message}`;
  }
});

apptBtn.addEventListener("click", async () => {
  apptOutput.textContent = "Loading...";
  try {
    const payload = JSON.parse(apptInput.value);
    const data = await callApi("/appointment/optimize", payload);
    apptOutput.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    apptOutput.textContent = `Error: ${err.message}`;
  }
});

qaBtn.addEventListener("click", async () => {
  qaOutput.textContent = "Loading...";
  try {
    const payload = JSON.parse(qaInput.value);
    const data = await callApi("/qa", payload);
    qaOutput.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    qaOutput.textContent = `Error: ${err.message}`;
  }
});
