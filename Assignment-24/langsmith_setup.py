"""
langsmith_setup.py - LangSmith tracking (Task 1, step 5).

LangSmith records every LangChain call ("run"): input, output, model, time, tokens and errors, and shows them
as a trace in the web app https://smith.langchain.com. Tracing is controlled by environment variables that
config.py reads from .env:

    LANGSMITH_TRACING=true            (set automatically when a real LANGSMITH_API_KEY exists)
    LANGSMITH_API_KEY=...
    LANGSMITH_PROJECT=genai-assignment-24-ollama-chatbot
    LANGSMITH_ENDPOINT=...            (only for EU / self-hosted accounts)

    tracing_enabled()      -> True when tracing is switched on and a key exists
    describe()             -> text that explains the current state
    finish_and_report()    -> flushes the traces and prints the run id / project / link
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env

ENABLE_HELP = (
    "  To turn LangSmith tracking on:\n"
    "   1. Sign up (free) at https://smith.langchain.com\n"
    "   2. Settings -> API Keys -> Create API Key\n"
    "   3. Put it in .env:  LANGSMITH_API_KEY=...   (see .env.example), then run this task again"
)


def tracing_enabled():
    return bool(os.getenv("LANGSMITH_API_KEY")) and os.getenv("LANGSMITH_TRACING", "").lower() in ("true", "1", "yes")


def endpoint():
    return os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")


def describe():
    if tracing_enabled():
        return (f"ON  (project '{config.LANGSMITH_PROJECT}', endpoint {endpoint()}, key hidden)")
    return "OFF (no LANGSMITH_API_KEY found)\n" + ENABLE_HELP


def finish_and_report(run_id=None):
    """Send the pending traces to LangSmith and print where to find them. Never raises."""
    if not tracing_enabled():
        return
    try:
        from langchain_core.tracers.langchain import wait_for_all_tracers
        from langsmith import Client

        wait_for_all_tracers()                           # make sure the background upload has finished
        client = Client()
        client.flush()
    except Exception as error:
        print(f"  (could not send the traces to LangSmith: {type(error).__name__}: {str(error)[:200]})")
        print("   -> Check LANGSMITH_API_KEY, your internet connection and LANGSMITH_ENDPOINT.")
        return

    print(f"  Project : {config.LANGSMITH_PROJECT}")
    if run_id:
        print(f"  Run id  : {run_id}")
    # read the run back, to prove that LangSmith really received it (it can take a few seconds to appear)
    for _ in range(6):
        try:
            run = client.read_run(run_id) if run_id else None
        except Exception:
            run = None
        if run is not None:
            print(f"  Status  : {run.status}   |   child runs: {len(getattr(run, 'child_run_ids', None) or [])}")
            if getattr(run, "url", None):
                print(f"  Open the trace: {run.url}")
            return
        time.sleep(2)
    print("  Could not confirm that LangSmith received the trace.")
    print("   -> If LangSmith errors were printed above, check LANGSMITH_API_KEY and LANGSMITH_ENDPOINT")
    print("      (accounts in the EU region need LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com).")
    print(f"   -> Otherwise open https://smith.langchain.com -> Tracing -> '{config.LANGSMITH_PROJECT}' in a few seconds.")
