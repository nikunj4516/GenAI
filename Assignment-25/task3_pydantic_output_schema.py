"""
PART 2 - Task 3: Pydantic Output Schema

  1. Define a Pydantic model for the chatbot response  -> schemas.Answer (answer, confidence, source)
  2. Use LangChain output parsers                       -> PydanticOutputParser
  3. Ensure the LLM output follows the schema           -> every response is validated and checked

The question is answered from the documents (Text + PDF + CSV in a FAISS store), so `source` can name the
file or movie that the answer came from.

    question -> retriever -> context -> prompt (with format instructions) -> LLM -> PydanticOutputParser -> Answer

Needs:  an LLM (OpenAI key or Ollama), see .env.example
Run:    python PART2_Structured_Output/task3_pydantic_output_schema.py
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough

import ingestion
import models
from prompts import STRUCTURED_ANSWER_PROMPT
from schemas import Answer


def main():
    print("=" * 70)
    print("TASK 3: PYDANTIC OUTPUT SCHEMA")
    print("=" * 70)

    # ---- 1) the schema
    print("\n[1] The Pydantic model (schemas.py)")
    print("    class Answer(BaseModel):  answer: str   confidence: float (0.0 - 1.0)   source: str")
    print("    JSON schema sent to the LLM:")
    print("      " + json.dumps(Answer.model_json_schema()["properties"], indent=2).replace("\n", "\n      "))

    # ---- 2) the parser
    parser = PydanticOutputParser(pydantic_object=Answer)
    print("\n[2] PydanticOutputParser: its format instructions are added to the prompt")
    print("    " + parser.get_format_instructions()[:230].replace("\n", " ") + " ...")

    print("\n    The parser also validates by itself (no LLM needed):")
    good = parser.parse('{"answer": "24 days", "confidence": 0.9, "source": "company_handbook.pdf (page 2)"}')
    print(f"      valid text   -> {good!r}")
    try:
        parser.parse('{"answer": "24 days", "confidence": 1.7, "source": "x"}')
    except Exception as error:
        print(f"      confidence 1.7 -> rejected ({type(error).__name__}): confidence must be <= 1")

    # ---- 3) the chain with the LLM
    print(f"\n[3] Chain with the LLM ({models.provider_label()})")
    try:
        llm = models.get_llm()
        retriever = ingestion.get_retriever()
    except models.ModelNotConfigured as error:
        models.fail(f"No LLM available.\n{error}")
    except Exception as error:
        models.fail_llm(error)

    chain = (
        {"context": retriever | ingestion.format_docs, "question": RunnablePassthrough()}
        | STRUCTURED_ANSWER_PROMPT.partial(format_instructions=parser.get_format_instructions())
        | llm
        | parser
    )

    valid = 0
    try:
        for i, question in enumerate(config.RAG_QUESTIONS, start=1):
            print(f"\nQ{i}: {question}")
            try:
                result = chain.invoke(question)
            except Exception as error:                       # parser error: the output did not follow the schema
                print(f"    INVALID output: {type(error).__name__}: {str(error).splitlines()[0][:130]}  (Task 4 repairs / retries this)")
                continue
            ok = isinstance(result, Answer) and 0.0 <= result.confidence <= 1.0 and bool(result.source)
            valid += ok
            print(f"    answer     : {result.answer}")
            print(f"    confidence : {result.confidence}")
            print(f"    source     : {result.source}")
            print(f"    schema check: {'PASS' if ok else 'FAIL'}  ({type(result).__name__}, "
                  f"as JSON: {result.model_dump_json()[:90]}...)")
    except Exception as error:
        models.fail_llm(error)

    print("\n" + "=" * 70)
    print(f"SUMMARY: {valid} / {len(config.RAG_QUESTIONS)} responses followed the schema on the first try")
    print("=" * 70)
    print("If a response does not follow the schema, Task 4 shows how to repair, retry or fall back.")

    # ---- bonus: the provider's own structured-output feature
    print("\nBonus: llm.with_structured_output(Answer) uses the model's native JSON/tool mode instead of text parsing")
    try:
        context = ingestion.format_docs(retriever.invoke(config.RAG_QUESTIONS[0]))
        native = llm.with_structured_output(Answer).invoke(
            STRUCTURED_ANSWER_PROMPT.partial(format_instructions="").format_messages(
                context=context, question=config.RAG_QUESTIONS[0])
        )
        print(f"    -> {native!r}")
    except Exception as error:
        print(f"    (not available for this model: {type(error).__name__}: {str(error)[:120]})")


if __name__ == "__main__":
    main()
