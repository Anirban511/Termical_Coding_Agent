# How to use this starter pack

1. Create your repo: `uv init forge && cd forge && git init`.
2. Copy everything from this pack into the repo root, keeping the folders:
   - `CLAUDE.md` → read automatically by Claude Code at the start of every session.
   - `.claude/skills/forge-build/SKILL.md` → the build loop Claude Code follows for each task.
   - `docs/TASKS.md` → the task graph (T0 to T15) with contracts, "done when" checks and interview questions.
   - `docs/ARCHITECTURE.md` → the whole pipeline explained in simple words. Read it before T0.
   - `docs/LOG.md` → your build log and list of questions to revise.
3. Open the repo in a terminal and start Claude Code (`claude`). Say:
   `Start the session ritual and begin T0.`
4. For each task, the assistant explains, writes tests first, and you write the core code.
   Say `speed mode for this task` only when you are behind schedule.
5. Delete this file once the repo is set up.

No coding assistant? The pack still works: follow `docs/TASKS.md` top to bottom yourself,
and use the "Interview questions" under each task to test yourself.
