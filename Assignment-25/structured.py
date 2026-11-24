"""
structured.py - reliable structured output: prompt -> LLM -> Pydantic object, with error handling (Task 4).

    structured_chain(prompt, llm, Schema, ...)  ->  a Runnable that returns a validated Schema object

Four layers protect the program from an LLM that does not follow the schema:
  1. PARSE     PydanticOutputParser checks the JSON and every field (types, confidence 0-1, ...).
  2. REPAIR    if parsing fails, the LLM gets its own bad output + the error and must correct it.
  3. RETRY     if that fails too, the whole question is asked again (up to max_attempts times).
  4. FALLBACK  if everything fails, a safe default object is returned instead of crashing.

The prompt must contain a {format_instructions} placeholder.
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import config  # noqa: F401  (import first: loads .env)

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

REPAIR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You repair invalid output so that it follows the required JSON format.\n"
            "Keep the meaning, fix only the format. Return ONLY the corrected JSON object, with no extra text.\n"
            "{format_instructions}",
        ),
        ("human", "Invalid output:\n{bad_output}\n\nWhat was wrong:\n{error}"),
    ]
)


def parse_or_repair(parser, repair_llm=None):
    """A Runnable: text -> Pydantic object. On a parse error it asks `repair_llm` to fix the text once."""

    def run(text):
        try:
            return parser.parse(text)
        except OutputParserException as first_error:
            if repair_llm is None:
                raise
            fixed = (REPAIR_PROMPT | repair_llm | StrOutputParser()).invoke(
                {
                    "format_instructions": parser.get_format_instructions(),
                    "bad_output": text,
                    "error": str(first_error)[:600],
                }
            )
            return parser.parse(fixed)           # still invalid -> OutputParserException (the retry layer catches it)

    return RunnableLambda(run, name="parse_or_repair")


def structured_chain(prompt, llm, schema, max_attempts=3, repair=True, fallback=None):
    """prompt | llm | parse (+repair) with retry and an optional fallback value (a `schema` object)."""
    parser = PydanticOutputParser(pydantic_object=schema)
    chain = (
        prompt.partial(format_instructions=parser.get_format_instructions())
        | llm
        | StrOutputParser()
        | parse_or_repair(parser, llm if repair else None)
    )
    chain = chain.with_retry(
        retry_if_exception_type=(OutputParserException,),
        stop_after_attempt=max_attempts,
        wait_exponential_jitter=False,
    )
    if fallback is not None:
        chain = chain.with_fallbacks(
            [RunnableLambda(lambda _: fallback.model_copy(), name="fallback_value")],
            exceptions_to_handle=(OutputParserException,),
        )
    return chain
