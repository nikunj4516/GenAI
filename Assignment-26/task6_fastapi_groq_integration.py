"""Task 6: FastAPI + Groq Integration - verification.

  1. /chat calls the Groq chatbot / RAG logic
  2. Errors are handled gracefully (clean JSON, correct status, no stack traces)
  3. Requests are validated with Pydantic models

Run:  python "PART 3 — Building API using FastAPI/task6_fastapi_groq_integration.py"
"""
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from app import config  # noqa: E402
from app.groq_service import GroqServiceError  # noqa: E402
from app.rag_service import RAGError  # noqa: E402

results: list[bool] = []


def check(name: str, condition: bool) -> None:
    results.append(condition)
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")


def run() -> int:
    print(f"Mode: {config.CHAT_MODE} | Model: {config.GROQ_MODEL}\n")

    print("--- 1. Real integration: /chat -> RAG/Groq ---")
    with TestClient(main.app) as client:  # `with` runs the startup warm-up
        r = client.post("/chat", json={"query": "What do customers say about the products?"})
        if config.GROQ_API_KEY:
            check("POST /chat with real pipeline -> 200", r.status_code == 200)
            answer = r.json().get("answer", "")
            check("answer is a non-empty string", isinstance(answer, str) and bool(answer.strip()))
            print(f"       answer preview: {answer[:150]!r}")
        else:
            print("       (GROQ_API_KEY not set - verifying graceful failure instead)")
            check("missing key/dataset -> clean 503, not a crash", r.status_code == 503)
            print(f"       detail: {r.json().get('detail')}")

        print("\n--- 2. Graceful error handling (simulated failures) ---")
        with patch.object(main, "generate_answer", side_effect=GroqServiceError("Groq rate limit reached.", 429)):
            r = client.post("/chat", json={"query": "hello"})
        check("Groq rate limit -> 429 with JSON detail", r.status_code == 429 and "detail" in r.json())

        with patch.object(main, "generate_answer", side_effect=GroqServiceError("Could not connect to Groq.", 503)):
            r = client.post("/chat", json={"query": "hello"})
        check("Groq unreachable -> 503 with JSON detail", r.status_code == 503 and "detail" in r.json())

        with patch.object(main, "generate_answer", side_effect=RAGError("dataset missing")):
            r = client.post("/chat", json={"query": "hello"})
        check("RAG failure -> 503 with JSON detail", r.status_code == 503 and "detail" in r.json())

        with patch.object(main, "generate_answer", side_effect=RuntimeError("secret internal boom")):
            r = client.post("/chat", json={"query": "hello"})
        check("Unexpected error -> 500", r.status_code == 500)
        check("500 response does not leak internal error text", "boom" not in r.text)

        print("\n--- 3. Pydantic request validation ---")
        check("empty query -> 422", client.post("/chat", json={"query": ""}).status_code == 422)
        check("missing query -> 422", client.post("/chat", json={}).status_code == 422)
        check("wrong type -> 422", client.post("/chat", json={"query": ["a"]}).status_code == 422)

    passed = sum(results)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(run())
