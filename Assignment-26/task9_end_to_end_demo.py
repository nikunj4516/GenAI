"""Task 9: End-to-End Demo.

1. Calls POST /chat with different questions
2. Verifies: low latency, correct (grounded) answers, stable API behaviour

Start the server first (project root):  uvicorn main:app --reload
Run:  python "PART 5 — Mini Project Validation/task9_end_to_end_demo.py"

Optional env vars: API_BASE_URL (default http://127.0.0.1:8000),
                   LATENCY_THRESHOLD_SECONDS (default 5)
"""
import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import httpx  # noqa: E402

import app  # noqa: E402,F401  (UTF-8 console setup)
from app.prompts import NO_ANSWER_MESSAGE  # noqa: E402

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
LATENCY_THRESHOLD = float(os.getenv("LATENCY_THRESHOLD_SECONDS", "5"))

QUESTIONS = [
    "What do customers like most about the products?",
    "What are the most common complaints in the reviews?",
    "Which products have the best feedback?",
    "Summarize what reviewers say about quality and value for money.",
    "Are there any complaints about delivery, packaging or customer service?",
]
OUT_OF_SCOPE = "Who won the FIFA World Cup in 2018?"


def ask(client: httpx.Client, query: str) -> tuple[int, str, float]:
    started = time.perf_counter()
    r = client.post(f"{BASE_URL}/chat", json={"query": query})
    elapsed = time.perf_counter() - started
    try:
        body = r.json()
        text = body.get("answer") or body.get("detail") or ""
    except ValueError:
        text = r.text
    return r.status_code, text, elapsed


def main() -> int:
    print("=" * 70)
    print(f"TASK 9: End-to-End Demo against {BASE_URL}")
    print("=" * 70)
    checks: list[tuple[str, bool]] = []

    with httpx.Client(timeout=90) as client:
        try:
            health = client.get(f"{BASE_URL}/health").json()
        except httpx.ConnectError:
            print("[FAIL] Cannot connect. Start the server first:  uvicorn main:app --reload")
            return 1
        print(f"Health: {health}\n")

        ask(client, "Hello")  # warm-up call (excluded from latency stats)

        print("--- A. Different questions ---")
        latencies, statuses = [], []
        for number, question in enumerate(QUESTIONS, start=1):
            status, text, elapsed = ask(client, question)
            latencies.append(elapsed)
            statuses.append(status)
            print(f"\nQ{number}: {question}\n   status={status} | latency={elapsed:.2f}s\n   answer: {text[:300]}")

        print("\n--- B. Correctness: out-of-scope question must NOT be answered from outside knowledge ---")
        status, text, elapsed = ask(client, OUT_OF_SCOPE)
        refused = status == 200 and NO_ANSWER_MESSAGE.lower()[:40] in text.lower()
        print(f"Q: {OUT_OF_SCOPE}\n   status={status} | latency={elapsed:.2f}s\n   answer: {text[:300]}")
        if health.get("mode") == "chat":
            print("   (mode=chat: grounding check skipped)")
        else:
            checks.append(("out-of-scope question gets a grounded refusal", refused))

        print("\n--- C. Stability: same question x3, then 3 parallel requests ---")
        repeat = [ask(client, QUESTIONS[0]) for _ in range(3)]
        with ThreadPoolExecutor(max_workers=3) as pool:
            parallel = list(pool.map(lambda q: ask(client, q), QUESTIONS[:3]))
        repeat_ok = all(s == 200 for s, _, _ in repeat)
        parallel_ok = all(s == 200 for s, _, _ in parallel)
        print(f"repeat statuses  : {[s for s, _, _ in repeat]}")
        print(f"parallel statuses: {[s for s, _, _ in parallel]}")

        bad = client.post(f"{BASE_URL}/chat", json={"query": ""})
        print(f"invalid request  : {bad.status_code} (expected 422)")
        still_healthy = client.get(f"{BASE_URL}/health").status_code == 200

    avg = statistics.mean(latencies)
    p50 = statistics.median(latencies)
    worst = max(latencies)
    print("\n" + "=" * 70)
    print(f"Latency (s): avg={avg:.2f} | median={p50:.2f} | max={worst:.2f} | threshold={LATENCY_THRESHOLD:.1f}")
    print("=" * 70)

    checks += [
        ("all different questions returned HTTP 200", all(s == 200 for s in statuses)),
        (f"average latency under {LATENCY_THRESHOLD:.1f}s", avg < LATENCY_THRESHOLD),
        ("repeated requests are stable", repeat_ok),
        ("parallel requests are stable", parallel_ok),
        ("invalid input rejected with 422", bad.status_code == 422),
        ("API still healthy after all tests", still_healthy),
    ]
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("\nNote: answer correctness for in-scope questions should be read and judged manually above.")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
