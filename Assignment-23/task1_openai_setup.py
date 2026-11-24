"""
PART 1 - Task 1: OpenAI Setup & Basic Prompt

  1. Set up the OpenAI API key (in the .env file, never inside the code)
  2. Call an OpenAI chat model
  3. Send a simple prompt and print the response

The call is made twice, to show both ways of using OpenAI:
  A) the official `openai` Python SDK
  B) LangChain's ChatOpenAI  (this is what every other task uses)

Setup:  copy .env.example to .env and set OPENAI_API_KEY=...
Run:    python PART1_Getting_Started/task1_openai_setup.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from openai_models import OpenAINotConfigured, fail, fail_openai, get_llm, require_api_key

PROMPT = "Explain Retrieval-Augmented Generation (RAG) in two simple sentences."


def main():
    print("=" * 70)
    print("TASK 1: OPENAI SETUP & BASIC PROMPT")
    print("=" * 70)

    # ---- 1) API key ----
    try:
        key = require_api_key()
    except OpenAINotConfigured as error:
        fail(f"OpenAI is not set up.\n{error}")
    print(f"API key loaded from .env : yes ({len(key)} characters, hidden for safety)")
    print(f"Chat model               : {config.OPENAI_CHAT_MODEL}")
    print(f"Prompt                   : {PROMPT!r}")

    # ---- 2A) official OpenAI SDK ----
    print("\n--- A) Official OpenAI SDK ---")
    try:
        from openai import OpenAI

        client = OpenAI()                                   # reads OPENAI_API_KEY from the environment
        start = time.perf_counter()
        response = client.chat.completions.create(
            model=config.OPENAI_CHAT_MODEL,
            messages=[{"role": "user", "content": PROMPT}],
        )
        print(f"Response ({time.perf_counter() - start:.1f} s):")
        print(response.choices[0].message.content)
        usage = response.usage
        print(f"Tokens: prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")
    except Exception as error:
        fail_openai(error)

    # ---- 2B) LangChain ChatOpenAI ----
    print("\n--- B) LangChain ChatOpenAI ---")
    try:
        llm = get_llm()
        start = time.perf_counter()
        reply = llm.invoke(PROMPT)                          # returns an AIMessage
        print(f"Response ({time.perf_counter() - start:.1f} s):")
        print(reply.content)
        if reply.usage_metadata:
            print("Tokens:", reply.usage_metadata)

        # a system message controls the style of the answer
        reply = llm.invoke(
            [
                ("system", "You are a teacher. Answer in one short sentence for a beginner."),
                ("human", "What is a vector database?"),
            ]
        )
        print("\nWith a system message -> What is a vector database?")
        print(reply.content)
    except Exception as error:
        fail_openai(error)


if __name__ == "__main__":
    main()
