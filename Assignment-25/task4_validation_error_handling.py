"""
PART 2 - Task 4: Validation & Error Handling

  1. Handle invalid LLM outputs
  2. Retry or fall back when the schema is not followed

Part A  What can go wrong?        5 kinds of invalid output, caught by the Pydantic parser (no LLM needed)
Part B  The 4 protection layers   REPAIR, RETRY, FALLBACK, shown with a SIMULATED model that gives bad answers on
                                   purpose, so you can see exactly how each layer behaves (no LLM needed)
Part C  The robust chain, real    the same chain (structured.py) with your real LLM on the document questions

Run:  python PART2_Structured_Output/task4_validation_error_handling.py
"""

import itertools
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough

import ingestion
import models
from prompts import STRUCTURED_ANSWER_PROMPT
from schemas import Answer
from structured import structured_chain

GOOD = '{"answer": "Employees get 24 paid leave days.", "confidence": 0.9, "source": "company_handbook.pdf (page 2)"}'
SAFE_ANSWER = Answer(answer="I could not produce a valid answer. Please try again.", confidence=0.0, source="none")

INVALID_OUTPUTS = {
    "1. not JSON at all": "Sure! Employees get 24 paid leave days.",
    "2. JSON with a code fence": "```json\n" + GOOD + "\n```",
    "3. missing field": '{"answer": "24 days", "confidence": 0.9}',
    "4. wrong type": '{"answer": "24 days", "confidence": "very high", "source": "handbook"}',
    "5. value out of range": '{"answer": "24 days", "confidence": 1.7, "source": "handbook"}',
}


class CallCounter(BaseCallbackHandler):
    """Counts how many times the LLM was called."""

    def __init__(self):
        self.calls = 0

    def on_chat_model_start(self, *args, **kwargs):
        self.calls += 1


def run_chain(chain, inputs):
    counter = CallCounter()
    result = chain.invoke(inputs, config={"callbacks": [counter]})
    return result, counter.calls


def fake_llm(*texts, forever=False):
    """A simulated chat model that returns the given texts one after the other."""
    messages = [AIMessage(content=t) for t in texts]
    return GenericFakeChatModel(messages=itertools.cycle(messages) if forever else iter(messages))


def part_a():
    print("\n" + "=" * 70)
    print("PART A: WHAT CAN GO WRONG?  (PydanticOutputParser, no LLM)")
    print("=" * 70)
    parser = PydanticOutputParser(pydantic_object=Answer)
    for name, text in INVALID_OUTPUTS.items():
        try:
            result = parser.parse(text)
            print(f"  {name:<28} -> accepted: {result!r}")
        except Exception as error:
            reason = str(error).replace("\n", " ")
            reason = reason.split("For troubleshooting")[0].strip()
            print(f"  {name:<28} -> REJECTED ({type(error).__name__}): {reason[:105]}")
    print("\n  Note: the parser even accepts a ```json fence (case 2), but rejects everything that breaks the schema.")
    print("  Without handling, a rejected output would crash the program. The next part prevents that.")


def part_b():
    print("\n" + "=" * 70)
    print("PART B: THE PROTECTION LAYERS  (SIMULATED model, so every case is repeatable)")
    print("=" * 70)
    inputs = {"context": "[source: company_handbook.pdf (page 2)]\nEvery full-time employee receives twenty-four paid leave days.",
              "question": "How many paid leave days does an employee get?"}
    bad = INVALID_OUTPUTS["1. not JSON at all"]

    print("\n  Case 1 - valid output: no extra work needed")
    result, calls = run_chain(structured_chain(STRUCTURED_ANSWER_PROMPT, fake_llm(GOOD), Answer, repair=False), inputs)
    print(f"    model says: valid JSON   -> LLM calls: {calls}  result: {result.answer!r} (confidence {result.confidence})")

    print("\n  Case 2 - REPAIR: the 1st output is invalid, the LLM is asked to correct its own output")
    result, calls = run_chain(structured_chain(STRUCTURED_ANSWER_PROMPT, fake_llm(bad, GOOD), Answer, repair=True), inputs)
    print(f"    model says: text, then fixed JSON -> LLM calls: {calls}  result: {result.answer!r}")

    print("\n  Case 3 - RETRY: invalid twice, valid on the 3rd attempt (repair switched off to show the retries)")
    result, calls = run_chain(
        structured_chain(STRUCTURED_ANSWER_PROMPT, fake_llm(bad, INVALID_OUTPUTS["5. value out of range"], GOOD),
                         Answer, max_attempts=3, repair=False), inputs)
    print(f"    model says: bad, bad, valid JSON -> LLM calls: {calls}  result: {result.answer!r}")

    print("\n  Case 4 - FALLBACK: the model never follows the schema, a safe default is returned")
    result, calls = run_chain(
        structured_chain(STRUCTURED_ANSWER_PROMPT, fake_llm(bad, forever=True), Answer,
                         max_attempts=3, repair=True, fallback=SAFE_ANSWER), inputs)
    print(f"    model says: always invalid -> LLM calls: {calls} (3 attempts x [answer + repair])  result: {result!r}")

    print("\n  Case 5 - no fallback given: after all attempts the error is raised (the caller must handle it)")
    try:
        run_chain(structured_chain(STRUCTURED_ANSWER_PROMPT, fake_llm(bad, forever=True), Answer,
                                   max_attempts=2, repair=False), inputs)
    except Exception as error:
        print(f"    -> {type(error).__name__} raised after the retries")

    print("""
  Order of the layers in structured.py:   parse -> repair -> retry -> fallback
    parse    cheap, always on
    repair   one extra LLM call that only fixes the format (keeps the answer)
    retry    asks the whole question again (new answer, up to max_attempts)
    fallback never crash: return a default object with confidence 0.0""")


def part_c():
    print("\n" + "=" * 70)
    print(f"PART C: THE ROBUST CHAIN WITH THE REAL LLM ({models.provider_label()})")
    print("=" * 70)
    try:
        llm = models.get_llm()
        retriever = ingestion.get_retriever()
    except models.ModelNotConfigured as error:
        print(f"  skipped - no LLM available.\n  {str(error)}".replace("\n", "\n  "))
        return
    except Exception as error:
        models.fail_llm(error)

    chain = (
        {"context": retriever | ingestion.format_docs, "question": RunnablePassthrough()}
        | structured_chain(STRUCTURED_ANSWER_PROMPT, llm, Answer, max_attempts=3, repair=True, fallback=SAFE_ANSWER)
    )
    fell_back = 0
    try:
        for question in config.RAG_QUESTIONS:
            counter = CallCounter()
            result = chain.invoke(question, config={"callbacks": [counter]})
            used_fallback = result == SAFE_ANSWER
            fell_back += used_fallback
            print(f"\n  Q: {question}")
            print(f"     {result.model_dump_json()}")
            print(f"     LLM calls: {counter.calls}  ({'FALLBACK used' if used_fallback else 'valid Answer object'})")
    except Exception as error:
        models.fail_llm(error)
    print(f"\n  Result: every question returned a valid Answer object; fallback used {fell_back} time(s).")
    print("  More than one LLM call per question means the repair or retry layer had to step in.")


def main():
    print("=" * 70)
    print("TASK 4: VALIDATION & ERROR HANDLING")
    print("=" * 70)
    part_a()
    part_b()
    part_c()


if __name__ == "__main__":
    main()
