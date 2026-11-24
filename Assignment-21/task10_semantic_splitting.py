"""
PART 2 - Task 10: Semantic Meaning-Based Splitting (Conceptual + Demo)

Concept (see task10_semantic_splitting.md):
  Semantic chunking splits text where the MEANING changes. Sentences are turned into
  embeddings; a large distance between two neighbouring sentences marks a new topic.

Demo:
  LangChain's SemanticChunker with a small TF-IDF embedding class (scikit-learn).
  No LLM call, no download and no vector database is used.
  In a real project, replace TfidfEmbeddings() with a neural embedding model.

Run:  python PART2_Text_Splitters/task10_semantic_splitting.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: sets user agent, hides warnings)

from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from sklearn.feature_extraction.text import TfidfVectorizer

# Three topics: cooking, space and football. Sentences of the same topic share
# topic words (pasta, sauce, planet, match ...), which is what TF-IDF can detect.
DEMO_TEXT = (
    "Boil the pasta in salted water for ten minutes. "
    "Drain the pasta and keep a little water for the sauce. "
    "Cook the tomato sauce with garlic and olive oil. "
    "Mix the sauce with the pasta and serve it hot. "
    "Jupiter is the largest planet in the solar system. "
    "Many space missions study the planet and its moons. "
    "Telescopes help astronomers observe each distant planet and galaxy. "
    "A rocket burns enormous fuel to reach another planet. "
    "The football match started in a packed stadium. "
    "The striker scored two goals in the football match. "
    "The goalkeeper saved a penalty and the crowd cheered the striker. "
    "The team won the match and the crowd lifted the trophy."
)


class TfidfEmbeddings(Embeddings):
    """Tiny offline embedding model: TF-IDF vectors fitted on the texts it receives."""

    def embed_documents(self, texts):
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            matrix = vectorizer.fit_transform(texts)
        except ValueError:                      # no usable words in the texts
            return [[0.0] for _ in texts]
        return matrix.toarray().tolist()

    def embed_query(self, text):
        return self.embed_documents([text])[0]


def build_semantic_chunker(threshold=80):
    return SemanticChunker(
        TfidfEmbeddings(),
        buffer_size=0,          # compare single sentences (no neighbouring sentences)
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=threshold,
    )


def main():
    print("=" * 70)
    print("TASK 10: SEMANTIC MEANING-BASED SPLITTING")
    print("=" * 70)
    print(
        "Concept: semantic chunking cuts the text where the topic changes. Each sentence\n"
        "is converted to an embedding; a large distance between two neighbouring sentences\n"
        "marks a breakpoint. Sentences between breakpoints form one chunk.\n"
    )

    chunker = build_semantic_chunker()

    # ---- Demo 1: text with three known topics ----
    chunks = chunker.split_text(DEMO_TEXT)
    print("--- Demo 1: 12 sentences = 4 about cooking, 4 about space, 4 about football ---")
    print("Number of semantic chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}: {chunk}")

    # ---- Check: did the cuts fall exactly where the topic changes? ----
    expected_starts = ["Boil the pasta", "Jupiter is", "The football match"]
    found = [c.startswith(e) for c, e in zip(chunks, expected_starts)]
    print("\nCut exactly at the topic changes (cooking -> space -> football):",
          len(chunks) == 3 and all(found))
    print(
        "\nNote: TF-IDF only sees shared WORDS, so this works because sentences of one topic\n"
        "share words. Neural embeddings (HuggingFaceEmbeddings, OpenAIEmbeddings, ...) also\n"
        "understand synonyms and are what you would use on real documents."
    )


if __name__ == "__main__":
    main()
