# Task 6: Why Text Splitting is Required

## 1. Why can large documents not be passed directly to LLMs?

- **Context window limit.** Every LLM can read only a fixed number of tokens at once. A long PDF, a book or a 4,800-row CSV is far bigger than that limit, so it would be cut off or rejected.
- **Cost and speed.** Models are billed and slowed down by the number of tokens sent. Sending a whole document with every question is expensive and slow.
- **Lost focus.** When the useful sentence is hidden inside thousands of irrelevant lines, the model pays less attention to it and answers become less accurate ("lost in the middle" problem).
- **Poor search.** To find the right information we compare the question with pieces of text. One huge document gives one vague match; many small pieces give precise matches.

## 2. What problems does chunking solve in GenAI systems?

| Problem | How chunking helps |
|---------|--------------------|
| Text is larger than the context window | Each chunk fits easily inside the limit |
| High cost per request | Only the few relevant chunks are sent to the model |
| Irrelevant text confuses the model | Each chunk is small and focused on one idea |
| Imprecise retrieval | A question can be matched to the exact chunk that answers it |
| Embedding quality | Embeddings of short, focused text represent meaning better than embeddings of a whole document |
| Answers cannot be traced | Chunk metadata (file, page, header) shows exactly where an answer came from |

## Summary

Chunking turns one large document into small, meaningful, searchable pieces. A good chunk is **big enough to keep a complete idea** and **small enough to stay focused**. Chunk overlap keeps ideas from being cut in half at the boundary (see Task 12).
