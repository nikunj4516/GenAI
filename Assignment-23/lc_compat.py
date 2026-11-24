"""
lc_compat.py - imports that work with old and new LangChain.

In LangChain 1.x the classic retrievers (MultiQuery, ContextualCompression, document
compressors) live in the 'langchain-classic' package; in LangChain 0.3 they are inside
'langchain' itself. This file hides that difference so the tasks use one import.
"""

try:  # LangChain 1.x
    from langchain_classic.retrievers import ContextualCompressionRetriever
    from langchain_classic.retrievers.document_compressors import (
        DocumentCompressorPipeline,
        EmbeddingsFilter,
        LLMChainExtractor,
    )
    from langchain_classic.retrievers.multi_query import MultiQueryRetriever
except ImportError:  # LangChain 0.3.x
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import (
        DocumentCompressorPipeline,
        EmbeddingsFilter,
        LLMChainExtractor,
    )
    from langchain.retrievers.multi_query import MultiQueryRetriever

__all__ = [
    "ContextualCompressionRetriever",
    "DocumentCompressorPipeline",
    "EmbeddingsFilter",
    "LLMChainExtractor",
    "MultiQueryRetriever",
]
