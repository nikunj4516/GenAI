# Assignment 26: Groq API Chatbot, RAG & FastAPI Serving

A low-latency GenAI backend built with the **Groq API**, a **FAISS-based RAG pipeline** over `product_reviews_dataset.csv`, and a **FastAPI** service (`/health`, `/chat`).

---

## Project Structure

```
GenAI/
├── product_reviews_dataset.csv          <- dataset (here, or inside the project folder)
└── GenAI_Task(26)Nikunj/
    ├── PART 1 — Getting Started with Groq API/
    │   ├── task1_groq_setup.py
    │   └── task2_groq_chatbot.py
    ├── PART 2 — Groq + RAG/
    │   ├── task3_groq_rag_pipeline.py
    │   └── task4_prompt_template.py
    ├── PART 3 — Building API using FastAPI/
    │   ├── task5_fastapi_app.py
    │   └── task6_fastapi_groq_integration.py
    ├── PART 4 — Serving the Groq App/
    │   ├── task7_run_and_test_api.py
    │   └── task8_production_readiness_check.py
    ├── PART 5 — Mini Project Validation/
    │   ├── task9_end_to_end_demo.py
    │   └── task10_Observations_and_Insights.md
    ├── app/                         <- shared core code used by every task + the API
    │   ├── config.py                (env vars, dataset lookup)
    │   ├── logger.py                (console + logs/app.log)
    │   ├── prompts.py               (RAG prompt template)
    │   ├── groq_service.py          (Groq client, groq_chat, error mapping)
    │   ├── rag_service.py           (load -> chunk -> embed -> FAISS -> retrieve -> answer)
    │   ├── chat_service.py          (routes a question to RAG or plain chat)
    │   └── schemas.py               (Pydantic models)
    ├── main.py                      <- FastAPI app (Task 5 & 6)
    ├── requirements.txt             <- Task 8
    ├── .env.example                 <- copy to .env and add your key
    ├── .gitignore
    └── README.md
```

`logs/` and `vectorstore/` are created automatically on first run.

---

## Setup

```bash
# 1. Activate your virtual environment (the existing GenAI/.venv works)
#    Windows PowerShell:  ..\.venv\Scripts\Activate.ps1
#    macOS/Linux:         source ../.venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key  (get one at https://console.groq.com/keys)
copy .env.example .env        # Windows
cp .env.example .env          # macOS/Linux
#    then edit .env:  GROQ_API_KEY=your_real_key
```

The dataset is found automatically in the project folder, its parent folder (`GenAI/`), or the path given in `DATASET_PATH`.

> **Model note:** `llama-3.3-70b-versatile` and `llama-3.1-8b-instant` were retired by Groq on **16 Aug 2026**. This project defaults to **`openai/gpt-oss-120b`**. You can change it with `GROQ_MODEL` in `.env`; list the currently available models at https://console.groq.com/docs/models.

---

## Run the Tasks (from the project folder)

| Task | Command |
|------|---------|
| 1 | `python "PART 1 — Getting Started with Groq API/task1_groq_setup.py"` |
| 2 | `python "PART 1 — Getting Started with Groq API/task2_groq_chatbot.py"` |
| 3 | `python "PART 2 — Groq + RAG/task3_groq_rag_pipeline.py"` |
| 4 | `python "PART 2 — Groq + RAG/task4_prompt_template.py"` |
| 5 | `python "PART 3 — Building API using FastAPI/task5_fastapi_app.py"` |
| 6 | `python "PART 3 — Building API using FastAPI/task6_fastapi_groq_integration.py"` |
| 7 | start the server, then `python "PART 4 — Serving the Groq App/task7_run_and_test_api.py"` |
| 8 | `python "PART 4 — Serving the Groq App/task8_production_readiness_check.py"` |
| 9 | start the server, then `python "PART 5 — Mini Project Validation/task9_end_to_end_demo.py"` |
| 10 | read `PART 5 — Mini Project Validation/task10_Observations_and_Insights.md` |

The first RAG run downloads the embedding model (about 90 MB) and builds the FAISS index; later runs load it from `vectorstore/`. The index rebuilds automatically if the CSV or chunk settings change.

---

## Run the API (Task 7)

```bash
uvicorn main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### `GET /health`

```json
{"status": "ok", "model": "openai/gpt-oss-120b", "mode": "rag", "rag_ready": true, "groq_key_configured": true}
```

### `POST /chat`

Request:
```json
{"query": "What do customers say about the products?"}
```
Response:
```json
{"answer": "model response"}
```

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" \
     -d "{\"query\": \"What do customers say about the products?\"}"
```

### Error responses (JSON `{"detail": "..."}`)

| Status | When |
|--------|------|
| 422 | Invalid body (missing/empty/too long/non-string `query`) |
| 429 | Groq rate limit reached |
| 503 | Missing/invalid API key, Groq unreachable, or dataset unavailable |
| 504 | Groq request timed out |
| 502 | Other Groq errors (for example the configured model was retired) |
| 500 | Unexpected error (details are logged, not exposed) |

---

## Configuration (`.env`)

| Variable | Default | Purpose |
|----------|---------|---------|
| `GROQ_API_KEY` | (required) | Groq API key |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | Model used for answers |
| `GROQ_REASONING_EFFORT` | `low` | Used only for `openai/gpt-oss-*` models (`low`/`medium`/`high`) |
| `CHAT_MODE` | `rag` | `rag` = answers grounded in the CSV, `chat` = plain Groq chatbot |
| `LLM_TEMPERATURE` | `0.2` | Sampling temperature (RAG uses 0.1) |
| `LLM_MAX_TOKENS` | `1024` | Max completion tokens (keep generous for reasoning models) |
| `TOP_K` | `5` | Chunks retrieved per question |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `500` / `50` | Characters per chunk / overlap |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `DATASET_PATH` | auto-detected | Explicit CSV location |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## How It Works

1. **Load:** every CSV row becomes a document of `column: value` pairs (works with any column layout).
2. **Split:** documents are cut into 500-character chunks with 50-character overlap, without breaking words.
3. **Embed + store:** `all-MiniLM-L6-v2` embeddings (normalised) go into a FAISS `IndexFlatIP`, saved to `vectorstore/`.
4. **Retrieve:** the top-k chunks for the question are fetched.
5. **Prompt:** system rules + numbered context + question (see `app/prompts.py`). The model must answer only from context and otherwise say it does not have enough information.
6. **Generate:** the prompt goes to Groq; the answer is returned as `{"answer": ...}`.

## Troubleshooting

- **`GROQ_API_KEY is not set`:** create `.env` from `.env.example`.
- **HTTP 502 mentioning the model:** your `GROQ_MODEL` may have been retired. Pick a current one from the Groq models page.
- **Empty response error:** increase `LLM_MAX_TOKENS` (reasoning models use part of the budget for thinking).
- **Dataset not found:** keep `product_reviews_dataset.csv` in the project folder or in `GenAI/`, or set `DATASET_PATH`.
- **Changed the CSV but answers look old:** delete the `vectorstore/` folder (it normally rebuilds on its own).
