# Task 4: How does MMR improve diversity?

## The problem with plain similarity search

`search_type="similarity"` returns the `k` chunks that are closest to the query. When the knowledge base contains many similar or repeated chunks (several chunks of the same movie, sequels, overlapping transcript chunks), the top `k` results are often **near-duplicates**. The LLM then receives the same information several times and misses other relevant information.

## What MMR does

**Maximal Marginal Relevance** selects the results one at a time:

1. Fetch `fetch_k` candidate chunks by normal similarity (for example 20).
2. Pick the most relevant candidate first.
3. For every next pick, score each remaining candidate as

   `score = lambda_mult x relevance(candidate, query) - (1 - lambda_mult) x similarity(candidate, already chosen chunks)`

4. Choose the highest score and repeat until `k` chunks are selected.

A candidate that is relevant **but very similar to a chunk that is already chosen** gets a lower score, so a different (still relevant) chunk wins instead.

## The settings

| Parameter | Meaning |
|-----------|---------|
| `k` | Number of chunks returned |
| `fetch_k` | Size of the candidate pool (larger = more room for diversity, a bit slower) |
| `lambda_mult` | 1.0 = only relevance (same as similarity search), 0.0 = only diversity, 0.5 = balanced |

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5},
)
```

## When to use it

- The data has many similar chunks (sequels, repeated explanations, overlapping chunks).
- The question is broad ("which movies are about superheroes?") and the answer needs **several different** sources.
- You want to give the LLM a wider context in the same number of chunks.

## Trade-off

MMR can return a chunk that is slightly less relevant than the next similarity result. For a very specific question with one correct chunk, plain similarity search can be better. Task 4 prints both methods side by side so you can see the difference on the movie data.
