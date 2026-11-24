"""
PART 3 - Task 5: Simple Chain

  1. Create a basic chain:  Prompt -> Any LLM -> Output
  2. Execute the chain

    {"question": ...}  ->  ChatPromptTemplate  ->  LLM  ->  StrOutputParser  ->  text

The chain is written with the LCEL pipe operator (|). It is executed three ways:
invoke (one input), batch (several inputs at once) and stream (token by token).

Needs:  an LLM (OpenAI key or Ollama), see .env.example
Run:    python PART3_Chains/task5_simple_chain.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import StrOutputParser

import models
from prompts import DIRECT_PROMPT


def build_simple_chain(llm):
    """Prompt -> LLM -> Output parser."""
    return DIRECT_PROMPT | llm | StrOutputParser()


def main():
    print("=" * 70)
    print("TASK 5: SIMPLE CHAIN  (Prompt -> LLM -> Output)")
    print("=" * 70)
    try:
        llm = models.get_llm()
    except models.ModelNotConfigured as error:
        models.fail(f"No LLM available.\n{error}")

    chain = build_simple_chain(llm)
    print(f"\nLLM   : {models.provider_label()}")
    print("Chain : " + " | ".join(type(step).__name__ for step in (chain.first, *chain.middle, chain.last)))

    try:
        print("\n[1] invoke: one input")
        question = config.PROMPT_INPUTS[0]
        start = time.perf_counter()
        answer = chain.invoke({"question": question})
        print(f"    Q: {question}\n    A: {answer.strip()}\n    ({time.perf_counter() - start:.1f} s, the result is a plain string: {isinstance(answer, str)})")

        print("\n[2] batch: several inputs, run concurrently")
        questions = config.PROMPT_INPUTS[1:4]
        start = time.perf_counter()
        answers = chain.batch([{"question": q} for q in questions])
        for q, a in zip(questions, answers):
            print(f"    Q: {q}\n    A: {a.strip()}")
        print(f"    ({time.perf_counter() - start:.1f} s for {len(questions)} questions)")

        print("\n[3] stream: the answer appears piece by piece")
        print("    Q: " + config.PROMPT_INPUTS[4] + "\n    A: ", end="", flush=True)
        for piece in chain.stream({"question": config.PROMPT_INPUTS[4]}):
            print(piece, end="", flush=True)
        print()
    except Exception as error:
        models.fail_llm(error)

    print("\nThe same chain object supports invoke, batch and stream because every part of it is a Runnable.")


if __name__ == "__main__":
    main()
