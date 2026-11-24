"""
run_all.py - runs every code task (1, 2, 4, 5, 6, 7, 8, 10) in order.

A task that needs something you do not have (an OpenAI key, a running Ollama app) prints a clear
message explaining what to do and the next task still runs.
Conceptual tasks 3, 9 and 11 are in the .md files.

Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: loads .env, hides warnings)

from PART1_Embedding_Models import task1_openai_embeddings, task2_huggingface_embeddings
from PART2_Similarity_Search_OpenAI import task4_similarity_search_core, task5_langchain_vectorstore_search
from PART3_Ollama_Embeddings import task6_ollama_embeddings
from PART4_Vector_Stores import task7_faiss_store, task8_chroma_store
from PART5_Mini_Project import task10_end_to_end_pipeline

TASKS = [
    ("Task 1", task1_openai_embeddings),
    ("Task 2", task2_huggingface_embeddings),
    ("Task 4", task4_similarity_search_core),
    ("Task 5", task5_langchain_vectorstore_search),
    ("Task 6", task6_ollama_embeddings),
    ("Task 7", task7_faiss_store),
    ("Task 8", task8_chroma_store),
    ("Task 10", task10_end_to_end_pipeline),
]

if __name__ == "__main__":
    sys.argv = sys.argv[:1]               # tasks must not read run_all's own arguments
    skipped = []
    for name, task in TASKS:
        try:
            task.main()
        except SystemExit as stop:         # a task stops itself when a backend is not available
            if stop.code not in (0, None):
                skipped.append(name)
        print()

    print("=" * 70)
    if skipped:
        print("Stopped early (missing key / Ollama / model):", ", ".join(skipped))
        print("See the message printed by each of those tasks for how to fix it.")
    else:
        print("All code tasks finished.")
    print("Conceptual tasks: 3, 9 and 11 are in the .md files of PART1, PART4 and PART5.")
