# Task 6 (setup): Install and run Ollama locally

Ollama runs open models on your own computer. For this assignment we use the embedding model **`nomic-embed-text`** (768 dimensions).

## Steps

1. **Install Ollama**
   - Windows / macOS: download the installer from https://ollama.com/download and run it.
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
2. **Make sure Ollama is running.** The desktop app starts it automatically. Otherwise, open a terminal and run:
   ```bash
   ollama serve
   ```
   Ollama listens on `http://localhost:11434`.
3. **Download the embedding model** (one time, about 270 MB):
   ```bash
   ollama pull nomic-embed-text
   ```
4. **Check that it is installed:**
   ```bash
   ollama list
   ```
   `nomic-embed-text` must appear in the list.
5. **Install the LangChain integration** (already part of `requirements.txt`):
   ```bash
   pip install langchain-ollama
   ```
6. **Run the task:**
   ```bash
   python PART3_Ollama_Embeddings/task6_ollama_embeddings.py
   ```

## Troubleshooting

| Message | Fix |
|---------|-----|
| `Ollama is not running at http://localhost:11434` | Start the Ollama app or run `ollama serve` |
| `model 'nomic-embed-text' is not installed` | Run `ollama pull nomic-embed-text` |
| Very slow first request | The model is loading into memory; the next requests are faster |

To use another model, set `OLLAMA_EMBEDDING_MODEL` in the `.env` file (for example `mxbai-embed-large`).
