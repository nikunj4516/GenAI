"""
PART 4 - Task 8: Runnables Basics

  1. Convert chains (and plain functions) into Runnables
  2. Use RunnablePassthrough
  3. Compose components with the LCEL pipe operator (|)

A Runnable is any LangChain component with the same methods: invoke, batch, stream (and async versions).
Prompts, LLMs, parsers, retrievers and whole chains are all Runnables, so they can be connected with |.

Parts 1-4 need no LLM. Part 5 uses the real LLM; if none is available it uses a SIMULATED model (clearly
labelled) so you can still see how the composition works.

Run:  python PART4_Runnables_LCEL/task8_runnables_basics.py
"""

import asyncio
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # import first: loads .env, hides warnings

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough

import models
from prompts import DIRECT_PROMPT


def title(text):
    print("\n" + "-" * 70 + f"\n{text}\n" + "-" * 70)


def main():
    print("=" * 70)
    print("TASK 8: RUNNABLES BASICS")
    print("=" * 70)

    # ------------------------------------------------------------------ 1) plain functions -> Runnables
    title("[1] A plain Python function becomes a Runnable with RunnableLambda")
    clean = RunnableLambda(lambda text: " ".join(text.split()), name="clean")
    count_words = RunnableLambda(lambda text: len(text.split()), name="count_words")
    messy = "   What   is  a   vector    store?  "
    print(f"    isinstance(clean, Runnable) = {isinstance(clean, Runnable)}")
    print(f"    invoke : {clean.invoke(messy)!r}")
    print(f"    batch  : {clean.batch(['  a   b ', ' c    d '])}")
    print(f"    stream : {list(clean.stream(messy))}   (a function returns everything in one piece)")
    print(f"    async  : {asyncio.run(clean.ainvoke(messy))!r}   (ainvoke is available without extra code)")

    # ------------------------------------------------------------------ 2) RunnablePassthrough
    title("[2] RunnablePassthrough: pass the input on unchanged (or add keys to it)")
    print(f"    RunnablePassthrough().invoke('hello')           -> {RunnablePassthrough().invoke('hello')!r}")
    added = RunnablePassthrough.assign(words=lambda x: len(x["text"].split()), characters=lambda x: len(x["text"]))
    print(f"    RunnablePassthrough.assign(...).invoke(dict)    -> {added.invoke({'text': 'one two three'})}")
    print("    (assign keeps the original keys and adds new ones; this is how chains carry the question along)")

    # ------------------------------------------------------------------ 3) LCEL composition
    title("[3] LCEL: components connected with |")
    pipeline = clean | RunnableLambda(str.title, name="title_case") | RunnableParallel(text=RunnablePassthrough(), words=count_words)
    print(f"    clean | title_case | RunnableParallel(text, words)")
    print(f"    invoke -> {pipeline.invoke(messy)}")
    print(f"    steps  -> {[getattr(s, 'name', None) or type(s).__name__ for s in (pipeline.first, *pipeline.middle, pipeline.last)]}")
    same = clean.pipe(RunnableLambda(str.upper))
    print(f"    .pipe() is the same as |      -> {same.invoke(messy)!r}")
    shortcut = {"original": RunnablePassthrough(), "upper": RunnableLambda(str.upper)}
    coerced = RunnablePassthrough() | shortcut
    print(f"    a dict inside a chain is turned into a RunnableParallel automatically: {type(coerced.last).__name__}")
    print(f"    -> {coerced.invoke('abc')}")

    # ------------------------------------------------------------------ 4) config on runnables
    title("[4] Useful methods on every Runnable")
    safe = RunnableLambda(lambda x: 10 / x, name="divide").with_fallbacks([RunnableLambda(lambda x: float('nan'))])
    print(f"    with_fallbacks : 10/0 -> {safe.invoke(0)} (no crash),  10/4 -> {safe.invoke(4)}")
    mapped = RunnableLambda(lambda x: x * 2).map()
    print(f"    map()          : applies the runnable to every item of a list -> {mapped.invoke([1, 2, 3])}")
    print(f"    with_config    : names a run for tracing -> {clean.with_config(run_name='clean_text').config}")

    # ------------------------------------------------------------------ 5) chains as runnables
    title("[5] Chains are Runnables too: compose chains from chains")
    try:
        llm = models.get_llm()
        print(f"    LLM: {models.provider_label()}")
    except models.ModelNotConfigured:
        llm = GenericFakeChatModel(messages=iter([
            AIMessage(content="A vector store keeps embeddings so that similar texts can be found quickly."),
            AIMessage(content="A vector store finds similar texts fast."),
        ] * 3))
        print("    LLM: SIMULATED model (no OpenAI key / Ollama found): the text below is canned, the composition is real")

    explain_chain = DIRECT_PROMPT | llm | StrOutputParser()                     # chain 1: question -> answer
    shorten_prompt = ChatPromptTemplate.from_template("Rewrite in one short sentence: {text}")
    shorten_chain = {"text": RunnablePassthrough()} | shorten_prompt | llm | StrOutputParser()   # chain 2: text -> short text

    print(f"    explain_chain is a Runnable: {isinstance(explain_chain, Runnable)}   shorten_chain: {isinstance(shorten_chain, Runnable)}")
    two_steps = explain_chain | shorten_chain                                   # chain of chains
    keep_all = RunnableParallel(question=lambda x: x["question"], long=explain_chain) | RunnablePassthrough.assign(
        short=lambda x: shorten_chain.invoke(x["long"])
    )
    try:
        print(f"\n    explain_chain | shorten_chain  (chain of chains):\n      {two_steps.invoke({'question': config.PROMPT_INPUTS[0]})}")
        result = keep_all.invoke({"question": config.PROMPT_INPUTS[0]})
        print("\n    RunnableParallel + RunnablePassthrough.assign (keep every intermediate value):")
        for key, value in result.items():
            print(f"      {key:<9}: {value}")
    except Exception as error:
        models.fail_llm(error)

    print("\nSUMMARY: function -> RunnableLambda | keep input -> RunnablePassthrough | combine -> | | parallel -> dict / RunnableParallel")


if __name__ == "__main__":
    main()
