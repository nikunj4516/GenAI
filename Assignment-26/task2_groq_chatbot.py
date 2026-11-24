"""Task 2: Build a Groq Chatbot (Core Logic).

  1. Function `groq_chat(prompt: str)` returns the model response
     (implemented in app/groq_service.py so the API reuses the exact same code).
  2. Handles system + user messages.
  3. Tested with multiple queries.

Run:  python "PART 1 — Getting Started with Groq API/task2_groq_chatbot.py"
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.groq_service import GroqServiceError, groq_chat  # noqa: E402

QUERIES = [
    "What is a Large Language Model? Answer in one sentence.",
    "Give me three tips for writing a clear product review.",
    "What is the difference between supervised and unsupervised learning?",
    "Translate 'Good quality, fast delivery' into Hindi.",
]


def main() -> int:
    print("=" * 70)
    print("TASK 2: Groq Chatbot - default system prompt")
    print("=" * 70)
    failures = 0
    for number, query in enumerate(QUERIES, start=1):
        print(f"\nQ{number}: {query}")
        try:
            print(f"A{number}: {groq_chat(query)}")
        except (GroqServiceError, ValueError) as exc:
            failures += 1
            print(f"[ERROR] {exc}")

    print("\n" + "=" * 70)
    print("Custom SYSTEM prompt (same question, different persona)")
    print("=" * 70)
    question = "Explain what an API is."
    personas = {
        "Pirate": "You are a pirate. Answer in one short sentence using pirate speech.",
        "Teacher": "You are a patient teacher explaining to a 10-year-old. Use one short sentence.",
    }
    for name, system_prompt in personas.items():
        print(f"\n[{name}] {question}")
        try:
            print(groq_chat(question, system_prompt=system_prompt))
        except (GroqServiceError, ValueError) as exc:
            failures += 1
            print(f"[ERROR] {exc}")

    print("\nInput validation: empty prompt")
    try:
        groq_chat("   ")
    except ValueError as exc:
        print(f"[OK] Rejected as expected: {exc}")

    print("\n[OK] Task 2 finished." if not failures else f"\n[WARN] {failures} call(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
