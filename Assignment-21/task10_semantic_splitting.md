# Task 10: Semantic Meaning-Based Splitting

## 1. What is semantic chunking?

Semantic chunking cuts a document **where the topic changes**, not after a fixed number of characters. Instead of asking "have I reached 500 characters?", it asks "does the next sentence still talk about the same thing?". Every chunk therefore contains sentences about one idea, even if the chunks have different lengths.

## 2. How do embeddings help?

1. The text is split into sentences.
2. Each sentence (usually together with its neighbours) is converted into an **embedding**, a vector of numbers that represents its meaning. Sentences with similar meaning get vectors that point in similar directions.
3. The **cosine distance** between each pair of neighbouring sentences is calculated. A small distance means the topic continues; a large distance means the topic has changed.
4. A **breakpoint** is placed wherever the distance is unusually large (for example above the 80th percentile of all distances).
5. Sentences between two breakpoints form one chunk.

## 3. Demo

`task10_semantic_splitting.py` uses LangChain's `SemanticChunker`.

- To respect the restrictions (no LLM calls, no downloads, no vector database) the demo uses a small **TF-IDF embedding class built with scikit-learn**. TF-IDF vectors capture shared words, so it works for the demo, but it cannot understand synonyms.
- In a real project you would pass a neural embedding model to `SemanticChunker` (for example `HuggingFaceEmbeddings` or `OpenAIEmbeddings`). The splitter code stays the same; only the embeddings object changes.

## Trade-offs

| Advantage | Disadvantage |
|-----------|--------------|
| Chunks follow the meaning of the text | Slower: every sentence must be embedded |
| No arbitrary cuts in the middle of a topic | Chunk sizes are uneven |
| Better retrieval for long, mixed-topic documents | Quality depends on the embedding model and threshold |
