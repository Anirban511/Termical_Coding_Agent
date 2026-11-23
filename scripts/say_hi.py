"""T1 smoke test: one real call to the model configured in .env.

Run: uv run python scripts/say_hi.py
"""

from forge.llm import chat

reply = chat([{"role": "user", "content": "say hi"}], [])
print("reply:", reply.text)
print("tokens in/out:", reply.tokens_in, reply.tokens_out)
