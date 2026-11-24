"""
run_all.py - runs every code task (1-5, 7-11) in order and prints all outputs.
Task 5 and the web part of Task 11 need an internet connection; if there is none they
print a clear message and the rest continues.

Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: sets user agent, hides warnings)

from PART1_Document_Loaders import (
    task1_text_loader,
    task2_csv_loader,
    task3_pdf_loader,
    task4_directory_loader,
    task5_webbase_loader,
)
from PART2_Text_Splitters import (
    task7_character_splitter,
    task8_recursive_splitter,
    task9_structure_based_splitter,
    task10_semantic_splitting,
)
from PART3_Mini_Integration import task11_unified_pipeline

TASKS = [
    task1_text_loader,
    task2_csv_loader,
    task3_pdf_loader,
    task4_directory_loader,
    task5_webbase_loader,
    task7_character_splitter,
    task8_recursive_splitter,
    task9_structure_based_splitter,
    task10_semantic_splitting,
    task11_unified_pipeline,
]

if __name__ == "__main__":
    sys.argv = sys.argv[:1]          # tasks must not read run_all's own arguments
    for task in TASKS:
        try:
            task.main()
        except SystemExit:           # Task 5 exits with 1 when the page cannot be loaded
            pass
        print()
    print("Conceptual tasks 6, 10 and 12 are in the .md files of PART2 and PART3.")
