"""Task 7: Run & Test FastAPI App Locally.

1. Start the server (terminal 1, from the project root):
       uvicorn main:app --reload

2. Test the endpoints with ANY of these:

   Browser    http://127.0.0.1:8000/health
              http://127.0.0.1:8000/docs      (Swagger UI -> POST /chat -> "Try it out")

   Postman    Method: POST    URL: http://127.0.0.1:8000/chat
              Body -> raw -> JSON:   {"query": "What do customers say about the products?"}

   curl       curl http://127.0.0.1:8000/health
              curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
                   -d "{\"query\": \"What do customers say about the products?\"}"

3. Or run this script (terminal 2) for an automated smoke test:
       python "PART 4 — Serving the Groq App/task7_run_and_test_api.py"
"""
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import httpx  # noqa: E402

import app  # noqa: E402,F401  (UTF-8 console setup)

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def show(label: str, response: httpx.Response, elapsed: float) -> bool:
    ok = response.status_code == 200
    print(f"[{'PASS' if ok else 'FAIL'}] {label} -> {response.status_code} ({elapsed:.2f}s)")
    return ok


def main() -> int:
    print(f"Testing API at {BASE_URL}\n")
    try:
        with httpx.Client(timeout=60) as client:
            outcomes = []

            t = time.perf_counter()
            r = client.get(f"{BASE_URL}/health")
            outcomes.append(show("GET /health", r, time.perf_counter() - t))
            print(f"       {r.json()}")

            t = time.perf_counter()
            r = client.get(f"{BASE_URL}/docs")
            outcomes.append(show("GET /docs (Swagger UI)", r, time.perf_counter() - t))

            t = time.perf_counter()
            r = client.post(f"{BASE_URL}/chat", json={"query": "What do customers say about the products?"})
            outcomes.append(show("POST /chat", r, time.perf_counter() - t))
            print(f"       {r.json()}")

            r = client.post(f"{BASE_URL}/chat", json={"query": ""})
            print(f"[{'PASS' if r.status_code == 422 else 'FAIL'}] POST /chat with empty query -> {r.status_code} (expected 422)")
            outcomes.append(r.status_code == 422)
    except httpx.ConnectError:
        print("[FAIL] Cannot connect. Start the server first:  uvicorn main:app --reload")
        return 1

    print("\nAll good." if all(outcomes) else "\nSome checks failed - see messages above and logs/app.log.")
    return 0 if all(outcomes) else 1


if __name__ == "__main__":
    sys.exit(main())
