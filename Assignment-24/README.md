# GenAI Assignment 24 – Ollama Chatbot

A local LLM (Ollama) used through LangChain and tracked with LangSmith.
This folder contains **Task 1: Ollama Setup & Basic Chat**. The other tasks of the assignment will be added
in the same structure.

## Folder structure

```
GenAI_Task(24)Nikunj/
├── PART1_Getting_Started/
│   └── task1_ollama_setup_chat.py     Task 1 – Ollama setup, LangChain OllamaLLM, LangSmith tracking
├── screenshots/                       put your LangSmith screenshot here (step 6)
├── SCREENSHOT_GUIDE.md                exactly what the screenshot must show
├── config.py                          settings (.env loader, model name, LangSmith project)
├── ollama_models.py                   server/model checks, pull, OllamaLLM + ChatOllama
├── langsmith_setup.py                 LangSmith status and trace report
├── run_all.py   requirements.txt   .env.example   .gitignore
```

## Setup

1. **Install Ollama** – <https://ollama.com/download> (or `curl -fsSL https://ollama.com/install.sh | sh` on Linux).
   The desktop app starts the server; otherwise run `ollama serve`.
2. **Pull a model** – `ollama pull llama3` (about 4.7 GB) or `ollama pull mistral`.
   Smaller option for weak computers: `ollama pull llama3.2` and set `OLLAMA_MODEL=llama3.2` in `.env`.
3. **Python packages** – `pip install -r requirements.txt`
4. **LangSmith key** – free account at <https://smith.langchain.com> → Settings → API Keys.
   `cp .env.example .env` and set `LANGSMITH_API_KEY=...` (never commit `.env`).

## Run

```bash
python PART1_Getting_Started/task1_ollama_setup_chat.py
python PART1_Getting_Started/task1_ollama_setup_chat.py --pull    # downloads the model if missing
python run_all.py
```

## Task 1 – step by step

| Step | Requirement | How it is done |
|---|---|---|
| 1 | Install and run Ollama locally | you install it; the script checks `GET /api/version` and explains what to do if it is not running |
| 2 | Pull a model | you run `ollama pull llama3`; the script verifies it (or pulls it with `--pull`) |
| 3 | LangChain's Ollama LLM wrapper | `langchain_ollama.OllamaLLM` (plus `ChatOllama` as a bonus with a system message) |
| 4 | Send a simple prompt, print the response | prompt from `config.py`; response and timing are printed |
| 5 | Track with LangSmith | the call runs inside a `@traceable` run `task1_ollama_basic_chat` (tags, metadata); the model calls appear as child runs; traces are flushed and read back to confirm |
| 6 | Screenshot in Drive | taken by you from your LangSmith account – see `SCREENSHOT_GUIDE.md` |

Without a LangSmith key the chat still works and the script says how to turn tracking on.

## Testing notes (honest)

The code was run in a sandbox that has **no real Ollama, no GPU and no LangSmith account**, using local stand-in
servers for the Ollama HTTP API and the LangSmith API. This verified the wiring: server/model checks, `--pull`,
`OllamaLLM` and `ChatOllama` calls, the trace with its two child runs being sent and read back, and the error
messages (server down, model missing, LangSmith unreachable). It did **not** verify real model answers, real
speed, or the LangSmith web page – and the screenshot can only come from you.

## Troubleshooting

- **Cannot reach the Ollama server** → start the app or `ollama serve`; check `OLLAMA_BASE_URL`.
- **Model not pulled** → `ollama pull llama3` (the name must match `OLLAMA_MODEL`; see `ollama list`).
- **First answer is slow** → the model is loaded into memory; later answers are faster.
- **No trace in LangSmith** → check the key, the region (`LANGSMITH_ENDPOINT` for EU) and the project name.
