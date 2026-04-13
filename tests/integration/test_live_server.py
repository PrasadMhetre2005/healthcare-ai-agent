import json
import threading
import time
import urllib.request
from contextlib import contextmanager
from socket import socket, AF_INET, SOCK_STREAM

from werkzeug.serving import make_server

from api.app import app


def _get_free_port():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    addr, port = sock.getsockname()
    sock.close()
    return port


@contextmanager
def run_server():
    port = _get_free_port()
    server = make_server("127.0.0.1", port, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)


def _post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(url):
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def test_live_health_and_care_gaps():
    with run_server() as base:
        status, body = _get(f"{base}/health")
        assert status == 200
        assert body["status"] == "ok"

        payload = {
            "patient_id": "P-live",
            "age": 60,
            "conditions": ["Diabetes"],
            "medications": [],
            "last_visit_date": "2024-01-01",
            "labs": [],
            "vaccinations": [],
            "missed_appointments_last_12mo": 1,
        }
        status, body = _post(f"{base}/care-gaps", payload)
        assert status == 200
        assert body["patient_id"] == "P-live"
        assert body["status"] == "at-risk"
        assert any(g["category"] == "Chronic disease monitoring" for g in body["gaps"])


def test_live_qa_shape():
    with run_server() as base:
        payload = {"patient_id": "P-live", "question": "Should I take meds with food?"}
        status, body = _post(f"{base}/qa", payload)
        assert status == 200
        assert body["patient_id"] == "P-live"
        assert "answer" in body
