# GenAI Assignment 23 – OpenAI & RAG

Retrieval-Augmented Generation with **LangChain + OpenAI + FAISS**.
Part 2–3 use the movie dataset (`data/Movie_recommendation.csv`), Part 4 builds a chatbot for a YouTube video.
No fine-tuning is used; the focus is retrieval quality.

## Folder structure

```
GenAI_Task(23)Nikunj/
├── data/Movie_recommendation.csv
├── PART1_Getting_Started/
│   └── task1_openai_setup.py            Task 1  – API key + basic prompt
├── PART2_Retriever_Based_RAG/
│   ├── task2_wikipedia_retriever.py     Task 2  – WikipediaRetriever
│   └── task3_vectorstore_retriever.py   Task 3  – OpenAI embeddings + FAISS retriever
├── PART3_Advanced_Retrieval/
│   ├── task4_mmr_retriever.py           Task 4  – similarity vs MMR
│   ├── task4_mmr_explanation.md         Task 4  – written explanation
│   ├── task5_multiquery_retriever.py    Task 5  – MultiQueryRetriever
│   └── task6_contextual_compression.py  Task 6  – ContextualCompressionRetriever
├── PART4_YouTube_RAG_Chatbot/
│   ├── task7_load_youtube.py            Task 7  – YoutubeLoader + text splitting
│   ├── task8_youtube_vectorstore.py     Task 8  – vector store + retriever
│   ├── task9_youtube_chatbot.py         Task 9  – RAG chatbot with conversation memory
│   └── task10_testing_evaluation.py     Task 10 – testing and evaluation
├── config.py  openai_models.py  corpus.py  store_utils.py  lc_compat.py   (shared helpers)
├── run_all.py        runs Tasks 1–10 in order
├── requirements.txt  .env.example  .gitignore
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # then open .env and put your key after OPENAI_API_KEY=
```

The key lives only in `.env` (ignored by Git). Optional overrides are listed in `.env.example`.

**Model note:** the default chat model is `gpt-6-luna` (older small models such as gpt-4o-mini / gpt-4.1-mini are
deprecated). Change it with `OPENAI_CHAT_MODEL=` in `.env`. Embeddings use `text-embedding-3-small`.
Internet is needed for OpenAI, Wikipedia and YouTube.

## Running

```bash
python run_all.py                                              # everything
python PART1_Getting_Started/task1_openai_setup.py             # or any single task
python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py --interactive
python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py --question "What is a bias?"
python PART4_YouTube_RAG_Chatbot/task10_testing_evaluation.py
```

## Tasks

| Task | What it does |
|---|---|
| 1 | Loads the key from `.env`, sends a prompt with the official SDK and with LangChain `ChatOpenAI` (key is never printed). |
| 2 | `WikipediaRetriever` for several queries, shows titles and text; optional LLM answer from the pages. |
| 3 | Embeds the first 300 movies (tagline, overview, genres, keywords; title added to each chunk) with OpenAI embeddings, saves a FAISS store in `vectorstores/`, retrieves top-k. |
| 4 | Compares similarity search and MMR (`k`, `fetch_k`, `lambda_mult`) with precision / unique-movie / diversity metrics. Explanation in `task4_mmr_explanation.md`. |
| 5 | `MultiQueryRetriever` prints the generated query variants and compares it with plain similarity using the same document budget. |
| 6 | `ContextualCompressionRetriever` with `LLMChainExtractor`, plus an `EmbeddingsFilter` → extractor pipeline; shows before/after text length. |
| 7 | `YoutubeLoader` (timestamped 60 s segments), then `RecursiveCharacterTextSplitter` (1000/200). |
| 8 | Embeds the transcript chunks into FAISS (cached; rebuilt automatically if settings change) and exposes an MMR retriever. |
| 9 | Chatbot: rewrites follow-ups into standalone questions, retrieves chunks, answers **only** from them, keeps the last 6 turns, says "I couldn't find that in the video." when unsure. |
| 10 | 7 video questions (keyword + LLM-judge "grounded" + sources/evidence checks), 2 unknown questions, 1 follow-up memory test, summary. |

## Design notes

- Stores save a `build_info.json` signature, so changing chunk size, model or row limit rebuilds the index.
- The default video is 3Blue1Brown's neural-network video. For another video use `--url` and edit
  `YOUTUBE_TEST_CASES`, `YOUTUBE_UNKNOWN_QUESTIONS` and `YOUTUBE_FOLLOW_UP` in `config.py`.
- Task 10's "grounded" check is an LLM judgement: a strong signal, not proof. A keyword FAIL can mean different
  wording, so read the answer and the evidence line.

## Testing notes (honest)

The code was run end to end in a sandbox **without** a real OpenAI key, internet or YouTube access, using a local
stand-in for the OpenAI API and a fake transcript/Wikipedia. That verified the wiring (SDK and LangChain calls, FAISS
build/save/load, retrievers, chatbot memory, error messages). It did **not** verify real model answers or real
retrieval-quality numbers; these will differ when you run it with a real key. Some stand-in "FAIL"s in Task 10 came
from the crude stand-in model, not the code.

## Troubleshooting

- **OPENAI_API_KEY is not set** → create `.env` from `.env.example`.
- **Model not found / temperature error** → set `OPENAI_CHAT_MODEL` to a model your account can use.
- **YouTube blocks transcripts** (cloud servers, VPNs) → run on your own network, or copy the transcript from YouTube
  ("Show transcript") into `data/youtube_transcript.txt`.
- **Wikipedia not reachable** → check your internet connection.
- **Rebuild a store** → `python PART4_YouTube_RAG_Chatbot/task8_youtube_vectorstore.py --rebuild`.
