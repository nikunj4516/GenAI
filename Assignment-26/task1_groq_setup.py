"""Task 1: Groq API Setup & Basic Chat.

Steps covered
  1. Create a Groq account + API key  -> https://console.groq.com/keys
  2. Install the Groq SDK             -> pip install groq   (already in requirements.txt)
  3. Call a Groq LLM
  4. Send a simple prompt and print the response

Run:  python "PART 1 — Getting Started with Groq API/task1_groq_setup.py"
"""
import sys
from importlib.metadata import version
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import groq  # noqa: E402

from app import config  # noqa: E402


def main() -> int:
    print("=" * 70)
    print("TASK 1: Groq API Setup & Basic Chat")
    print("=" * 70)

    print(f"[1] Groq SDK installed, version: {version('groq')}")

    if not config.GROQ_API_KEY:
        print("[FAIL] GROQ_API_KEY not found.")
        print("       1) Create a key at https://console.groq.com/keys")
        print("       2) Copy .env.example to .env and set GROQ_API_KEY=<your key>")
        return 1
    masked = f"{config.GROQ_API_KEY[:4]}...{config.GROQ_API_KEY[-4:]}"
    print(f"[2] API key loaded from environment: {masked}")
    print(f"[3] Model: {config.GROQ_MODEL}")

    client = groq.Groq(api_key=config.GROQ_API_KEY)
    prompt = "In two sentences, explain why fast LLM inference matters for real-time applications."

    request = {
        "model": config.GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": config.LLM_MAX_TOKENS,
    }
    if config.GROQ_MODEL.startswith("openai/gpt-oss"):
        request["extra_body"] = {"reasoning_effort": config.GROQ_REASONING_EFFORT}

    print(f"\nPrompt  : {prompt}")
    try:
        response = client.chat.completions.create(**request)
    except groq.GroqError as exc:
        print(f"[FAIL] Groq call failed: {exc}")
        return 1

    print(f"Response: {response.choices[0].message.content}")
    print("\n[OK] Groq API setup verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
