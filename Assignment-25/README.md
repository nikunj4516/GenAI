# GenAI Assignment 25 – Prompting & LangChain Chains

Prompt templates, structured output with Pydantic, chains (simple, conditional, parallel), Runnables and LCEL.
Only LangChain and Pydantic are used. The documents (Text, PDF and CSV from Assignments 21–22) are loaded,
split into chunks and stored in a **FAISS** vector store (`ingestion.py`).

## Folder structure

```
GenAI_Task(25)Nikunj/
├── data/                              notes.txt, company_handbook.pdf, Movie_recommendation.csv
├── PART1_Prompt_Templates/
│   ├── task1_prompt_template.py             Task 1  – PromptTemplate
│   └── task2_chat_prompt_template.py        Task 2  – ChatPromptTemplate + message templates
├── PART2_Structured_Output/
│   ├── task3_pydantic_output_schema.py      Task 3  – Answer schema + PydanticOutputParser
│   └── task4_validation_error_handling.py   Task 4  – validation, repair, retry, fallback
├── PART3_Chains/
│   ├── task5_simple_chain.py                Task 5  – Prompt | LLM | Parser
│   ├── task6_conditional_chain.py           Task 6  – RunnableBranch: retrieval vs direct LLM
│   └── task7_parallel_chain.py              Task 7  – answer + summary + follow-ups in parallel
├── PART4_Runnables_LCEL/
│   ├── task8_runnables_basics.py            Task 8  – Runnables, RunnablePassthrough, |
│   ├── task9_lcel_rag_chain.py              Task 9  – Retriever | Prompt | LLM | Parser
│   └── task10_observations_insights.md      Task 10 – written answers
├── config.py  models.py  ingestion.py  prompts.py  schemas.py  structured.py   (shared modules)
├── run_all.py   requirements.txt   .env.example   .gitignore
```

**Modular design:** each concern lives in one file. `models.py` creates the LLM / embeddings, `ingestion.py` the
vector store and retriever, `prompts.py` all shared prompts, `schemas.py` the Pydantic models, `structured.py` the
reusable "reliable structured output" chain. A task file only wires these pieces together.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # then edit .env
```

Choose the LLM in `.env` (**"any LLM"** is allowed by Task 5):

| `LLM_PROVIDER` | Needs | Default models |
|---|---|---|
| `openai` (default) | `OPENAI_API_KEY` | chat `gpt-6-luna`, embeddings `text-embedding-3-small` |
| `ollama` | Ollama running; `ollama pull llama3` and `ollama pull nomic-embed-text` | chat `llama3`, embeddings `nomic-embed-text` |

The first run that needs retrieval embeds the 412 chunks and saves the FAISS store in `vectorstores/`
(rebuilt automatically when the provider, model, chunk size or files change).

## Run

```bash
python run_all.py                                              # Tasks 1-9
python PART2_Structured_Output/task4_validation_error_handling.py   # any single task
python PART4_Runnables_LCEL/task9_lcel_rag_chain.py --question "How many sick days are there?"
```

Tasks 1, 2, 8 and parts A and B of Task 4 run **without any LLM** (formatting, parsing and the protection layers are
shown with a simulated model). The other tasks need the LLM and print a clear message if it is missing.

## Tasks

| Task | What it shows |
|---|---|
| 1 | `PromptTemplate` with a system instruction, `{question}` and a default `{level}`; 5 test inputs; missing-variable error. |
| 2 | `ChatPromptTemplate` from `SystemMessagePromptTemplate`, `HumanMessagePromptTemplate`, `AIMessagePromptTemplate` (few-shot example) and `MessagesPlaceholder` (history); comparison table with Task 1. |
| 3 | `Answer(answer, confidence, source)` (confidence checked to be 0–1). `PydanticOutputParser` + format instructions; RAG answers over the documents; each response is checked against the schema. Bonus: `with_structured_output`. |
| 4 | Part A: five kinds of invalid output. Part B: **parse → repair → retry → fallback** (`structured.py`), shown with a simulated model and an LLM-call counter. Part C: the robust chain with your real LLM. |
| 5 | `prompt \| llm \| StrOutputParser()` run with `invoke`, `batch` and `stream`. |
| 6 | An LLM router returns a validated `RouteDecision`; `RunnableBranch` sends **factual** questions through retrieval and everything else straight to the LLM. 6 test questions with expected routes. |
| 7 | `RunnableParallel` runs answer, summary and follow-up chains on the same retrieved context; outputs are combined into one report; parallel vs sequential timing. |
| 8 | `RunnableLambda`, `RunnablePassthrough` (and `.assign`), `\|`, `.pipe`, dict → `RunnableParallel`, `with_fallbacks`, `map`, async; composing chains from chains. |
| 9 | `{"context": retriever \| format_docs, "question": RunnablePassthrough()} \| prompt \| llm \| StrOutputParser()`; 6 queries (one not in the documents), a sources variant, streaming. |
| 10 | Short written answers in `task10_observations_insights.md`. |

### Design decisions

- **"Factual" (Task 6)** means: asks for specific information stored in *our* documents (policy, number, notes, movie
  details). General knowledge, advice and chat go to the direct LLM branch. If the router output is invalid, the
  repair / retry layers run, and a keyword rule decides as a last resort.
- **Answers only from the context (Tasks 3, 6, 7, 9):** if the documents do not contain the answer the chain says
  "I don't know based on the documents." (the last test question, *capital of France*, checks this).
- **Temperature:** not sent to OpenAI (some newer models reject it); `0` for Ollama.

## Testing notes (honest)

The code was run end to end in a sandbox **without** a real OpenAI key or Ollama, against a local stand-in for the
OpenAI API (embeddings, chat and streaming). That verified the wiring: loading, splitting, FAISS build/save/load,
every chain, the router, the parallel chain, schema validation, and the error messages (no key, wrong key, Ollama
not running, unknown provider). Task 4 Parts A and B and Tasks 1, 2 and 8 do not need a model and were verified
with their real output. Real answer quality, router accuracy and timings with a real model were **not** measured:
they will differ when you run it with your own key or Ollama.

## Troubleshooting

- **OPENAI_API_KEY is not set** → create `.env` from `.env.example` (or use `LLM_PROVIDER=ollama`).
- **Model not found / temperature error** → set `OPENAI_CHAT_MODEL` to a model your account can use, leave `OPENAI_TEMPERATURE` empty.
- **Ollama: cannot reach / model not pulled** → start Ollama, then `ollama pull llama3` and `ollama pull nomic-embed-text`.
- **Changed the provider and the answers look odd** → delete the `vectorstores/` folder (it is rebuilt automatically).
- **A small local model returns invalid JSON often** → Task 4's repair / retry / fallback layers handle it; use a larger model for best results.
