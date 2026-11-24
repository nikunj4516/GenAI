"""
run_all.py - runs every code task (1-9) in order.

A task that needs something you do not have (an OpenAI key, a running Ollama) prints a clear message
explaining what to do and the next task still runs.
Task 10 (observations and insights) is the written file PART4_Runnables_LCEL/task10_observations_insights.md.

Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: loads .env, hides warnings)

from PART1_Prompt_Templates import task1_prompt_template, task2_chat_prompt_template
from PART2_Structured_Output import task3_pydantic_output_schema, task4_validation_error_handling
from PART3_Chains import task5_simple_chain, task6_conditional_chain, task7_parallel_chain
from PART4_Runnables_LCEL import task8_runnables_basics, task9_lcel_rag_chain

TASKS = [
    ("Task 1", task1_prompt_template),
    ("Task 2", task2_chat_prompt_template),
    ("Task 3", task3_pydantic_output_schema),
    ("Task 4", task4_validation_error_handling),
    ("Task 5", task5_simple_chain),
    ("Task 6", task6_conditional_chain),
    ("Task 7", task7_parallel_chain),
    ("Task 8", task8_runnables_basics),
    ("Task 9", task9_lcel_rag_chain),
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
        print("These tasks stopped early (no LLM / model error):", ", ".join(stopped))
        print("Read the message printed by each of them for how to fix it.")
    else:
        print("All tasks finished.")
    print("Task 10 answers: PART4_Runnables_LCEL/task10_observations_insights.md")
