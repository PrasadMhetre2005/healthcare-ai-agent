import { useRef, useState } from "react";
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
  const [searchInput, setSearchInput] = useState(
    "Ask about medications, symptoms, or follow-ups..."
  );
  const [qaOutput, setQaOutput] = useState("");
  const [careOutput, setCareOutput] = useState("");
  const [apptOutput, setApptOutput] = useState("");
  const [voiceStatus, setVoiceStatus] = useState("Idle");
  const [voiceTranscript, setVoiceTranscript] = useState("");
  const [voiceAnswer, setVoiceAnswer] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [voiceLang, setVoiceLang] = useState("en-US");
  const recognitionRef = useRef(null);
  const [smsPhone, setSmsPhone] = useState("+15551234567");
  const [smsResult, setSmsResult] = useState("");
  const [smsCustom, setSmsCustom] = useState(
    "Care gap: annual exam overdue. Please schedule."
  );

  async function callApi(path, payload) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return res.json();
  }

  async function runCareGaps() {
    setCareOutput("Loading...");
    try {
      const data = await callApi("/care-gaps", defaults.care_gaps_example);
      setCareOutput(JSON.stringify(data, null, 2));
    } catch (err) {
      setCareOutput(`Error: ${err.message}`);
    }
  }

  async function runAppointment() {
    setApptOutput("Loading...");
    try {
      const data = await callApi(
        "/appointment/optimize",
        defaults.appointment_opt_example
      );
      setApptOutput(JSON.stringify(data, null, 2));
    } catch (err) {
      setApptOutput(`Error: ${err.message}`);
    }
  }

  async function runQA() {
    setQaOutput("Loading...");
    try {
      const payload = {
        ...defaults.qa_example,
        question: searchInput || defaults.qa_example.question
      };
      const data = await callApi("/qa", payload);
      setQaOutput(JSON.stringify(data, null, 2));
    } catch (err) {
      setQaOutput(`Error: ${err.message}`);
    }
  }

  async function runVoiceQA(transcript) {
    setVoiceAnswer("Loading...");
    try {
      const payload = {
        ...defaults.qa_example,
        question: transcript || defaults.qa_example.question
      };
      const data = await callApi("/qa", payload);
      const answer = data.answer || "No answer available.";
      setVoiceAnswer(answer);
      if ("speechSynthesis" in window) {
        const utter = new SpeechSynthesisUtterance(answer);
        utter.rate = 1;
        utter.pitch = 1;
        utter.lang = voiceLang;
        window.speechSynthesis.speak(utter);
      }
    } catch (err) {
      setVoiceAnswer(`Error: ${err.message}`);
    }
  }

  function startVoice() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceStatus("Speech recognition not supported in this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;
    recognition.lang = voiceLang;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setVoiceStatus("Listening...");
      setIsListening(true);
    };
    recognition.onend = () => {
      setVoiceStatus("Idle");
      setIsListening(false);
    };
    recognition.onerror = () => {
      setVoiceStatus("Error listening.");
      setIsListening(false);
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setVoiceTranscript(transcript);
      runVoiceQA(transcript);
    };

    recognition.start();
  }

  function stopVoice() {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setVoiceStatus("Stopped");
      setIsListening(false);
    }
  }

  async function sendSms(payload) {
    setSmsResult("Sending...");
    try {
      const data = await callApi("/alerts/sms", payload);
      setSmsResult(JSON.stringify(data, null, 2));
    } catch (err) {
      setSmsResult(`Error: ${err.message}`);
    }
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="logo">
          <span className="logo-icon">+</span>
          MediBuddy
        </div>
        <nav className="nav">
          <button className="nav-item active">
            <span className="nav-icon">🩺</span>
            Check Symptoms
          </button>
          <button className="nav-item">
            <span className="nav-icon">💓</span>
            Manage Vitals
          </button>
          <button className="nav-item">
            <span className="nav-icon">📅</span>
            Book Appointment
          </button>
          <button className="nav-item">
            <span className="nav-icon">📁</span>
            My Records
          </button>
        </nav>
        <div className="sidebar-footer">
          <p>AI Agent</p>
          <small>Connected to local API</small>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <h1>Hi Sarah, how can MediBuddy help you today?</h1>
          <span className="header-pill">AI Powered</span>
        </header>

        <section className="hero-grid">
          <div className="search-card">
            <div className="bot">
              <div className="bot-face">
                <span className="bot-eye" />
                <span className="bot-eye" />
                <span className="bot-smile" />
              </div>
              <div>
                <p className="bot-label">Ask or describe symptoms</p>
                <p className="bot-sub">Your personal health assistant</p>
              </div>
            </div>
            <div className="search-bar">
              <input
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Type or speak a question..."
              />
              <button className="icon-btn" onClick={runQA} aria-label="Ask">
                <span className="mic">🎤</span>
                Ask
              </button>
            </div>
            <pre className="result">{qaOutput || "Q&A response will appear here."}</pre>
          </div>

          <div className="insight-card">
            <h3>Personal Insight</h3>
            <div className="insight-row">
              <span>Last BP</span>
              <span className="pill">118/78 mmHg</span>
            </div>
            <div className="insight-row">
              <span>Current Medication</span>
              <span>Cetirizine 10mg (8am)</span>
            </div>
            <div className="insight-row">
              <span>Health Goal</span>
              <span>Steps 7500/10000</span>
            </div>
            <div className="progress">
              <div className="bar" />
            </div>
            <div className="insight-cta">
              <p>Care Gaps</p>
              <button onClick={runCareGaps}>Analyze</button>
            </div>
            <div className="doctor-illustration">
              <div className="doctor-head" />
              <div className="doctor-body" />
              <div className="doctor-card">
                <span>✔</span>
                Summary
              </div>
            </div>
            <pre className="result">{careOutput || "Care gap alert output."}</pre>
          </div>
        </section>

        <section className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-grid">
            <button className="action-card green" onClick={runCareGaps}>
              <span className="action-icon">🔍</span>
              <span>Start Symptom Check</span>
              <strong>Care Gap Scan</strong>
            </button>
            <button className="action-card blue" onClick={runAppointment}>
              <span className="action-icon">📈</span>
              <span>View Your Vitals</span>
              <strong>Optimize Appointment</strong>
            </button>
            <button className="action-card amber" onClick={runQA}>
              <span className="action-icon">🗓️</span>
              <span>Ask a Question</span>
              <strong>Patient Q&amp;A</strong>
            </button>
          </div>
          <pre className="result">{apptOutput || "Appointment optimization output."}</pre>
        </section>

        <section className="voice-section">
          <div className="voice-card">
            <h2>Voice Assistant</h2>
            <p className="voice-sub">
              Tap to speak your healthcare question. The assistant will answer and
              read it back to you.
            </p>
            <div className="voice-controls">
              <button className="voice-btn" onClick={startVoice}>
                🎙️ Start Listening
              </button>
              <button className="voice-btn stop" onClick={stopVoice}>
                ⏹ Stop Listening
              </button>
              <span className="voice-status">{voiceStatus}</span>
            </div>
            <div className="voice-controls secondary">
              <label className="voice-label" htmlFor="voice-lang">
                Language
              </label>
              <select
                id="voice-lang"
                className="voice-select"
                value={voiceLang}
                onChange={(e) => setVoiceLang(e.target.value)}
              >
                <option value="en-US">English (US)</option>
                <option value="en-IN">English (India)</option>
                <option value="hi-IN">Hindi</option>
                <option value="mr-IN">Marathi</option>
                <option value="es-ES">Spanish</option>
              </select>
              <span className={`wave ${isListening ? "active" : ""}`}>
                <span />
                <span />
                <span />
                <span />
                <span />
              </span>
            </div>
            <div className="voice-grid">
              <div>
                <h3>Transcript</h3>
                <div className="voice-box">
                  {voiceTranscript || "Your spoken question will appear here."}
                </div>
              </div>
              <div>
                <h3>AI Response</h3>
                <div className="voice-box">
                  {voiceAnswer || "The response will appear here."}
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="sms-section">
          <div className="sms-card">
            <h2>SMS Alerts</h2>
            <p className="voice-sub">
              Send care gap and appointment reminders to patients.
            </p>
            <div className="sms-row">
              <label htmlFor="sms-phone">Patient Mobile</label>
              <input
                id="sms-phone"
                value={smsPhone}
                onChange={(e) => setSmsPhone(e.target.value)}
                placeholder="+15551234567"
              />
            </div>
            <div className="sms-actions">
              <button
                className="action-card green"
                onClick={() =>
                  sendSms({
                    to: smsPhone,
                    template: "care_gap",
                    data: {
                      patient_name: "Sarah",
                      gap: "Annual exam",
                      due: "this week"
                    }
                  })
                }
              >
                <span className="action-icon">✅</span>
                <span>Care Gap</span>
                <strong>Send Reminder</strong>
              </button>
              <button
                className="action-card amber"
                onClick={() =>
                  sendSms({
                    to: smsPhone,
                    template: "appointment",
                    data: {
                      patient_name: "Sarah",
                      provider: "Dr. Patel",
                      date: "Apr 20 at 10:00 AM"
                    }
                  })
                }
              >
                <span className="action-icon">📅</span>
                <span>Appointment</span>
                <strong>Send Reminder</strong>
              </button>
            </div>
            <div className="sms-row">
              <label htmlFor="sms-custom">Custom Message</label>
              <textarea
                id="sms-custom"
                rows="3"
                value={smsCustom}
                onChange={(e) => setSmsCustom(e.target.value)}
              />
            </div>
            <button
              className="voice-btn"
              onClick={() => sendSms({ to: smsPhone, message: smsCustom })}
            >
              Send Custom SMS
            </button>
            <pre className="result">{smsResult || "SMS responses appear here."}</pre>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
