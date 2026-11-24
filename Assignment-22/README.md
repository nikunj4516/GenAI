# 🔎 Assignment 22: Embedding Models, Vector Stores & Similarity Search

The retrieval foundation of a **Personal Knowledge Search Engine**:

```
Documents -> Splitter -> Embeddings -> Vector Store -> Similarity Search
```

Documents from Assignment 21 (text, PDF, CSV, web) are split into chunks, converted to embeddings with
**OpenAI**, **Hugging Face** or **Ollama**, stored in **FAISS** or **ChromaDB**, and searched by meaning.
No full RAG chat yet: this assignment is the retrieval half of RAG.

> Restrictions followed: LangChain, OpenAI, Hugging Face, Ollama, FAISS and ChromaDB only.

## Documents (reused from Assignment 21)

| File | Type | Notes |
|------|------|-------|
| `data/notes.txt` | Text notes | 6 chunks |
| `data/company_handbook.pdf` | 3-page PDF | 6 chunks, page numbers kept in metadata |
| `data/Movie_recommendation.csv` | TMDB 5000 Movies | first **100 movies** are used (`CSV_ROW_LIMIT` in `config.py`; set `None` for all 4,803). Only title, tagline, overview, genres and keywords become text |
| Web page | https://en.wikipedia.org/wiki/Natural_language_processing | loaded when you are online (change `WEB_URL` in `config.py`); skipped automatically without internet |

All documents are split with `RecursiveCharacterTextSplitter` (chunk size 500, overlap 50), exactly as in Assignment 21.

## Project structure

```
GenAI_Task(22)Nikunj/
├── data/
│   ├── notes.txt
│   ├── company_handbook.pdf
│   └── Movie_recommendation.csv
├── PART1_Embedding_Models/
│   ├── task1_openai_embeddings.py
│   ├── task2_huggingface_embeddings.py
│   └── task3_openai_vs_huggingface.md
├── PART2_Similarity_Search_OpenAI/
│   ├── task4_similarity_search_core.py          # search(query, top_k=3) with NumPy
│   └── task5_langchain_vectorstore_search.py    # vectorstore.similarity_search(query)
├── PART3_Ollama_Embeddings/
│   ├── task6_ollama_setup.md
│   └── task6_ollama_embeddings.py
├── PART4_Vector_Stores/
│   ├── task7_faiss_store.py
│   ├── task8_chroma_store.py
│   └── task9_faiss_vs_chroma.md
├── PART5_Mini_Project/
│   ├── task10_end_to_end_pipeline.py            # switchable backend + store
│   └── task11_observations_insights.md
├── config.py                # paths, model names, settings, test queries
├── ingestion.py             # documents -> chunks (from Assignment 21)
├── embedding_backends.py    # one place that creates the 3 embedding models
├── run_all.py               # runs every code task in order
├── requirements.txt
├── .env.example             # copy to .env and add your OpenAI key
├── .gitignore
└── README.md
```

`vectorstores/` is created automatically when you run Tasks 7, 8 and 10 (it is ignored by Git).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

**1. OpenAI (Tasks 1, 2 comparison, 4, 5, 6 comparison)**
Copy `.env.example` to `.env` and paste your key: `OPENAI_API_KEY=sk-...`
The `.env` file is ignored by Git, so your key is never uploaded. Never put the key inside the code.

**2. Hugging Face (Tasks 2, 7, 8, 10)**
Nothing to configure. `sentence-transformers/all-MiniLM-L6-v2` (about 90 MB) downloads automatically the first time you run it.

**3. Ollama (Task 6, optional in Task 10)**
Install Ollama from https://ollama.com, make sure it is running, then:
```bash
ollama pull nomic-embed-text
```
Full steps and troubleshooting: `PART3_Ollama_Embeddings/task6_ollama_setup.md`.

## Run

```bash
python run_all.py                # every code task in order
```

If a task needs something you do not have (no OpenAI key, Ollama not running), it prints what to do and the next task still runs.
Each task can also be run alone:

```bash
python PART1_Embedding_Models/task1_openai_embeddings.py
python PART4_Vector_Stores/task7_faiss_store.py                  # Hugging Face (default)
python PART4_Vector_Stores/task7_faiss_store.py openai           # choose the embedding backend
python PART4_Vector_Stores/task8_chroma_store.py ollama
```

### Task 10: switch the embedding backend and the vector store

```bash
python PART5_Mini_Project/task10_end_to_end_pipeline.py                                   # demo: every available backend x faiss + chroma
python PART5_Mini_Project/task10_end_to_end_pipeline.py --embeddings openai --store chroma
python PART5_Mini_Project/task10_end_to_end_pipeline.py --embeddings huggingface --store faiss --query "How do I report a lost laptop?"
python PART5_Mini_Project/task10_end_to_end_pipeline.py --interactive                      # type your own questions
python PART5_Mini_Project/task10_end_to_end_pipeline.py --rebuild                          # re-embed and overwrite saved stores
```

The first run builds and saves the store; later runs **load the saved store without re-embedding**.
Each combination is saved separately (`vectorstores/faiss_openai`, `vectorstores/chroma_huggingface`, ...) because vectors from different models cannot be mixed.

From Python:

```python
from PART5_Mini_Project.task10_end_to_end_pipeline import KnowledgeSearchEngine

engine = KnowledgeSearchEngine(embedding_backend="huggingface", vector_store="chroma")
engine.search("a movie about a space war", top_k=3)
```

## Tasks overview

| Task | File | What it does |
|------|------|--------------|
| 1 | `task1_openai_embeddings.py` | `text-embedding-3-small`: vector length (1536) and sample values |
| 2 | `task2_huggingface_embeddings.py` | `all-MiniLM-L6-v2`: 384 dimensions, speed, comparison table |
| 3 | `task3_openai_vs_huggingface.md` | When to prefer each, cost vs performance |
| 4 | `task4_similarity_search_core.py` | In-memory embeddings + `search(query, top_k=3)`, 4 test queries |
| 5 | `task5_langchain_vectorstore_search.py` | `OpenAIEmbeddings` + FAISS + `similarity_search` |
| 6 | `task6_ollama_embeddings.py` | `nomic-embed-text` (768 dimensions) vs OpenAI / Hugging Face: size, speed, top-3 agreement |
| 7 | `task7_faiss_store.py` | Build, search, **save**, **reload and verify** a FAISS index |
| 8 | `task8_chroma_store.py` | Collection, store, **persist**, search, reopen from disk and verify |
| 9 | `task9_faiss_vs_chroma.md` | In-memory vs persistent, use cases |
| 10 | `task10_end_to_end_pipeline.py` | Documents -> Splitter -> Embeddings -> Store -> Search, switchable |
| 11 | `task11_observations_insights.md` | Why embeddings, why vector databases, how this enables RAG |

## Design notes

- **Same similarity score everywhere.** Vectors are normalized, and every search prints *cosine similarity* (FAISS: `1 - d/2` from the squared L2 distance; Chroma: `1 - cosine distance`). I checked that FAISS, Chroma and a plain NumPy dot product give identical values.
- **Movie chunks keep their title.** Every chunk of a movie starts with `title: <movie>`, so a long movie that is split into 2-4 chunks can still be found by name.
- **FAISS reload.** `FAISS.load_local(..., allow_dangerous_deserialization=True)` is required because LangChain stores documents in a pickle file. Only load indexes you created yourself.
- **Chroma re-runs** never create duplicates: the collection is recreated and every chunk has a fixed id.

## Testing notes

The code was tested end to end in an environment **without internet, an OpenAI key or Ollama**, using local stand-ins for the OpenAI and Ollama servers and a small local sentence-transformers model. This verified the wiring of all three backends, both vector stores, save/reload, persistence, the switchable pipeline and the error messages. It could **not** show real model quality or real timings, so run the tasks on your machine to get your own numbers and screenshots. Network-dependent parts (web page loading, the first model download, OpenAI calls) need internet on your side.

## Troubleshooting

| Message | Fix |
|---------|-----|
| `OPENAI_API_KEY is not set` | Create `.env` from `.env.example` and add your key |
| `Ollama is not running at http://localhost:11434` | Start the Ollama app or run `ollama serve` |
| `model 'nomic-embed-text' is not installed` | `ollama pull nomic-embed-text` |
| `Could not load the Hugging Face model` | `pip install sentence-transformers` and connect to the internet for the first download |
| `web=not available` | No internet; the other documents are still used |
| Changed the embedding model but results look wrong | Re-run with `--rebuild` (or delete `vectorstores/`) so the vectors are recreated with the new model |

## Tech stack

Python · LangChain · OpenAI Embeddings · Hugging Face (sentence-transformers) · Ollama · FAISS · ChromaDB
