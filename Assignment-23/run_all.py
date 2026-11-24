"""
run_all.py - runs every task (1-10) in order.

A task that needs something you do not have (an OpenAI key, internet, a transcript) prints a clear
message explaining what to do and the next task still runs.

Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: loads .env, hides warnings)

from PART1_Getting_Started import task1_openai_setup
from PART2_Retriever_Based_RAG import task2_wikipedia_retriever, task3_vectorstore_retriever
from PART3_Advanced_Retrieval import task4_mmr_retriever, task5_multiquery_retriever, task6_contextual_compression
from PART4_YouTube_RAG_Chatbot import (
    task7_load_youtube,
    task8_youtube_vectorstore,
    task9_youtube_chatbot,
    task10_testing_evaluation,
)

TASKS = [
    ("Task 1", task1_openai_setup),
    ("Task 2", task2_wikipedia_retriever),
    ("Task 3", task3_vectorstore_retriever),
    ("Task 4", task4_mmr_retriever),
    ("Task 5", task5_multiquery_retriever),
    ("Task 6", task6_contextual_compression),
    ("Task 7", task7_load_youtube),
    ("Task 8", task8_youtube_vectorstore),
    ("Task 9", task9_youtube_chatbot),
    ("Task 10", task10_testing_evaluation),
]

if __name__ == "__main__":
    sys.argv = sys.argv[:1]               # tasks must not read run_all's own arguments
    stopped = []
    for name, task in TASKS:
        try:
            task.main()
        except SystemExit as stop:         # a task stops itself when something is missing
            if stop.code not in (0, None):
                stopped.append(name)
        print()

    print("=" * 70)
    if stopped:
        print("These tasks stopped early (missing key / internet / transcript):", ", ".join(stopped))
        print("Read the message printed by each of them for how to fix it.")
    else:
        print("All tasks finished.")
    print("Task 4 explanation: PART3_Advanced_Retrieval/task4_mmr_explanation.md")
    print("For the interactive chatbot run:  python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py --interactive")
