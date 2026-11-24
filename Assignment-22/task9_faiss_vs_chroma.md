# Task 9: FAISS vs ChromaDB Comparison

| | FAISS | ChromaDB |
|---|---|---|
| What it is | A **library** from Meta for fast vector search | A **vector database** with its own storage and query API |
| Storage | **In memory** while running. You must call `save_local()` / `load_local()` yourself to keep it | **Persistent** when `persist_directory` is set; data is saved automatically |
| Stores text and metadata? | Only vectors. LangChain keeps the documents in a separate pickle file (`index.pkl`) | Stores vectors, document text, metadata and ids together |
| Metadata filtering | Limited (filter after search in LangChain) | Built in (`filter={"type": "pdf"}`) |
| Add / update / delete | Adding is easy; deleting and updating are limited | `add`, `update`, `delete`, `get` by id |
| Search algorithms | Many (flat, IVF, HNSW, product quantization, GPU) | HNSW |
| Setup | `pip install faiss-cpu` | `pip install chromadb` |

## 1. In-memory vs persistent storage

- **In-memory (FAISS):** the index lives in RAM, so searching is extremely fast. When the program ends, the index is lost unless you save it to disk. After `save_local()` you can reload it with `load_local()` (Task 7). LangChain's loader needs `allow_dangerous_deserialization=True` because the document file is a pickle, so only load indexes you created yourself.
- **Persistent (ChromaDB):** data is written to a folder on disk as you add it, and it is available again the next time you open the same `persist_directory` (Task 8). There is no manual save step, and the next session can add more documents without rebuilding everything.

## 2. Use cases for FAISS

- Very **fast similarity search** over a large number of vectors (millions or more), including GPU search.
- **Research, benchmarks and experiments** where you control the index type and want maximum speed.
- A fixed collection that you **build once, save, and load** when needed (for example a read-only knowledge base inside a batch job).
- When you want **low-level control** over the index (compression, approximate search) or minimal dependencies.

## 3. Use cases for ChromaDB

- **Applications that keep growing**: documents are added, updated or deleted over time.
- When you need **metadata filtering** (search only the PDFs, only one author or one year).
- **Prototypes and small to medium RAG apps** that need persistence without running a database server.
- When you want one place that stores **text, metadata and embeddings together** and can be queried by id.
- Local development, and a path to a hosted or client/server setup later.

## Summary

Use **FAISS** when raw search speed and index control matter most; use **ChromaDB** when you want a simple persistent store with metadata, ids and easy updates. Both work with the same LangChain `similarity_search` interface, which is why Task 10 can switch between them with one setting.
