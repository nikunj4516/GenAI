"""
run_all.py - runs every task of Assignment 24 in order.

A task that needs something you do not have (Ollama, a pulled model) prints a clear message
explaining what to do; the next task still runs.

Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: loads .env)

from PART1_Getting_Started import task1_ollama_setup_chat

TASKS = [
    ("Task 1", task1_ollama_setup_chat),
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
        print("These tasks stopped early:", ", ".join(stopped))
        print("Read the message printed by each of them for how to fix it.")
    else:
        print("All tasks finished.")
