# Forge: project rules (read at the start of every session)

## What we are building
Forge is a terminal AI coding agent, written from scratch in Python.
You give it a task ("fix the failing test in this repo"). It reads files, edits them,
runs tests, and stops when the job is done or a limit is hit.
The same tools are also served over the Model Context Protocol (MCP), and an eval
harness measures how well the agent works.

## Why we are building it
1. The owner (Anirban) wants a resume project for AI systems / AI engineer roles.
2. He must be able to **explain and defend every line** in an interview.
   This matters more than speed. Code he cannot explain is worth nothing to him.
3. It must be finished in about 2 days (~20 focused hours), solo, from the terminal.

## Hard constraints
- Python 3.11+, managed with `uv`. No GPU. No web UI.
- Allowed dependencies: `openai`, `pydantic`, `typer`, `python-dotenv`, `pytest`, `rich`.
  Optional later: `langgraph` (task T15 only). Ask before adding anything else.
- The LLM is called through the OpenAI-compatible Chat Completions API, so the same
  code works with OpenAI, Groq, Gemini's OpenAI endpoint, or a local Ollama model.
  Settings come from `.env`: `FORGE_BASE_URL`, `FORGE_API_KEY`, `FORGE_MODEL`.
- Never commit `.env`. Never print the API key.
- Every agent run has hard limits: max steps, max tool-output size, a workspace folder
  it cannot leave, and a per-command timeout.

## How we work (always)
- Follow `docs/TASKS.md`. Work on ONE task at a time: the first unchecked task whose
  dependencies are all checked.
- For each task, use the `forge-build` skill (`.claude/skills/forge-build/SKILL.md`).
  It defines the loop: explain → interface → tests first → owner writes → review → quiz → commit.
- **Mentor mode is the default.** For the core files (`registry.py`, `dispatch.py`,
  `loop.py`, `gates.py`, `planner.py`, `mcp_server.py`) do NOT write the full
  implementation. Explain, give the function signatures and the tests, then give
  hints in steps. Write it fully only if the owner says "speed mode" for that task,
  and then walk him through it line by line afterwards.
- Boilerplate (pyproject, CLI wiring, Dockerfile, CI, README layout, eval task folders)
  may be written directly, but explain what each part does in 2-3 lines.
- Use simple English. No jargon without a one-line meaning.
- After each task: run `uv run pytest -q`, tick the box in `docs/TASKS.md`, add a line
  to `docs/LOG.md` (what was built, what broke, what was learned), and commit.

## Commands
- Tests: `uv run pytest -q`
- Run the agent: `uv run forge run "<task>" --workspace <dir> [--no-gates] [--mode plan]`
- List tools: `uv run forge tools`
- MCP server: `uv run forge serve`
- Evals: `uv run forge eval [--tasks N] [--runs 3]`

## Code style
- Type hints everywhere. Small functions. Dataclasses or Pydantic models for data.
- A short docstring on each public function that says **why** it exists, not just what.
- No `shell=True`. No bare `except:`. Errors that the model should see become text,
  errors that are our bugs should crash loudly in tests.
- In `mcp_server.py`, stdout carries protocol messages ONLY. All logs go to stderr.

## Commit messages
`T<number>: <what was built>` — for example `T4: dispatcher with timeouts and error text`.

## Start-of-session ritual
1. Read `docs/TASKS.md` and the last 10 lines of `docs/LOG.md`.
2. Run `uv run pytest -q` and report the result.
3. Say which task is next, its "done when" check, and the plan in 3-5 lines.
4. Wait for the owner to say go.
