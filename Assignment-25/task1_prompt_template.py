"""
PART 1 - Task 1: PromptTemplate

  1. Create a PromptTemplate with a system instruction and a user question placeholder
  2. Inject the user input dynamically
  3. Test with multiple inputs

A PromptTemplate is ONE string with {placeholders}. It produces plain text (a single block),
so the "system instruction" and the "question" live in the same string.

The formatting part runs without any LLM. The last part sends the prompts to the LLM when one is available.

Run:  python PART1_Prompt_Templates/task1_prompt_template.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.prompts import PromptTemplate

import models

# ---- 1) the template: system instruction + {question} placeholder (+ {level}, which has a default)
TEMPLATE = (
    "You are a patient AI tutor. Answer in at most two sentences and use simple words "
    "for a {level}.\n"
    "Question: {question}\n"
    "Answer:"
)
prompt = PromptTemplate(
    input_variables=["question"],
    template=TEMPLATE,
    partial_variables={"level": "beginner"},      # a default value, can be changed with .partial()
)


def main():
    print("=" * 70)
    print("TASK 1: PromptTemplate")
    print("=" * 70)

    print("\n[1] The template")
    print(f"    Type                : {type(prompt).__name__}")
    print(f"    Variables to fill   : {prompt.input_variables}   (default already set: {list(prompt.partial_variables)})")
    print("    Template text:")
    print("      " + TEMPLATE.replace("\n", "\n      "))

    print("\n[2] Dynamic input: prompt.format(question=...)")
    first = prompt.format(question=config.PROMPT_INPUTS[0])
    print("      " + first.replace("\n", "\n      "))

    print("\n[3] Test with multiple inputs")
    for i, question in enumerate(config.PROMPT_INPUTS, start=1):
        text = prompt.format(question=question)
        print(f"    Input {i}: {question!r}  ->  prompt of {len(text)} characters, question inserted: {question in text}")

    print("\n    Changing the default with .partial(): level='senior engineer'")
    expert = prompt.partial(level="senior engineer")
    print("      " + expert.format(question="What is a vector store?").replace("\n", "\n      "))

    print("\n    Missing input is detected:")
    try:
        PromptTemplate.from_template("Question: {question} Language: {language}").format(question="x")
    except KeyError as error:
        print(f"      KeyError: the placeholder {error} was not filled")

    print("\n    A PromptTemplate is a Runnable: .invoke() returns a StringPromptValue")
    value = prompt.invoke({"question": "What is a retriever?"})
    print(f"      {type(value).__name__} -> as text: {len(value.to_string())} characters, as messages: "
          f"{[type(m).__name__ for m in value.to_messages()]}")
    print("      (a plain string becomes ONE HumanMessage: there is no separate system message)")

    # ---- 3) send the prompts to the LLM
    print(f"\n[4] Send the prompts to the LLM ({models.provider_label()})")
    try:
        llm = models.get_llm()
    except models.ModelNotConfigured as error:
        print(f"    skipped - no LLM available.\n    {str(error)}".replace("\n", "\n    "))
        print("\n    (The prompt formatting above does not need an LLM and worked.)")
        return
    try:
        for question in config.PROMPT_INPUTS[:3]:
            reply = llm.invoke(prompt.format(question=question))
            print(f"\n    Q: {question}\n    A: {reply.content.strip()}")
    except Exception as error:
        models.fail_llm(error)


if __name__ == "__main__":
    main()
