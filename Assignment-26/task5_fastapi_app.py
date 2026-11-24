"""Task 5: Create FastAPI Application - verification.

The application itself is main.py (project root). This script checks, without
calling Groq, that:
  - GET  /health works
  - POST /chat accepts {"query": "..."} and returns exactly {"answer": "..."}
  - invalid bodies are rejected with HTTP 422

Run:  python "PART 3 — Building API using FastAPI/task5_fastapi_app.py"
"""
import sys
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

results: list[bool] = []


def check(name: str, condition: bool) -> None:
    results.append(condition)
    print(f"[{'PASS' if condition else 'FAIL'}] {name}")


def run() -> int:
    # No `with` block -> startup warm-up is skipped, so this test needs no dataset or API key.
    client = TestClient(main.app)

    print("Registered routes:", sorted({r.path for r in main.app.routes if hasattr(r, "methods")}))
    print()

    r = client.get("/health")
    check("GET /health -> 200", r.status_code == 200)
    check('GET /health body has status == "ok"', r.json().get("status") == "ok")

    with patch.object(main, "generate_answer", return_value="stub answer"):
        r = client.post("/chat", json={"query": "Your question here"})
    check("POST /chat valid body -> 200", r.status_code == 200)
    check('POST /chat response is exactly {"answer": "..."}', r.json() == {"answer": "stub answer"})

    invalid_bodies = {
        "missing body": None,
        "empty object": {},
        "empty query": {"query": ""},
        "whitespace-only query": {"query": "    "},
        "wrong key name": {"question": "hi"},
        "non-string query": {"query": 123},
        "query too long (2001 chars)": {"query": "x" * 2001},
    }
    for label, body in invalid_bodies.items():
        r = client.post("/chat", json=body) if body is not None else client.post("/chat")
        check(f"POST /chat {label} -> 422", r.status_code == 422)

    check("GET /docs (Swagger UI) -> 200", client.get("/docs").status_code == 200)

    passed = sum(results)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(run())
