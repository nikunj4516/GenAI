"""
prompts.py - the prompt templates shared by Tasks 3-9 (Tasks 1 and 2 define their own, to show how they are built).

Keeping every prompt in one file is part of the modular design: a chain imports a prompt, it never builds
a long string inside its own code.
"""

from langchain_core.prompts import ChatPromptTemplate

import config

# ---- RAG answer in plain text (Tasks 7, 9; the RAG branch of Task 6)
RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a question-answering assistant for a personal knowledge base.\n"
            "Answer ONLY from the context below. Do not use outside knowledge.\n"
            f"If the context does not contain the answer, reply exactly: {config.NOT_FOUND_ANSWER}\n"
            "Keep the answer short (one to three sentences).\n\n"
            "Context:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

# ---- RAG answer as JSON that must fit the Answer schema (Tasks 3, 4)
STRUCTURED_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a question-answering assistant for a personal knowledge base.\n"
            "Answer ONLY from the context below. Do not use outside knowledge.\n"
            "Fill the fields like this:\n"
            "- answer: one to three sentences. If the context has no answer, write: " + config.NOT_FOUND_ANSWER + "\n"
            "- confidence: a number from 0.0 to 1.0 (use 0.0 when the context has no answer)\n"
            "- source: the label after 'source:' of the excerpt you used, copied exactly (use 'none' when there is no answer)\n\n"
            "Return ONLY a JSON object, with no extra text and no code fences.\n"
            "{format_instructions}\n\n"
            "Context:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

# ---- answer without documents (Tasks 5, 6)
DIRECT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer clearly in at most three sentences."),
        ("human", "{question}"),
    ]
)

# ---- router of the conditional chain (Task 6)
ROUTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a router. Decide how a user question should be answered.\n"
            "The knowledge base contains: " + config.DOCUMENT_TOPICS + ".\n"
            "- factual: the question asks for specific information that would be stored in those documents "
            "(a policy, a number, a rule, a definition from the notes, details of a movie).\n"
            "- general: anything else (greetings, advice, opinions, creative writing, general chat).\n"
            "Return ONLY a JSON object, with no extra text and no code fences.\n"
            "{format_instructions}",
        ),
        ("human", "{question}"),
    ]
)

# ---- the three chains of the parallel chain (Task 7)
SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Summarize the context below in two sentences, keeping only what is relevant to the question. "
            "Use only the context.\n\nContext:\n{context}",
        ),
        ("human", "{question}"),
    ]
)

FOLLOWUP_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Suggest follow-up questions a user could ask next, based on the question and the context. "
            "Give three short questions that the context can help to answer.\n"
            "Return ONLY a JSON object, with no extra text and no code fences.\n"
            "{format_instructions}\n\nContext:\n{context}",
        ),
        ("human", "{question}"),
    ]
)
