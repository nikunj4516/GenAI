# Task 10: Observations & Insights

Short answers, written from what the code of Tasks 1-9 does.

## 1. Why is structured output important?

An LLM returns text, but a program needs data. A reply such as "about 24 days, I think" cannot be put in a
database, compared with a threshold or shown in a table without guessing. With a Pydantic schema
(`Answer`: `answer`, `confidence`, `source`) the reply becomes an object with known fields and types.

- **Reliable code:** `result.confidence` is always a float between 0 and 1. The code does not need string tricks.
- **Validation:** a wrong type, a missing field or `confidence = 1.7` is rejected right away (Task 4, Part A).
- **Error handling:** because the failure is a clear exception, it can be repaired, retried or replaced by a safe
  default (Task 4, Part B) instead of crashing or silently passing a bad value on.
- **Trust and traceability:** the `source` and `confidence` fields let a user or a later step decide whether to
  believe the answer.
- **Composition:** the output of one chain can be the input of the next (Task 6: the router's `RouteDecision`
  decides which branch runs).

Limit: a schema guarantees the *shape* of the output, not that the content is true. The answer still has to
be grounded in the retrieved context.

## 2. Advantages of LCEL over traditional chains

LCEL (the `|` syntax) builds a chain from Runnables; "traditional" chains are fixed classes such as `LLMChain`
or `RetrievalQA` with their own parameters.

| LCEL | Traditional chain classes |
|---|---|
| Every step is a Runnable, so any step can be replaced (a different LLM, retriever or parser) | The structure is fixed inside the class |
| `invoke`, `batch`, `stream` and async (`ainvoke`) work on the whole chain without extra code | Streaming and async are limited or have to be added |
| `RunnableParallel` runs independent steps at the same time (Task 7) | Steps run one after the other |
| `with_retry` and `with_fallbacks` can be added to any step (Task 4) | Error handling is custom code |
| The data flow is visible in one readable line: `retriever \| prompt \| llm \| parser` (Task 9) | The flow is hidden in the class |
| Every step is traced as its own run (LangSmith), which makes debugging easy | Harder to see what happened inside |
| This is the current style of LangChain; many old chain classes are deprecated | Older style |

## 3. When to use parallel vs conditional chains?

**Parallel chain** (`RunnableParallel`): use it when several tasks are *independent* and *all* of them are needed.
Every branch gets the same input and all of them run. Example (Task 7): answer, summary and follow-up questions
for the same retrieved context. The waiting time is about that of the slowest branch, but the cost is the sum of
all branches.

**Conditional chain** (`RunnableBranch` or a router): use it when the input decides *which one* path is needed.
Only one branch runs. Example (Task 6): a factual question goes through retrieval, a greeting goes straight to the
LLM. It saves cost and time, because unneeded steps (retrieval, long context) are skipped, and it avoids wrong
answers such as forcing retrieval for small talk.

| | Parallel | Conditional |
|---|---|---|
| Question it answers | "What do I need to do with this input?" (all of it) | "Which way should this input go?" (one way) |
| Branches that run | all | one |
| Main benefit | speed for independent work | saving cost, choosing the right tool |
| Main risk | cost of all branches | a wrong routing decision |

They can be combined: a router chooses the path, and one branch can itself be a parallel chain.
