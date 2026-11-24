"""Core package for Assignment 26: Groq chatbot, RAG pipeline and FastAPI serving."""
import sys

# Windows consoles often default to cp1252, which crashes on non-ASCII model output.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
