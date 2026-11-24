"""
PART 4 - Task 10: Testing & Evaluation

  1. Ask at least 5 questions related to the video            (7 questions)
  2. Verify that the answers come from the video content      (3 checks per answer, see below)
  3. Handle unknown questions gracefully                      (2 questions the video cannot answer)
  + test of the conversation memory (a follow-up question)

Checks for every video question:
  keyword   : the answer contains the expected fact (e.g. "784")
  grounded  : a second LLM call ("judge") confirms that every fact of the answer is stated in the
              retrieved transcript chunks, i.e. the answer is not invented
              (not applicable when the bot says it could not find the answer)
  sources   : transcript chunks (with timestamps) were retrieved for the answer; the "Evidence" line
              shows the transcript sentence that best matches the answer
For unknown questions the bot passes when it says it could not find the answer in the video.

The test questions are written for the default video (3Blue1Brown, neural networks). If you test another
video, edit YOUTUBE_TEST_CASES, YOUTUBE_UNKNOWN_QUESTIONS and YOUTUBE_FOLLOW_UP in config.py.

Needs:  OPENAI_API_KEY in .env and internet for the first run
Run:    python PART4_YouTube_RAG_Chatbot/task10_testing_evaluation.py
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from openai_models import OpenAINotConfigured, fail, fail_openai, get_embeddings, get_llm
from PART4_YouTube_RAG_Chatbot.task7_load_youtube import TranscriptUnavailable
from PART4_YouTube_RAG_Chatbot.task9_youtube_chatbot import create_chatbot, format_context

JUDGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You check whether an answer is supported by transcript excerpts of a video. "
            "Reply with exactly one word: YES if every fact in the answer is stated in the excerpts, "
            "NO if any part of the answer is not in the excerpts.",
        ),
        ("human", "Excerpts:\n{context}\n\nAnswer to check:\n{answer}"),
    ]
)


def contains_any(text, words):
    text = text.lower()
    return any(w.lower() in text for w in words)


def short(text, n=120):
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 3] + "..."


def stamps(result):
    return ", ".join(s["timestamp"] for s in result["sources"]) or "-"


def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2}


def best_evidence(result):
    """The transcript sentence (and its timestamp) that best matches the answer, or None."""
    answer_words = words(result["answer"])
    best_score, best_stamp, best_sentence = 0, None, ""
    for doc in result["docs"]:
        stamp = doc.metadata.get("start_timestamp", "n/a")
        for sentence in re.split(r"(?<=[.?!])\s+", " ".join(doc.page_content.split())):
            score = len(answer_words & words(sentence))
            if score > best_score:
                best_score, best_stamp, best_sentence = score, stamp, sentence
    return (best_stamp, best_sentence) if best_stamp else None


def main():
    parser = argparse.ArgumentParser(description="Test and evaluate the YouTube RAG chatbot")
    parser.add_argument("--url", default=config.YOUTUBE_URL, help="YouTube video URL")
    args = parser.parse_args()

    print("=" * 70)
    print("TASK 10: TESTING & EVALUATION OF THE YOUTUBE RAG CHATBOT")
    print("=" * 70)
    print(f"Video: {args.url}")
    if args.url != config.YOUTUBE_URL:
        print("NOTE: the test questions are written for the default video. Edit them in config.py for this one.")

    try:
        get_embeddings()
        bot = create_chatbot(args.url)
        judge = JUDGE_PROMPT | get_llm() | StrOutputParser()
    except OpenAINotConfigured as error:
        fail(f"OpenAI is not available.\n{error}")
    except (TranscriptUnavailable, ValueError) as error:
        fail(str(error))
    except Exception as error:
        fail_openai(error)

    passed = {"video": 0, "grounded": 0, "unknown": 0, "memory": 0}
    answered = 0          # video questions where the bot gave an answer (so "grounded" can be judged)

    try:
        # ------------------------------------------------------------ A) questions about the video
        cases = config.YOUTUBE_TEST_CASES
        print("\n" + "=" * 70)
        print(f"A) {len(cases)} QUESTIONS ABOUT THE VIDEO  (each one starts a fresh conversation)")
        print("=" * 70)
        for i, case in enumerate(cases, start=1):
            bot.reset()
            result = bot.ask(case["question"])
            keyword_ok = contains_any(result["answer"], case["expected_any"])
            has_sources = bool(result["sources"]) and result["found"]

            if result["found"]:
                verdict = judge.invoke({"context": format_context(result["docs"]), "answer": result["answer"]})
                grounded = verdict.strip().upper().startswith("YES")
                answered += 1
                passed["grounded"] += grounded
                grounded_text = "PASS" if grounded else "FAIL"
            else:
                grounded_text = "n/a (the bot gave no answer)"

            passed["video"] += keyword_ok and has_sources
            print(f"\nQ{i}: {case['question']}")
            print(f"    Answer   : {short(result['answer'], 230)}")
            print(f"    Retrieved: transcript chunks at {stamps(result)}")
            print(f"    Checks   : keyword {'PASS' if keyword_ok else 'FAIL'} (expects one of {case['expected_any']}) | "
                  f"grounded {grounded_text} | sources {'PASS' if has_sources else 'FAIL'}")
            evidence = best_evidence(result) if result["found"] else None
            if evidence:
                print(f"    Evidence : [{evidence[0]}] \"{short(evidence[1], 220)}\"")

        # ------------------------------------------------------------ B) unknown questions
        unknown = config.YOUTUBE_UNKNOWN_QUESTIONS
        print("\n" + "=" * 70)
        print(f"B) {len(unknown)} UNKNOWN QUESTIONS  (the video does not contain the answer)")
        print("=" * 70)
        for question in unknown:
            bot.reset()
            result = bot.ask(question)
            ok = not result["found"]
            passed["unknown"] += ok
            print(f"\nQ: {question}")
            print(f"    Answer : {short(result['answer'], 200)}")
            print(f"    Check  : {'PASS - says it could not find it' if ok else 'FAIL - it answered from outside the video'}")

        # ------------------------------------------------------------ C) conversation memory
        follow = config.YOUTUBE_FOLLOW_UP
        print("\n" + "=" * 70)
        print("C) CONVERSATION CONTEXT  (the 2nd question depends on the 1st)")
        print("=" * 70)
        bot.reset()
        first = bot.ask(follow["first"])
        second = bot.ask(follow["second"])
        memory_ok = contains_any(second["answer"], follow["expected_any"]) and second["found"]
        passed["memory"] += memory_ok
        print(f"\nQ1: {follow['first']}\n    Answer: {short(first['answer'], 200)}")
        print(f"Q2: {follow['second']}\n    Rewritten as: {second['standalone_question']}")
        print(f"    Answer: {short(second['answer'], 200)}")
        print(f"    Check : {'PASS' if memory_ok else 'FAIL'} (expects one of {follow['expected_any']})")
    except Exception as error:
        fail_openai(error)

    # ------------------------------------------------------------ summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Video questions answered correctly with sources : {passed['video']} / {len(cases)}")
    print(f"  Answers confirmed as grounded in the transcript  : {passed['grounded']} / {answered}  (answers that were given)")
    print(f"  Unknown questions handled gracefully             : {passed['unknown']} / {len(unknown)}")
    print(f"  Follow-up question understood (memory)           : {passed['memory']} / 1")
    print(
        "\nHow to read this: a FAIL on 'keyword' can also mean the answer is worded differently, so read the\n"
        "answer and the evidence line. 'grounded' is judged by an LLM and is a strong signal, not a proof."
    )


if __name__ == "__main__":
    main()
