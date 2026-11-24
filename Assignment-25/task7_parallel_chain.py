"""
PART 3 - Task 7: Parallel Chain

  1. Run multiple chains in parallel: one generates the answer, one a summary, one follow-up questions
  2. Combine the outputs

                                         +-> answer chain     (RAG prompt)        -> text
    question -> retriever -> context ----+-> summary chain    (summary prompt)    -> text
                                         +-> follow-up chain  (structured: FollowUps) -> list of questions
                                                      |
                                                      +-> combine -> one report

RunnableParallel sends the same input to every chain at the same time. The three chains do not depend on each
other, so the total time is about the time of the slowest chain, not the sum of all three.

Needs:  an LLM (OpenAI key or Ollama), see .env.example
Run:    python PART3_Chains/task7_parallel_chain.py
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

import ingestion
import models
from prompts import FOLLOWUP_PROMPT, RAG_PROMPT, SUMMARY_PROMPT
from schemas import FollowUps
from structured import structured_chain

DEFAULT_FOLLOW_UPS = FollowUps(questions=["Can you give more details?", "Where can I read more about this?"])


def build_parallel_chain(llm, retriever):
    # the three independent chains
    answer_chain = RAG_PROMPT | llm | StrOutputParser()
    summary_chain = SUMMARY_PROMPT | llm | StrOutputParser()
    followup_chain = structured_chain(FOLLOWUP_PROMPT, llm, FollowUps, max_attempts=2, repair=True,
                                      fallback=DEFAULT_FOLLOW_UPS)
    parallel = RunnableParallel(answer=answer_chain, summary=summary_chain, follow_ups=followup_chain)

    # retrieve once, share the context with all three chains
    retrieve = RunnableParallel(docs=retriever, question=RunnablePassthrough()) | RunnablePassthrough.assign(
        context=lambda x: ingestion.format_docs(x["docs"])
    )

    # combine the outputs into one report
    combine = RunnableLambda(
        lambda x: {
            "answer": x["results"]["answer"].strip(),
            "summary": x["results"]["summary"].strip(),
            "follow_ups": x["results"]["follow_ups"].questions,
            "sources": x["sources"],
        },
        name="combine",
    )
    chain = retrieve | RunnableParallel(results=parallel, sources=lambda x: ingestion.source_names(x["docs"])) | combine
    return chain, (answer_chain, summary_chain, followup_chain), retrieve


def main():
    print("=" * 70)
    print("TASK 7: PARALLEL CHAIN  (answer + summary + follow-up questions)")
    print("=" * 70)
    try:
        llm = models.get_llm()
        retriever = ingestion.get_retriever()
    except models.ModelNotConfigured as error:
        models.fail(f"No LLM available.\n{error}")
    except Exception as error:
        models.fail_llm(error)

    chain, (answer_chain, summary_chain, followup_chain), retrieve = build_parallel_chain(llm, retriever)
    print(f"\nLLM: {models.provider_label()}   |   retrieve -> RunnableParallel(answer, summary, follow_ups) -> combine")

    try:
        for question in (config.PARALLEL_QUESTION, config.RAG_QUESTIONS[0]):
            start = time.perf_counter()
            report = chain.invoke(question)
            seconds = time.perf_counter() - start
            print(f"\nQuestion : {question}")
            print(f"Answer   : {report['answer']}")
            print(f"Summary  : {report['summary']}")
            print("Follow-up questions:")
            for q in report["follow_ups"]:
                print(f"   - {q}")
            print(f"Retrieved: {', '.join(report['sources'])}")
            print(f"Time     : {seconds:.1f} s")

        # ---- parallel vs sequential: the same three chains, run one after the other
        question = config.PARALLEL_QUESTION
        inputs = retrieve.invoke(question)
        start = time.perf_counter()
        RunnableParallel(a=answer_chain, s=summary_chain, f=followup_chain).invoke(inputs)
        parallel_time = time.perf_counter() - start
        start = time.perf_counter()
        answer_chain.invoke(inputs), summary_chain.invoke(inputs), followup_chain.invoke(inputs)
        sequential_time = time.perf_counter() - start
    except Exception as error:
        models.fail_llm(error)

    print("\n" + "=" * 70)
    print("PARALLEL vs SEQUENTIAL (same three chains, same input, retrieval excluded)")
    print("=" * 70)
    print(f"  parallel   : {parallel_time:.2f} s")
    print(f"  sequential : {sequential_time:.2f} s")
    if parallel_time > 0:
        print(f"  speed-up   : {sequential_time / parallel_time:.1f}x   (times depend on the model and your network)")


if __name__ == "__main__":
    main()
