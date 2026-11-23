"""LLM client wrapper for calling OpenAI-compatible Chat Completions API.

Why this module exists: it is the ONLY place that talks to the model provider.
The rest of Forge works with the small dataclasses below, so switching provider
(OpenAI, Groq, Gemini, Ollama) means changing `.env`, not code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import openai
from dotenv import load_dotenv


@dataclass
class ToolCall:
    """One tool request from the model."""

    id: str  # the model's id for this call; we must echo it back
    name: str
    arguments: str  # raw JSON string from the model, NOT parsed yet


@dataclass
class LLMReply:
    """Everything Forge needs from one model response, provider-independent."""

    text: str | None  # what the model said, if anything
    tool_calls: list[ToolCall] = field(default_factory=list)  # may be empty
    tokens_in: int = 0
    tokens_out: int = 0


@dataclass
class Settings:
    """Connection settings read from the environment / `.env`."""

    base_url: str
    api_key: str
    model: str


def load_settings() -> Settings:
    """Read FORGE_BASE_URL, FORGE_API_KEY, FORGE_MODEL so config lives in `.env`, not code.

    Raises RuntimeError naming the missing variable(s) if any is unset or empty.
    Must never include the API key's value in the error text.
    """
    ...


def chat(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    *,
    client: Any | None = None,
    model: str | None = None,
) -> LLMReply:
    """Send one Chat Completions request and convert the answer to an LLMReply.

    Why: the loop and planner should not know SDK details. `client` and `model`
    exist so tests can pass a fake client; by default both come from `load_settings()`.

    Rules:
    - Only send `tools=` when the list is non-empty (some providers reject `tools=[]`).
    - Retry exactly once on a network error (`openai.APIConnectionError`); if the
      second attempt also fails, let the error propagate.
    - If the response has no `usage`, report 0 tokens instead of crashing.
    """
    ...
