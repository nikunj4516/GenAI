"""
PART 1 - Task 2: ChatPromptTemplate & Message Templates

  1. Create a ChatPromptTemplate using SystemMessage, HumanMessage and (optional) AIMessage
  2. Use message prompt templates to structure a conversation
  3. Compare with a simple PromptTemplate

A ChatPromptTemplate is a LIST of messages, each with its own role. Chat models are trained on roles, so
the system instruction is kept apart from the user's question.

The formatting part runs without any LLM. The last part sends the prompts to the LLM when one is available.

Run:  python PART1_Prompt_Templates/task2_chat_prompt_template.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

import models

# ---- 1) message prompt templates: one template per role
system_template = SystemMessagePromptTemplate.from_template(
    "You are a patient AI tutor. Answer in at most two sentences and use simple words for a {level}."
)
example_question = HumanMessagePromptTemplate.from_template("{example_question}")      # an example (few-shot) turn
example_answer = AIMessagePromptTemplate.from_template("{example_answer}")             # AIMessage (optional)
user_template = HumanMessagePromptTemplate.from_template("{question}")

# ---- 2) the chat prompt: system -> example human -> example AI -> (conversation history) -> real question
chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_template,
        example_question,
        example_answer,
        MessagesPlaceholder("history", optional=True),      # earlier turns of a conversation, can be empty
        user_template,
    ]
).partial(
    level="beginner",
    example_question="What is an embedding?",
    example_answer="An embedding is a list of numbers that represents the meaning of a text, so similar texts get similar numbers.",
)

# the plain PromptTemplate of Task 1, for the comparison
simple_prompt = PromptTemplate.from_template(
    "You are a patient AI tutor. Answer in at most two sentences and use simple words for a beginner.\n"
    "Question: {question}\nAnswer:"
)


def show_messages(messages):
    for m in messages:
        print(f"      {type(m).__name__:<14} role={m.type:<6} | {m.content}")


def main():
    print("=" * 70)
    print("TASK 2: ChatPromptTemplate & MESSAGE TEMPLATES")
    print("=" * 70)

    print("\n[1] The message templates")
    print(f"    SystemMessagePromptTemplate  -> variables {system_template.input_variables}")
    print(f"    HumanMessagePromptTemplate   -> variables {user_template.input_variables}")
    print(f"    AIMessagePromptTemplate      -> variables {example_answer.input_variables}")
    print(f"    ChatPromptTemplate still needs: {chat_prompt.input_variables}  (the rest has defaults)")

    print("\n[2] Dynamic input: chat_prompt.invoke({'question': ...}).to_messages()")
    messages = chat_prompt.invoke({"question": config.PROMPT_INPUTS[0]}).to_messages()
    print(f"    {len(messages)} messages:")
    show_messages(messages)

    print("\n    With conversation history (MessagesPlaceholder) and another level:")
    history = [HumanMessage(content="What is a vector store?"),
               AIMessage(content="It is a database that stores embeddings and finds the most similar ones.")]
    messages = chat_prompt.partial(level="senior engineer").invoke(
        {"question": "And how is it different from a normal database?", "history": history}
    ).to_messages()
    print(f"    {len(messages)} messages:")
    show_messages(messages)

    print("\n    Test with multiple inputs:")
    for i, question in enumerate(config.PROMPT_INPUTS, start=1):
        messages = chat_prompt.invoke({"question": question}).to_messages()
        print(f"      Input {i}: {question!r} -> {len(messages)} messages, last one is a {type(messages[-1]).__name__}")

    print("\n[3] Comparison with the simple PromptTemplate (same question)")
    question = "What is a vector store?"
    simple_value = simple_prompt.invoke({"question": question})
    chat_value = chat_prompt.invoke({"question": question})
    print(f"    PromptTemplate      -> {type(simple_value).__name__}: 1 text block -> "
          f"{[type(m).__name__ for m in simple_value.to_messages()]}")
    print(f"    ChatPromptTemplate  -> {type(chat_value).__name__}: {len(chat_value.to_messages())} messages -> "
          f"{[type(m).__name__ for m in chat_value.to_messages()]}")
    print("""
    PromptTemplate                              ChatPromptTemplate
    ------------------------------------------  --------------------------------------------------
    one string with {placeholders}              a list of messages, each with a role
    instruction and question are mixed          system instruction is separate from the user turn
    no conversation history                     MessagesPlaceholder keeps earlier turns
    no examples as real turns                   few-shot examples as Human / AI message pairs
    best for: simple completions, one-off text  best for: chat models, chatbots, RAG, agents""")

    print(f"\n[4] Send both prompts to the LLM ({models.provider_label()})")
    try:
        llm = models.get_llm()
    except models.ModelNotConfigured as error:
        print(f"    skipped - no LLM available.\n    {str(error)}".replace("\n", "\n    "))
        print("\n    (The prompt formatting above does not need an LLM and worked.)")
        return
    try:
        for name, value in (("PromptTemplate", simple_value), ("ChatPromptTemplate", chat_value)):
            reply = llm.invoke(value)
            print(f"\n    {name}: {reply.content.strip()}")
    except Exception as error:
        models.fail_llm(error)


if __name__ == "__main__":
    main()
