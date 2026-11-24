# 📚 Assignment 21: LangChain Document Loaders & Text Splitters

Foundation of a **Personal Knowledge Assistant**: load data from different sources with LangChain
**Document Loaders**, then split it into meaningful chunks with **Text Splitters**.

> Restrictions followed: Python + LangChain standard loaders/splitters only. **No vector database and no LLM calls.**

## Data (`data/` folder)

| File | Type | Used by |
|------|------|---------|
| `notes.txt` | Notes / explanation (`.txt`) | `TextLoader` |
| `Movie_recommendation.csv` | TMDB 5000 Movies table (`.csv`, 4,803 rows × 20 columns) | `CSVLoader` |
| `company_handbook.pdf` | Small 3-page PDF | `PyPDFLoader` |

Extra file: `extra/handbook.md`, a short Markdown document used only for header-based splitting (Task 9).
Web page for Task 5 / Task 11: https://en.wikipedia.org/wiki/Natural_language_processing (change `WEB_URL` in `config.py` to use any page).

## Project structure

```
GenAI_Task(21)Nikunj/
├── data/
│   ├── notes.txt
│   ├── Movie_recommendation.csv
│   └── company_handbook.pdf
├── extra/
│   └── handbook.md
├── PART1_Document_Loaders/
│   ├── task1_text_loader.py            # TextLoader
│   ├── task2_csv_loader.py             # CSVLoader
│   ├── task3_pdf_loader.py             # PyPDFLoader
│   ├── task4_directory_loader.py       # DirectoryLoader (+ verification)
│   └── task5_webbase_loader.py         # WebBaseLoader
├── PART2_Text_Splitters/
│   ├── task6_why_text_splitting.md     # concept answers
│   ├── task7_character_splitter.py     # CharacterTextSplitter
│   ├── task8_recursive_splitter.py     # RecursiveCharacterTextSplitter + comparison
│   ├── task9_structure_based_splitter.py   # Markdown headers + PDF pages
│   ├── task10_semantic_splitting.md    # concept answers
│   ├── task10_semantic_splitting.py    # SemanticChunker demo
│   └── splitter_utils.py               # helpers shared by the splitter tasks
├── PART3_Mini_Integration/
│   ├── task11_unified_pipeline.py      # load_and_split_documents(path_or_url)
│   └── task12_observations_insights.md # observations and insights
├── config.py                           # paths + chunk settings
├── setup_data.py                       # (optional) regenerates notes.txt / PDF / handbook.md
├── run_all.py                          # runs every code task in order
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt

python run_all.py                 # run every code task in order
```

Every task can also be run on its own:

```bash
python PART1_Document_Loaders/task1_text_loader.py
python PART2_Text_Splitters/task8_recursive_splitter.py
python PART3_Mini_Integration/task11_unified_pipeline.py
python PART3_Mini_Integration/task11_unified_pipeline.py <folder-or-url>   # your own target
```

Tasks 5 and 11 (web part) need an internet connection. Without one they print a clear message and the remaining tasks still run.

## Task overview

| Task | File | What it does |
|------|------|--------------|
| 1 | `task1_text_loader.py` | `TextLoader` → 1 document, preview, metadata |
| 2 | `task2_csv_loader.py` | `CSVLoader` → 4,803 documents (one per row) |
| 3 | `task3_pdf_loader.py` | `PyPDFLoader` → 3 pages, sample page |
| 4 | `task4_directory_loader.py` | `DirectoryLoader` with a loader per type; checks txt = 1, csv = 4,803, pdf = 3 |
| 5 | `task5_webbase_loader.py` | `WebBaseLoader` → first 500 characters of a page |
| 6 | `task6_why_text_splitting.md` | Why LLMs need chunks, what chunking solves |
| 7 | `task7_character_splitter.py` | `CharacterTextSplitter` (size 500, overlap 50) |
| 8 | `task8_recursive_splitter.py` | `RecursiveCharacterTextSplitter` and comparison with Task 7 |
| 9 | `task9_structure_based_splitter.py` | Markdown headers and PDF pages kept in metadata |
| 10 | `task10_semantic_splitting.md/.py` | Semantic chunking concept + offline demo |
| 11 | `task11_unified_pipeline.py` | One function for folders, files and URLs |
| 12 | `task12_observations_insights.md` | Loader/splitter choices and why overlap matters |

## Key results (from a real run)

- `DirectoryLoader`: 4,807 documents (1 txt + 4,803 csv rows + 3 pdf pages), matching direct loading for every type.
- Task 7 and Task 8 at `chunk_size=500`, `chunk_overlap=50`: 12 chunks each, because every paragraph already fits.
- At `chunk_size=300` the length-based splitter produced 3 chunks above the limit (longest 375), the recursive splitter 0.
- Task 9: all Markdown chunks keep their `Header 1/2/3`, all PDF chunks keep their page number.
- Task 10: the TF-IDF `SemanticChunker` demo cuts exactly at the cooking → space → football topic changes.
- Task 11 on `data/`: 18,633 chunks (6 txt, 18,621 csv, 6 pdf).

## Notes

- Task 10 uses a small TF-IDF embedding class so it runs offline with no model download. It detects shared words only; real projects should pass a neural embedding model to `SemanticChunker`.
- `setup_data.py` is optional (needs `pip install reportlab` for the PDF). The data files are already included.

## Tech stack

Python · LangChain (`langchain-community`, `langchain-text-splitters`, `langchain-experimental`) · pypdf · BeautifulSoup · scikit-learn
