# Build log

One block per finished task. Keep each line short.

## Template
- Date:
- Task:
- Built:
- Broke:
- Learned:

## Entries
- Date: 2026-11-23
- Task: T0 Setup
- Built: Project layout, .gitignore, .env.example, pyproject.toml, forge/ package stubs, Typer CLI with 4 commands (run, tools, serve, eval), test_cli.py.
- Broke: Standard pip editable install without isolation failed trying to connect to PyPI; resolved with --no-build-isolation --no-deps.
- Learned: Isolated wheel builds in sandboxed/offline environments require using pre-installed build tools without network lookup.


## Revise
Interview questions I answered weakly (add them here during the quiz step):
-
