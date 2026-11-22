---
name: forge-build
description: Use for every build task in the Forge coding-agent project. Runs the mentor loop (explain, interface, tests first, owner writes, review, quiz, commit) so the owner can defend every line.
---

# Forge build loop

The goal is not just working code. The goal is working code **that the owner wrote,
understands, and can defend in an interview**. Follow these 7 steps for every task in
`docs/TASKS.md`. Do not skip steps 1, 5 and 6.

## Step 1 — Explain (before any code)
- Say what this part is for, in 5-8 short lines of simple English.
- Point to where it sits in the pipeline (see `docs/ARCHITECTURE.md`, the step numbers).
- Give one real-world comparison if it helps (for example: "the registry is a menu,
  the dispatcher is the waiter").
- Name the one or two design choices in this task and the trade-off of each.

## Step 2 — Interface
- Write the function and class signatures with docstrings and `...` bodies,
  exactly as listed in the task's "Contract" section. Owner confirms or changes them.

## Step 3 — Tests first
- Write the tests in `tests/test_<module>.py`. Cover the normal case, one bad input,
  and one limit case (timeout, too long, outside workspace, and so on).
- Run them and show that they fail. Failing tests are the target.

## Step 4 — Owner writes the code
In mentor mode, help with this hint ladder. Move one rung at a time, only when asked
or after the owner has been stuck for about 20 minutes:
1. A question that points at the next step ("what should happen if the name is not in the dict?").
2. The plan in plain words, as numbered steps.
3. Pseudocode.
4. One small real code snippet for the hard part only.
5. Full code (only in speed mode), followed by a line-by-line walkthrough.

## Step 5 — Review
Run `uv run pytest -q`, then check:
- Does every error the model could cause turn into readable text, not a crash?
- Is there a limit on everything that can grow (steps, output size, time)?
- Can any path or command escape the workspace?
- Are names clear? Is any function longer than ~40 lines?
- For `mcp_server.py`: does anything except protocol messages go to stdout?
Give at most 5 review points, most important first. Owner fixes them.

## Step 6 — Quiz
Ask the 3 interview questions listed in the task (or similar ones). One at a time.
After each answer: say what was right, what was missing, and the short ideal answer.
If an answer is weak, add the question to `docs/LOG.md` under "Revise".

## Step 7 — Close the task
- `uv run pytest -q` passes.
- Tick the task box in `docs/TASKS.md`.
- Add to `docs/LOG.md`: date, task, what was built (1 line), what broke (1 line),
  what was learned (1 line).
- Commit: `T<n>: <what was built>`.
- Say the next task and its "done when" check.

## Time keeping
Each task has a time budget in `docs/TASKS.md`. If a task runs 50% over, stop and
offer: (a) cut scope as the task's "cut if late" line says, (b) switch this task to
speed mode, or (c) continue. The owner decides.

## Things to never do
- Never add a dependency that is not in `CLAUDE.md` without asking.
- Never write numbers into the README or resume text that were not produced by `forge eval`.
- Never call the agent "production-ready". It is a prototype with tests and evals.
