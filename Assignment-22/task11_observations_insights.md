# Task 11: Observations & Insights

## 1. Importance of embeddings in GenAI

An embedding turns text into a list of numbers (a vector) that represents its **meaning**. Texts with similar meaning get vectors that are close to each other, even when they use different words ("kitten on the couch" is close to "cat on the sofa").

- Computers can compare meaning with simple math (cosine similarity) instead of exact keyword matching.
- They make **semantic search** possible: a question like "a film about a war in space" finds Avatar although the question never says "Avatar".
- They are the bridge between our documents and the language model: documents are stored as vectors, and a question is turned into a vector to find the right documents.
- The same idea powers recommendations, clustering, duplicate detection and classification.

## 2. Why are vector databases required?

- A real knowledge base has thousands or millions of chunks. Comparing a question with every vector one by one (as in Task 4) becomes **too slow**. Vector stores use indexes (such as FAISS or HNSW) for fast nearest-neighbour search.
- **Embedding is expensive** (time for local models, money for APIs). A vector store **saves the vectors**, so documents are embedded once and reused (Tasks 7 and 8 reload them from disk without calling the model again).
- They keep the **text and metadata** (source file, page, movie title) together with each vector, so results can be shown and cited.
- They support **adding, updating, deleting and filtering** documents as the knowledge base changes (ChromaDB).
- They provide a common interface (`similarity_search`), so the embedding model or the store can be switched without rewriting the application (Task 10).

## 3. How does this pipeline enable RAG systems?

RAG (Retrieval-Augmented Generation) answers a question using **retrieved** documents instead of only what the model remembers. Our pipeline is the **retrieval half**:

```
Documents -> Splitter -> Embeddings -> Vector Store      (done once, "indexing")
Question  -> Embedding -> Similarity Search -> top chunks (done for every question, "retrieval")
```

A full RAG chat only adds the last step: the top chunks are placed in a prompt together with the question and sent to an LLM, which writes the answer from that context. This reduces made-up answers, lets the model use private or recent data, and the chunk metadata shows the sources of the answer.

Because the pipeline in Task 10 is switchable (OpenAI / Hugging Face / Ollama and FAISS / Chroma), the retrieval part can be tuned and tested on its own, which is where most of the quality of a RAG system is decided: **if the right chunks are not retrieved, even the best LLM cannot answer correctly.**
