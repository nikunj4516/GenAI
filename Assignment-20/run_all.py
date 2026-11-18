"""
run_all.py - runs Tasks 1-5 in order and prints every required output.
Run:  python run_all.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PART1_Data_Preprocessing import task1_load_dataset, task2_text_preprocessing
from PART2_Text_Vectorization import task3_tfidf, task4_cosine_similarity
from PART3_Recommendation_Logic import task5_recommend_function

for task in (
    task1_load_dataset,
    task2_text_preprocessing,
    task3_tfidf,
    task4_cosine_similarity,
    task5_recommend_function,
):
    task.main()
    print()
