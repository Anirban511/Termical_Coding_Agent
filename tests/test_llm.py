"""Tests for forge.llm. A fake client stands in for the OpenAI SDK: no network, no key."""

from types import SimpleNamespace
from typing import Any

import openai
import pytest

from forge.llm import LLMReply, ToolCall, chat, load_settings


# ---------- helpers: build objects shaped like the SDK's response ----------

def fake_response(
    content: str | None = None,
    tool_calls: list[tuple[str, str, str]] | None = None,
    usage: tuple[int, int] | None = (10, 5),
) -> SimpleNamespace:
    """Mimic `client.chat.completions.create(...)`'s return value."""
    sdk_calls = None
    if tool_calls:
        sdk_calls = [
            SimpleNamespace(id=i, type="function", function=SimpleNamespace(name=n, arguments=a))
            for i, n, a in tool_calls
        ]
    message = SimpleNamespace(content=content, tool_calls=sdk_calls)
    usage_obj = (
        SimpleNamespace(prompt_tokens=usage[0], completion_tokens=usage[1]) if usage else None
    )
    return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=usage_obj)


class FakeClient:
    """Plays back a script: each item is a response to return, or an exception to raise."""

    def __init__(self, script: list[Any]) -> None:
        self.script = list(script)
        self.calls: list[dict[str, Any]] = []  # kwargs of every create() call
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class FakeNetworkError(openai.APIConnectionError):
    """A real APIConnectionError subclass that skips building an HTTP request object,
    so the test does not depend on which HTTP library the SDK uses internally."""

    def __init__(self) -> None:
        Exception.__init__(self, "Connection error.")


def network_error() -> openai.APIConnectionError:
    return FakeNetworkError()


MSGS = [{"role": "user", "content": "say hi"}]
TOOLS = [{"type": "function", "function": {"name": "finish", "parameters": {"type": "object"}}}]


# ---------- normal cases ----------

def test_text_reply_and_token_counts() -> None:
    client = FakeClient([fake_response(content="hi", usage=(12, 3))])
    reply = chat(MSGS, TOOLS, client=client, model="m")
    assert reply == LLMReply(text="hi", tool_calls=[], tokens_in=12, tokens_out=3)


def test_tool_calls_are_converted_and_arguments_stay_raw() -> None:
    client = FakeClient([fake_response(tool_calls=[("call_1", "read_file", '{"path": "a.py"}')])])
    reply = chat(MSGS, TOOLS, client=client, model="m")
    assert reply.text is None
    assert reply.tool_calls == [ToolCall(id="call_1", name="read_file", arguments='{"path": "a.py"}')]
    assert isinstance(reply.tool_calls[0].arguments, str)


def test_sends_model_messages_and_tools() -> None:
    client = FakeClient([fake_response(content="ok")])
    chat(MSGS, TOOLS, client=client, model="my-model")
    sent = client.calls[0]
    assert sent["model"] == "my-model"
    assert sent["messages"] == MSGS
    assert sent["tools"] == TOOLS


# ---------- bad input / provider quirks ----------

def test_empty_tools_list_is_not_sent() -> None:
    client = FakeClient([fake_response(content="ok")])
    chat(MSGS, [], client=client, model="m")
    assert "tools" not in client.calls[0]


def test_missing_usage_gives_zero_tokens() -> None:
    client = FakeClient([fake_response(content="ok", usage=None)])
    reply = chat(MSGS, TOOLS, client=client, model="m")
    assert (reply.tokens_in, reply.tokens_out) == (0, 0)


def test_missing_setting_raises_with_its_name_but_not_the_key(monkeypatch: pytest.MonkeyPatch) -> None:
    # Empty string counts as missing; setenv also stops load_dotenv from refilling it.
    monkeypatch.setenv("FORGE_BASE_URL", "http://x")
    monkeypatch.setenv("FORGE_API_KEY", "sk-secret-123")
    monkeypatch.setenv("FORGE_MODEL", "")
    with pytest.raises(RuntimeError) as err:
        load_settings()
    assert "FORGE_MODEL" in str(err.value)
    assert "sk-secret-123" not in str(err.value)


# ---------- limits: retry exactly once ----------

def test_retries_once_on_network_error() -> None:
    client = FakeClient([network_error(), fake_response(content="hi")])
    reply = chat(MSGS, TOOLS, client=client, model="m")
    assert reply.text == "hi"
    assert len(client.calls) == 2


def test_gives_up_after_second_network_error() -> None:
    client = FakeClient([network_error(), network_error(), fake_response(content="never")])
    with pytest.raises(openai.APIConnectionError):
        chat(MSGS, TOOLS, client=client, model="m")
    assert len(client.calls) == 2
