# Task 12: Observations & Insights

## 1. Which loader is used for which data type?

| Data type | Loader | One Document per... | Metadata you get |
|-----------|--------|---------------------|------------------|
| `.txt` / `.md` notes | `TextLoader` | file | `source` |
| `.csv` table | `CSVLoader` | row | `source`, `row` |
| `.pdf` | `PyPDFLoader` | page | `source`, `page`, `total_pages` |
| Web page | `WebBaseLoader` | URL | `source` |
| Folder with many files | `DirectoryLoader` (+ `loader_cls` per file type) | depends on the file type | depends on the file type |

## 2. Best splitter for...

| Data | Best splitter | Why |
|------|---------------|-----|
| **Small text** (notes, short articles) | `RecursiveCharacterTextSplitter` with `chunk_size` about 300-500 | Keeps paragraphs and sentences together; often only a few chunks are needed. `CharacterTextSplitter` is enough when the text has clean line breaks. |
| **Large PDFs** | Load page by page with `PyPDFLoader`, then `RecursiveCharacterTextSplitter` (about 800-1000 characters) | Every chunk keeps its page number for citations; PDF text has many line breaks, so paragraph/line/word fallbacks are needed. |
| **Web data** | `RecursiveCharacterTextSplitter` (or `MarkdownHeaderTextSplitter` if the page is converted to Markdown / `HTMLHeaderTextSplitter` for HTML) | Web text is long, uneven and has headings; the recursive splitter handles uneven paragraph sizes and header splitters keep section titles. |
| Markdown documents | `MarkdownHeaderTextSplitter` | Chunks follow the headings and store them as metadata. |
| Mixed-topic long text where quality matters most | `SemanticChunker` | Cuts where the meaning changes (slower, needs embeddings). |

## 3. Why is chunk overlap important?

Without overlap, a chunk boundary can fall in the middle of an idea. The first half of a sentence ends one chunk and the second half starts the next one, so **neither chunk contains the complete information** and retrieval may miss the answer.

With overlap, the last part of one chunk is repeated at the start of the next chunk:

- the context before and after the cut is kept in both chunks;
- a sentence or fact near the boundary appears whole in at least one chunk;
- retrieval is more reliable because the same important text can be matched from either chunk.

**Trade-off:** too much overlap creates duplicate text, more chunks and higher cost. A common choice is **10-20% of `chunk_size`** (this project uses 50 characters for 500, i.e. 10%).

## Key learning

Good answers in a RAG system start with good data preparation: choose the loader that matches the data, choose a splitter that respects the structure of the data, and keep metadata and a small overlap so every chunk stays meaningful and traceable.
