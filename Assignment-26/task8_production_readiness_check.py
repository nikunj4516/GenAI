"""Task 8: Production Readiness (Basic).

Verifies:
  1. requirements.txt exists and lists every needed package
  2. API keys are read from environment variables (no hard-coded secrets)
  3. Basic logging works (logs/app.log)
  4. .env is git-ignored

Run:  python "PART 4 — Serving the Groq App/task8_production_readiness_check.py"
"""
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import config  # noqa: E402
from app.logger import get_logger  # noqa: E402

results: list[bool] = []


def check(name: str, condition: bool, hint: str = "") -> None:
    results.append(condition)
    print(f"[{'PASS' if condition else 'FAIL'}] {name}" + (f"  -> {hint}" if hint and not condition else ""))


def main() -> int:
    print("=" * 70)
    print("TASK 8: Production Readiness Check")
    print("=" * 70)

    # 1. requirements.txt
    req_file = PROJECT_ROOT / "requirements.txt"
    check("requirements.txt exists", req_file.is_file())
    if req_file.is_file():
        names = {
            re.split(r"[<>=!~\[]", line.strip(), maxsplit=1)[0].lower()
            for line in req_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
        for pkg in ("groq", "fastapi", "uvicorn", "pydantic", "faiss-cpu", "sentence-transformers", "python-dotenv"):
            check(f"requirements.txt lists '{pkg}'", pkg in names)

    # 2. secrets
    check("GROQ_API_KEY is available from environment / .env", bool(config.GROQ_API_KEY), "copy .env.example to .env and set the key")
    leaked = [
        str(p.relative_to(PROJECT_ROOT))
        for p in PROJECT_ROOT.rglob("*.py")
        if ".venv" not in p.parts and re.search(r"gsk_[A-Za-z0-9]{20,}", p.read_text(encoding="utf-8", errors="ignore"))
    ]
    check("no hard-coded Groq keys in any .py file", not leaked, f"found in: {leaked}")

    gitignore = PROJECT_ROOT / ".gitignore"
    ignored = gitignore.is_file() and any(l.strip() == ".env" for l in gitignore.read_text(encoding="utf-8").splitlines())
    check(".env is listed in .gitignore", ignored)
    check(".env.example exists (safe template)", (PROJECT_ROOT / ".env.example").is_file())

    # 3. logging
    marker = "task8 logging check"
    get_logger("task8").info(marker)
    log_file = config.LOG_DIR / "app.log"
    check("logs/app.log is written", log_file.is_file() and marker in log_file.read_text(encoding="utf-8", errors="ignore"))

    passed = sum(results)
    print(f"\n{passed}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
