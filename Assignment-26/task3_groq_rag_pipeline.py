"""Task 3: Groq-Based RAG Pipeline.

  1. Retrieve relevant document chunks using a vector store (FAISS)
  2. Construct a RAG prompt using the retrieved context
  3. Pass the prompt to the Groq LLM
  4. Return grounded answers

Documents come from product_reviews_dataset.csv (loaded, split into chunks,
embedded with sentence-transformers and stored in FAISS - see app/rag_service.py).

Run:  python "PART 2 — Groq + RAG/task3_groq_rag_pipeline.py"
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import config  # noqa: E402
from app.groq_service import GroqServiceError  # noqa: E402
from app.rag_service import RAGError, RAGPipeline  # noqa: E402

QUESTIONS = [
    "What do customers like most about the products?",
    "What are the most common complaints in the reviews?",
    "Which products have the best feedback?",
]


def main() -> int:
    print("=" * 70)
    print("TASK 3: Groq-Based RAG Pipeline")
    print("=" * 70)

    pipeline = RAGPipeline()
    try:
        print(f"Dataset: {config.find_dataset_path()}")
        pipeline.build_or_load()
    except (RAGError, FileNotFoundError) as exc:
        print(f"[FAIL] {exc}")
        return 1

    stats = pipeline.stats()
    print(f"Documents (CSV rows): {stats['documents']}")
    print(f"Chunks in FAISS     : {stats['chunks']}")
    print(f"Embedding model     : {stats['embedding_model']}")
    print(f"LLM                 : {config.GROQ_MODEL}")

    failures = 0
    for number, question in enumerate(QUESTIONS, start=1):
        print("\n" + "-" * 70)
        print(f"Q{number}: {question}")
        try:
            result = pipeline.answer(question)
        except GroqServiceError as exc:
            failures += 1
            print(f"[ERROR] {exc.message}")
            continue
        print("\nRetrieved chunks (step 1):")
        for rank, src in enumerate(result["sources"], start=1):
            preview = src["text"][:110] + ("..." if len(src["text"]) > 110 else "")
            print(f"  {rank}. score={src['score']:.3f} | row {src['doc_id']} | {preview}")
        print(f"\nGrounded answer (steps 2-4):\n{result['answer']}")

    print("\n[OK] Task 3 finished." if not failures else f"\n[WARN] {failures} question(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
