"""
PART 1 - Task 1: Ollama Setup & Basic Chat

  1. Install and run Ollama locally          -> the script checks that the server is running
  2. Pull a model (e.g. llama3, mistral)     -> the script checks the model (or pulls it with --pull)
  3. Use LangChain's Ollama LLM wrapper      -> langchain_ollama.OllamaLLM
  4. Send a simple prompt and print response
  5. Track the application using LangSmith   -> every call is recorded as a trace
  6. Screenshot of the LangSmith app         -> see SCREENSHOT_GUIDE.md (you take it, it needs your account)

Steps 1-2 are done by you outside Python (install Ollama, `ollama pull llama3`); this script verifies them.

Setup:  ollama pull llama3            (or: ollama pull mistral  and set OLLAMA_MODEL=mistral in .env)
        copy .env.example to .env and set LANGSMITH_API_KEY=...
Run:    python PART1_Getting_Started/task1_ollama_setup_chat.py
        python PART1_Getting_Started/task1_ollama_setup_chat.py --pull     (download the model if missing)
"""

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env

import langsmith_setup
from ollama_models import OllamaNotReady, ensure_model, check_server, fail, get_chat_model, get_llm, list_models

from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree


@traceable(name="task1_ollama_basic_chat", run_type="chain", tags=config.TRACE_TAGS,
           metadata={"assignment": 24, "task": 1, "model": config.OLLAMA_MODEL})
def basic_chat(prompt):
    """One traced run that contains: the OllamaLLM call and a ChatOllama call with a system message.

    Returns (run_id, llm_answer, chat_answer, seconds_llm). In LangSmith both model calls appear as
    child runs below 'task1_ollama_basic_chat'.
    """
    run = get_current_run_tree()
    run_id = str(run.id) if run is not None else None

    # ---- 3 + 4) LangChain Ollama LLM wrapper: text in -> text out
    llm = get_llm()
    start = time.perf_counter()
    answer = llm.invoke(prompt)
    seconds = time.perf_counter() - start

    # ---- bonus: the chat wrapper with a system message (its trace also shows token counts)
    chat = get_chat_model()
    reply = chat.invoke([("system", config.SYSTEM_PROMPT), ("human", config.SYSTEM_QUESTION)])
    return run_id, answer, reply, seconds


def main():
    parser = argparse.ArgumentParser(description="Ollama setup and basic chat")
    parser.add_argument("--pull", action="store_true", help="download the model if it is not pulled yet")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 1: OLLAMA SETUP & BASIC CHAT")
    print("=" * 70)

    # ---- 1) Ollama installed and running?
    print("\n[1] Ollama server")
    try:
        version = check_server()
    except OllamaNotReady as error:
        fail(f"Ollama is not ready.\n{error}")
    print(f"    running at {config.OLLAMA_BASE_URL}  (version {version})")

    # ---- 2) model pulled?
    print("\n[2] Model")
    try:
        ensure_model(pull=args.pull)
    except OllamaNotReady as error:
        fail(f"Model is not ready.\n{error}")
    print(f"    '{config.OLLAMA_MODEL}' is available.  Models on this computer: {', '.join(list_models())}")

    # ---- 5) LangSmith status (before the call, so tracing is known to be on)
    print("\n[5a] LangSmith tracking (switched on before the chat, so the chat is recorded)")
    print(f"    {langsmith_setup.describe()}")

    # ---- 3 + 4) the actual chat
    print("\n[3-4] LangChain OllamaLLM")
    print(f"    Prompt : {config.BASIC_PROMPT!r}")
    try:
        run_id, answer, reply, seconds = basic_chat(config.BASIC_PROMPT)
    except Exception as error:
        langsmith_setup.finish_and_report()
        fail(f"The Ollama request failed ({type(error).__name__}): {str(error)[:300]}\n"
             f"  -> Is the server still running and is '{config.OLLAMA_MODEL}' pulled?  (ollama list)")
    print(f"    Response ({seconds:.1f} s):")
    print("    " + answer.strip().replace("\n", "\n    "))

    print("\n    ChatOllama with a system message ->", config.SYSTEM_QUESTION)
    print("    " + reply.content.strip().replace("\n", "\n    "))
    if reply.usage_metadata:
        print(f"    Tokens: {reply.usage_metadata}")

    # ---- 5) send the traces and show where to find them
    if langsmith_setup.tracing_enabled():
        print("\n[5b] Traces sent to LangSmith")
        langsmith_setup.finish_and_report(run_id)

    # ---- 6) screenshot
    print("\n[6] Screenshot for the Drive upload")
    print("    Open https://smith.langchain.com -> Tracing -> project "
          f"'{config.LANGSMITH_PROJECT}' -> click the run 'task1_ollama_basic_chat'.")
    print("    What to capture is listed in SCREENSHOT_GUIDE.md. Save it in the 'screenshots' folder.")


if __name__ == "__main__":
    main()
