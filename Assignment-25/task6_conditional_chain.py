"""
PART 3 - Task 6: Conditional Chain

  1. A chain that uses retrieval if the question is factual, and a direct LLM response otherwise
  2. The conditional logic is implemented with RunnableBranch

"Factual" here means: the question asks for specific information that is stored in OUR documents
(a company policy, a number, a definition from the notes, details of a movie). Greetings, advice,
opinions and creative requests are "general" and do not need retrieval.

    question -> ROUTER (LLM -> RouteDecision) -+-> factual -> retriever -> context -> LLM -> answer + sources
                                               +-> general -> LLM -> answer

If the router's output cannot be parsed, a simple keyword rule decides (so the chain never crashes).

Needs:  an LLM (OpenAI key or Ollama), see .env.example
Run:    python PART3_Chains/task6_conditional_chain.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough

import ingestion
import models
from prompts import DIRECT_PROMPT, RAG_PROMPT, ROUTER_PROMPT
from schemas import RouteDecision
from structured import structured_chain

FACT_WORDS = re.compile(r"\b(how many|how long|how much|what is|what are|which|who|when|where|policy|rule|days|movie|film|plot)\b", re.I)
FALLBACK_ROUTE = RouteDecision(route="general", reason="router output could not be parsed (keyword rule used)")


def keyword_route(question):
    """Last-resort rule when the LLM router fails."""
    kind = "factual" if FACT_WORDS.search(question) else "general"
    return RouteDecision(route=kind, reason="keyword rule (router output was invalid)")


def build_conditional_chain(llm, retriever):
    # 1) router: question -> RouteDecision (validated by Pydantic, with repair / retry from structured.py)
    router = structured_chain(ROUTER_PROMPT, llm, RouteDecision, max_attempts=2, repair=True, fallback=FALLBACK_ROUTE)

    # 2) the two branches; both return the same dictionary shape
    rag_branch = (
        RunnablePassthrough.assign(docs=lambda x: retriever.invoke(x["question"]))
        | RunnablePassthrough.assign(
            answer=(lambda x: {"context": ingestion.format_docs(x["docs"]), "question": x["question"]})
            | RAG_PROMPT | llm | StrOutputParser(),
            sources=lambda x: ingestion.source_names(x["docs"]),
        )
        | RunnableLambda(lambda x: {"route": "factual", "answer": x["answer"].strip(), "sources": x["sources"]})
    )
    direct_branch = (
        DIRECT_PROMPT | llm | StrOutputParser()
        | RunnableLambda(lambda text: {"route": "general", "answer": text.strip(), "sources": []})
    )

    # 3) the condition: RunnableBranch((condition, runnable), ..., default)
    branch = RunnableBranch(
        (lambda x: x["decision"].route == "factual", rag_branch),
        direct_branch,                                                        # default branch
    )
    # decide first (keep the decision next to the question), then branch on it
    decide = RunnablePassthrough.assign(
        decision=RunnableLambda(lambda x: {"question": x["question"]}) | router
    )
    return decide | RunnablePassthrough.assign(result=branch)


def main():
    print("=" * 70)
    print("TASK 6: CONDITIONAL CHAIN  (retrieval for factual questions, direct LLM otherwise)")
    print("=" * 70)
    try:
        llm = models.get_llm()
        retriever = ingestion.get_retriever()
    except models.ModelNotConfigured as error:
        models.fail(f"No LLM available.\n{error}")
    except Exception as error:
        models.fail_llm(error)

    chain = build_conditional_chain(llm, retriever)
    print(f"\nLLM: {models.provider_label()}   |   router -> RunnableBranch(factual: RAG, default: direct LLM)")

    matched = 0
    try:
        for question, expected in config.ROUTING_QUESTIONS:
            out = chain.invoke({"question": question})
            decision, result = out["decision"], out["result"]
            ok = decision.route == expected
            matched += ok
            print(f"\nQ: {question}")
            print(f"   router  : {decision.route}   (expected: {expected} -> {'OK' if ok else 'DIFFERENT'})   reason: {decision.reason}")
            print(f"   path    : {'retriever -> context -> LLM' if result['route'] == 'factual' else 'direct LLM (no retrieval)'}")
            print(f"   answer  : {result['answer']}")
            if result["sources"]:
                print(f"   sources : {', '.join(result['sources'])}")
    except Exception as error:
        models.fail_llm(error)

    print("\n" + "=" * 70)
    print(f"SUMMARY: the router chose the expected path for {matched} / {len(config.ROUTING_QUESTIONS)} questions")
    print("=" * 70)
    print("The router is an LLM decision, so it can differ from the expectation; the reason it gives is printed.")


if __name__ == "__main__":
    main()
