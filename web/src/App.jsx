import { useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

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

function App() {
  const [careInput, setCareInput] = useState(
    JSON.stringify(defaults.care_gaps_example, null, 2)
  );
  const [careOutput, setCareOutput] = useState("");

  const [apptInput, setApptInput] = useState(
    JSON.stringify(defaults.appointment_opt_example, null, 2)
  );
  const [apptOutput, setApptOutput] = useState("");

  const [qaInput, setQaInput] = useState(
    JSON.stringify(defaults.qa_example, null, 2)
  );
  const [qaOutput, setQaOutput] = useState("");

  async function callApi(path, payload) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return res.json();
  }

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Healthcare AI Agent MVP</p>
          <h1>Care Gap Alerts, Smart Scheduling, and Patient Q&amp;A</h1>
          <p className="sub">
            A minimal React UI that connects to the local API server for real
            time care-gap and appointment recommendations.
          </p>
        </div>
        <div className="hero-card">
          <p className="hero-card-title">Endpoints</p>
          <ul>
            <li>POST /care-gaps</li>
            <li>POST /appointment/optimize</li>
            <li>POST /qa</li>
          </ul>
          <p className="muted">API base: {API_BASE}</p>
        </div>
      </header>

      <section className="grid">
        <div className="panel">
          <h2>Care Gap Alerts</h2>
          <textarea
            rows="12"
            value={careInput}
            onChange={(e) => setCareInput(e.target.value)}
          />
          <button
            onClick={async () => {
              setCareOutput("Loading...");
              try {
                const payload = JSON.parse(careInput);
                const data = await callApi("/care-gaps", payload);
                setCareOutput(JSON.stringify(data, null, 2));
              } catch (err) {
                setCareOutput(`Error: ${err.message}`);
              }
            }}
          >
            Generate Care Gaps
          </button>
          <pre>{careOutput}</pre>
        </div>

        <div className="panel">
          <h2>Appointment Optimization</h2>
          <textarea
            rows="10"
            value={apptInput}
            onChange={(e) => setApptInput(e.target.value)}
          />
          <button
            onClick={async () => {
              setApptOutput("Loading...");
              try {
                const payload = JSON.parse(apptInput);
                const data = await callApi("/appointment/optimize", payload);
                setApptOutput(JSON.stringify(data, null, 2));
              } catch (err) {
                setApptOutput(`Error: ${err.message}`);
              }
            }}
          >
            Optimize Appointment
          </button>
          <pre>{apptOutput}</pre>
        </div>

        <div className="panel">
          <h2>Patient Q&amp;A</h2>
          <textarea
            rows="7"
            value={qaInput}
            onChange={(e) => setQaInput(e.target.value)}
          />
          <button
            onClick={async () => {
              setQaOutput("Loading...");
              try {
                const payload = JSON.parse(qaInput);
                const data = await callApi("/qa", payload);
                setQaOutput(JSON.stringify(data, null, 2));
              } catch (err) {
                setQaOutput(`Error: ${err.message}`);
              }
            }}
          >
            Answer Question
          </button>
          <pre>{qaOutput}</pre>
        </div>
      </section>
    </div>
  );
}

export default App;
