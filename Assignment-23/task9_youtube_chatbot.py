"""
PART 4 - Task 9: Build the YouTube RAG Chatbot

The chatbot
  1. accepts user questions
  2. retrieves the relevant transcript chunks (Task 8 retriever)
  3. uses an OpenAI LLM to generate the answer from those chunks only
  4. maintains the conversation context (chat history)

How one question is handled:

    user question
        |  (if there is chat history) the LLM rewrites it as a STANDALONE question
        |  e.g. "And the output layer?"  ->  "How many neurons are in the output layer?"
        v
    retriever (MMR over the transcript chunks)  ->  top chunks with timestamps
        v
    LLM answers using ONLY those chunks (+ chat history)   ->  answer + sources
        v
    the question and answer are added to the chat history

If the chunks do not contain the answer, the bot says so instead of guessing.

Run:  python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py                 (scripted demo conversation)
      python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py --interactive   (chat in the terminal)
      python PART4_YouTube_RAG_Chatbot/task9_youtube_chatbot.py --question "What is a bias?"
"""

import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings, get_llm
from PART4_YouTube_RAG_Chatbot.task7_load_youtube import TranscriptUnavailable
from PART4_YouTube_RAG_Chatbot.task8_youtube_vectorstore import get_youtube_retriever, get_youtube_vectorstore

CONDENSE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the latest user question, rewrite the latest question as a "
            "standalone question that can be understood without the chat history. Do NOT answer it. "
            "If it is already a standalone question, return it unchanged. Return only the question.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You answer questions about a YouTube video using ONLY the transcript excerpts below.\n"
            "Rules:\n"
            "- Use only the excerpts. Do not use outside knowledge, even if you know the answer.\n"
            "- If the excerpts do not contain the answer, reply exactly: {not_found}\n"
            "- Keep the answer clear and short (2-4 sentences).\n"
            "- The excerpts are automatic speech-to-text; silently fix obvious spelling mistakes.\n\n"
            "Transcript excerpts (each starts with its time in the video):\n{context}",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)


def format_context(docs):
    """Transcript chunks as text, each one starting with its timestamp."""
    return "\n\n".join(f"[{d.metadata.get('start_timestamp', '--:--:--')}] {d.page_content}" for d in docs)


class YouTubeChatbot:
    """Retrieval-augmented chatbot with conversation memory."""

    def __init__(self, retriever, llm, max_turns=6):
        self.retriever = retriever
        self.max_turns = max_turns                 # how many past question/answer pairs are remembered
        self.history = []                          # alternating HumanMessage / AIMessage
        self._condense = CONDENSE_PROMPT | llm | StrOutputParser()
        self._answer = ANSWER_PROMPT | llm | StrOutputParser()

    # ------------------------------------------------------------------ memory
    def reset(self):
        self.history = []

    def _remember(self, question, answer):
        self.history += [HumanMessage(content=question), AIMessage(content=answer)]
        self.history = self.history[-2 * self.max_turns:]

    # ------------------------------------------------------------------ one question
    def standalone_question(self, question):
        """Use the chat history to turn a follow-up into a self-contained question."""
        if not self.history:
            return question
        rewritten = self._condense.invoke({"question": question, "chat_history": self.history}).strip()
        return rewritten or question

    def ask(self, question):
        """Answer one question. Returns a dictionary with the answer, sources and details."""
        standalone = self.standalone_question(question)
        docs = self.retriever.invoke(standalone)

        if not docs:
            answer = config.NOT_FOUND_ANSWER
        else:
            answer = self._answer.invoke(
                {
                    "context": format_context(docs),
                    "question": standalone,
                    "chat_history": self.history,
                    "not_found": config.NOT_FOUND_ANSWER,
                }
            ).strip()

        found = config.NOT_FOUND_ANSWER.lower().rstrip(".") not in answer.lower()
        self._remember(question, answer)

        sources, seen = [], set()
        for d in sorted(docs, key=lambda d: d.metadata.get("start_seconds", 0)):
            stamp = d.metadata.get("start_timestamp")
            key = stamp or d.metadata.get("chunk_id")
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                {
                    "timestamp": stamp or "n/a",
                    "url": d.metadata.get("source", ""),
                    "preview": " ".join(d.page_content.split())[:110],
                }
            )
        return {
            "question": question,
            "standalone_question": standalone,
            "answer": answer,
            "found": found,
            "sources": sources,
            "docs": docs,
        }


def create_chatbot(url=config.YOUTUBE_URL, rebuild=False, verbose=True):
    """Build the whole chain: transcript -> vector store -> retriever -> chatbot."""
    llm = get_llm()
    store = get_youtube_vectorstore(url, rebuild=rebuild, verbose=verbose)
    return YouTubeChatbot(get_youtube_retriever(store), llm)


def print_turn(result):
    print(f"\nYou : {result['question']}")
    if result["standalone_question"].strip().lower() != result["question"].strip().lower():
        print(f"      (understood as: {result['standalone_question']})")
    print(f"Bot : {result['answer']}")
    if result["found"] and result["sources"]:
        print("      Retrieved from these moments of the video: " + ", ".join(
            f"{s['timestamp']}" for s in result["sources"]))


def interactive_chat(bot):
    print("\nChat with the video. Commands: 'reset' forgets the conversation, 'exit' quits.")
    while True:
        try:
            question = input("\nyou> ").strip()
        except EOFError:
            break
        if question.lower() in ("exit", "quit", "q", ""):
            break
        if question.lower() == "reset":
            bot.reset()
            print("(conversation history cleared)")
            continue
        try:
            print_turn(bot.ask(question))
        except Exception as error:
            print(f"(request failed: {type(error).__name__}: {str(error)[:150]})")


def main():
    parser = argparse.ArgumentParser(description="YouTube RAG chatbot")
    parser.add_argument("--url", default=config.YOUTUBE_URL, help="YouTube video URL")
    parser.add_argument("--question", help="ask one question and exit")
    parser.add_argument("--interactive", action="store_true", help="chat in the terminal")
    parser.add_argument("--rebuild", action="store_true", help="download and embed the transcript again")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 9: YOUTUBE RAG CHATBOT")
    print("=" * 70)
    print(f"Video: {args.url}")

    try:
        get_embeddings()
        bot = create_chatbot(args.url, rebuild=args.rebuild)
    except OpenAINotConfigured as error:
        fail(f"OpenAI is not available.\n{error}")
    except (TranscriptUnavailable, ValueError) as error:
        fail(str(error))
    except Exception as error:
        fail_openai(error)

    try:
        if args.question:
            print_turn(bot.ask(args.question))
        elif args.interactive:
            interactive_chat(bot)
        else:
            # scripted demo: a question, a follow-up that needs memory, and a question the video cannot answer
            follow = config.YOUTUBE_FOLLOW_UP
            print("\nDemo conversation (the 2nd question only makes sense with the 1st: conversation memory)")
            for question in (follow["first"], follow["second"], config.YOUTUBE_UNKNOWN_QUESTIONS[0]):
                print_turn(bot.ask(question))
            print(f"\nChat history kept: {len(bot.history) // 2} question/answer pairs")
    except Exception as error:
        fail_openai(error)


if __name__ == "__main__":
    main()
