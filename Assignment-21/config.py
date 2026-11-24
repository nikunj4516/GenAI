"""
config.py - shared paths and settings used by every task file.
"""

import os
import warnings

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")
EXTRA_DIR = os.path.join(ROOT, "extra")

TXT_FILE = os.path.join(DATA_DIR, "notes.txt")
CSV_FILE = os.path.join(DATA_DIR, "Movie_recommendation.csv")
PDF_FILE = os.path.join(DATA_DIR, "company_handbook.pdf")
MD_FILE = os.path.join(EXTRA_DIR, "handbook.md")

# Any public webpage works (documentation, blog, help page).
WEB_URL = "https://en.wikipedia.org/wiki/Natural_language_processing"

# Splitter settings shared by Tasks 7, 8, 9 and 11
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# WebBaseLoader asks for a user agent; set one so no warning is printed.
os.environ.setdefault("USER_AGENT", "GenAI-Task21-Nikunj/1.0")

# langchain-community prints a "being sunset" DeprecationWarning on import; hide it so
# the task output stays clean (the loaders used here are the standard LangChain loaders).
warnings.filterwarnings("ignore", category=DeprecationWarning)
