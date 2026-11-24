"""
config.py - shared paths, model names, settings and test data used by every task file.

The OpenAI key is read from a local ".env" file (copy ".env.example" to ".env").
"""

import os
import warnings

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_env_file(path):
    """Tiny .env reader: KEY=VALUE lines. Real environment variables win."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(os.path.join(ROOT, ".env"))

# ------------------------------------------------------------------ OpenAI models
# gpt-4o-mini / gpt-4.1-mini are deprecated (shutdown Jan 14, 2027); OpenAI recommends gpt-6-luna.
# Change the model in the .env file if your account uses another one.
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-6-luna")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
# Not sent unless you set it: some newer models only accept their default temperature.
OPENAI_TEMPERATURE = os.getenv("OPENAI_TEMPERATURE", "").strip() or None

# ------------------------------------------------------------------ movie knowledge base (Tasks 3-6)
DATA_DIR = os.path.join(ROOT, "data")
CSV_FILE = os.path.join(DATA_DIR, "Movie_recommendation.csv")
CSV_ROW_LIMIT = 300          # first 300 movies (set None for all 4,803 rows)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVER_K = 4              # documents returned by every retriever

# MMR settings (Task 4)
MMR_FETCH_K = 20             # candidates fetched by similarity first
MMR_LAMBDA = 0.5             # 1.0 = pure relevance, 0.0 = pure diversity

# Queries with an objective answer: a movie is "relevant" when its text contains one of the keywords.
# The queries are worded vaguely on purpose, so a single similarity search can miss relevant movies.
LABELLED_QUERIES = [
    {
        "query": "Which films follow a masked vigilante who protects a dark city at night?",
        "keywords": ["batman"],
    },
    {
        "query": "adventures on the high seas with a ship captain and cursed treasure",
        "keywords": ["pirate"],
    },
    {
        "query": "a teenager gets powers after a bite from a radioactive arachnid",
        "keywords": ["spider-man", "spider man"],
    },
]

# ------------------------------------------------------------------ Wikipedia (Task 2)
WIKI_QUERIES = [
    "Retrieval-augmented generation",
    "Who created the Python programming language?",
]
WIKI_TOP_K = 3
WIKI_MAX_CHARS = 1500

# ------------------------------------------------------------------ YouTube RAG chatbot (Tasks 7-10)
# 3Blue1Brown - "But what is a neural network? | Deep learning chapter 1" (English captions)
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "https://www.youtube.com/watch?v=aircAruvnKk")
YOUTUBE_LANGUAGES = ["en"]
YOUTUBE_SEGMENT_SECONDS = 60      # the transcript is loaded in 60-second documents (keeps timestamps)
YOUTUBE_CHUNK_SIZE = 1000         # then split with the text splitter
YOUTUBE_CHUNK_OVERLAP = 200
# Optional: if YouTube blocks the transcript download, paste the transcript into this file.
YOUTUBE_FALLBACK_FILE = os.path.join(DATA_DIR, "youtube_transcript.txt")

YOUTUBE_RETRIEVER_K = 4
YOUTUBE_FETCH_K = 20
YOUTUBE_LAMBDA = 0.7              # MMR: mostly relevance, some diversity (chunks overlap a lot)

NOT_FOUND_ANSWER = "I couldn't find that in the video."

# Test questions for the default video above. "expected_any": the answer should contain
# at least one of these words. If you change the video, edit these questions.
YOUTUBE_TEST_CASES = [
    {"question": "How many pixels does each input image have?", "expected_any": ["784", "28"]},
    {"question": "How many hidden layers does the network have and how many neurons are in each one?",
     "expected_any": ["16"]},
    {"question": "What does each of the output neurons represent?", "expected_any": ["digit"]},
    {"question": "What is a bias?", "expected_any": ["bias"]},
    {"question": "What does the sigmoid function do?", "expected_any": ["0 and 1", "between 0", "squish", "squash"]},
    {"question": "About how many weights and biases does the network have in total?",
     "expected_any": ["13,002", "13002", "13,000", "13k"]},
    {"question": "What does it mean for the network to learn?", "expected_any": ["weights", "biases"]},
]
# Questions the video cannot answer: the chatbot must say so instead of making something up.
YOUTUBE_UNKNOWN_QUESTIONS = [
    "What is the capital of France?",
    "Who won the 2022 FIFA World Cup?",
]
# Follow-up test: the second question only makes sense with the first one (conversation memory).
YOUTUBE_FOLLOW_UP = {
    "first": "How many neurons are in each hidden layer?",
    "second": "And how many neurons are in the output layer?",
    "expected_any": ["10", "ten"],
}

# ------------------------------------------------------------------ vector store location
VECTORSTORE_DIR = os.path.join(ROOT, "vectorstores")

# ------------------------------------------------------------------ environment hygiene
os.environ.setdefault("USER_AGENT", "GenAI-Task23-Nikunj/1.0")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
