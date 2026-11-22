# Forge architecture, in simple words

## 1. The objective
Build a program that can **fix code by itself** from the terminal, then **prove with numbers**
how well it works.

The problem it solves: a language model (LLM) can only produce text. It cannot open a file,
run a test, or check its own work. Forge is the "body" around the model's "brain".
It gives the model hands (tools), rules (limits), eyes on the result (tests), and a record
of everything it did (traces).

Your resume objective: show you can build the parts that AI engineer job posts ask for —
agents, tool calling, MCP, evals, observability, guardrails — and explain each one.

## 2. The whole pipeline at a glance
```
 you ──task──▶ CLI ──▶ HARNESS LOOP ◀──────────────▶ LLM (the brain)
                          │   ▲
              tool call   │   │ checked, shortened result
                          ▼   │
                     DISPATCHER ──▶ TOOL REGISTRY ──▶ TOOLS (read, edit, run tests...)
                          │                                   │
                          │                              GATES + BUDGET
                          ▼
                     TRACE LOG ──▶ EVAL RUNNER ──▶ results table (your resume number)

 Same TOOL REGISTRY ──▶ MCP SERVER (JSON-RPC over stdin/stdout) ──▶ any MCP client
```

## 3. One run, step by step
Example task: *"Make the tests pass"* in a folder where `add(2, 3)` wrongly returns 6.

**Step 1 — You give the task (CLI).**
`forge run "Make the tests pass" --workspace examples/toy_bug`.
The CLI builds a `RunConfig`: which folder, max 25 steps, gates on, output limit 4000 characters.

**Step 2 — The loop starts the conversation (harness loop, item 18).**
It makes a message list: a system prompt ("you are a coding agent; use tools; call finish when done")
and your task. It also sends the **menu of tools** — their names, descriptions, and argument shapes.

**Step 3 — The model picks a tool (LLM).**
The model does not run anything. It only replies with a request, like:
`read_file({"path": "calc.py"})`. This is called **tool calling** or **function calling**.

**Step 4 — The dispatcher checks and runs it (dispatcher, item 21, + registry, item 19).**
- Does a tool called `read_file` exist? (registry lookup)
- Are the arguments valid? (Pydantic checks `path` is a string)
- Is the path inside the workspace? (safety check)
- Run it with a time limit.
If anything is wrong, the model gets a **readable error message**, not a crash, so it can correct itself.

**Step 5 — The result is checked and shortened (gates + budget, item 23).**
- **Budget:** if the output is huge (a 5,000-line file), cut it to the first and last parts,
  so the model's memory (context window) does not fill up.
- **Gate:** if the tool changed a file, Forge runs the tests by itself and adds a line like
  `GATE: 0 passed, 1 failed (test_add)`. The model sees at once whether its edit worked.

**Step 6 — The result goes back to the model, and the loop repeats.**
The loop adds the result to the message list (linked by the tool call's id) and asks the model again.
A typical run: read `calc.py` → read the test → `edit_file` (replace `a + b + 1` with `a + b`)
→ gate says `1 passed` → model calls `finish("fixed off-by-one in add")`.

**Step 7 — The loop stops.**
It stops when the model calls `finish`, when the model stops asking for tools, or when it hits
25 steps. That last rule stops an agent that is stuck going in circles.

**Step 8 — Everything is written down (trace log).**
Every step adds one line to `trace.jsonl`: which tool, success or error, how long, how many tokens.
This is **observability**: when something goes wrong, you can see exactly where.

## 4. Plan mode (item 22)
Instead of deciding one step at a time, the model first writes a short plan as JSON
(`["read the failing test", "find the bug in calc.py", "fix it", "run the tests"]`),
then Forge runs each step. If a step fails, it asks for a new plan once.
The eval tells you whether this is better or worse than step-by-step. That comparison is
itself a good interview story.

## 5. The MCP server (items 20 and 13)
**MCP (Model Context Protocol)** is a standard way for AI apps to use tools that live in a
separate program. Instead of every app writing its own "read file" tool, one MCP server
offers it and any MCP client can use it.

How Forge's server works:
- An MCP client starts `forge serve` as a child process.
- They talk through **stdin and stdout**, one JSON message per line. The message format is
  **JSON-RPC 2.0**: a request has a `method`, `params` and an `id`; the reply has the same `id`
  and either a `result` or an `error` with a standard code.
- Methods: `tools/list` (show the menu) and `tools/call` (run one tool). The tools come from the
  **same registry** the agent uses, so there is one source of truth.
- **Stateless:** in the current spec, each message carries everything needed (including the
  protocol version in `_meta`). The server remembers nothing between messages, so it can be
  restarted or copied freely.
- **Governance:** an allowlist says which tools outside clients may use (start read-only),
  and an audit log records every call.

## 6. The eval harness (item 11) — where your resume number comes from
1. 20 small folders, each with one bug and one failing test.
2. For each folder and each setting (gates on, gates off, plan mode), 3 runs:
   copy the folder → let Forge work → **Forge's own harness runs the tests** to judge
   (never trust the agent saying "done").
3. Record pass/fail, steps, tokens, time, tool errors → `results.md`.

This gives an honest sentence like: "Verification gates raised the pass rate from X% to Y%
on 20 tasks." X and Y are whatever you actually measure.

## 7. Why each design choice (interview answers in short)
| Choice | Why |
| --- | --- |
| Write the loop from scratch | You understand every part; frameworks hide the loop. |
| Pydantic schemas for tools | One definition gives validation AND the schema the model sees. |
| Errors go back as text | The model can read the mistake and fix its own call. |
| Hard limits (steps, time, size, folder) | An agent without limits can loop forever, hang, or touch files it should not. |
| Tests run automatically after edits | The model is often confident and wrong; tests are not. |
| Keep head and tail of long output | Errors usually appear at the end of test output. |
| JSONL traces | Append-only, one event per line, easy to grep and to load into pandas. |
| Harness judges pass/fail itself | An eval must not trust the thing it is measuring. |
| OpenAI-compatible API | Swap providers or run a local model by changing `.env` only. |
| stdout only for protocol | Any stray print breaks the MCP client's parsing. |

## 8. Words you should be able to explain
agent loop · tool calling / function calling · JSON Schema · structured output ·
context window · context engineering · guardrails · verification gate · observability /
tracing · evaluation harness · pass rate · MCP · JSON-RPC 2.0 · stdio transport ·
stateless server · allowlist · audit log · ReAct · plan-and-execute.
