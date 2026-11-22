"""Terminal entrypoint for Forge using Typer.

Exposes the 4 core subcommands:
- run: Executes the agent on a coding task.
- tools: Lists the registered tools available to the model.
- serve: Runs the MCP server over stdio for external clients.
- eval: Evaluates agent performance across benchmark tasks.
"""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console

app = typer.Typer(
    name="forge",
    help="Forge: A terminal AI coding agent built from scratch.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def run(
    task: str = typer.Argument(..., help="Task instruction for the agent to execute"),
    workspace: Path = typer.Option(
        Path("."),
        "--workspace",
        "-w",
        help="Workspace directory the agent is restricted to",
    ),
    gates: bool = typer.Option(
        True,
        "--gates/--no-gates",
        help="Run automatic test verification after edits",
    ),
    mode: str = typer.Option(
        "react",
        "--mode",
        "-m",
        help="Execution mode: react (step-by-step) or plan (plan-and-execute)",
    ),
) -> None:
    """Run the coding agent on a task."""
    console.print(f"[bold green]Starting Forge run:[/bold green] {task}")
    console.print(
        f"Workspace: {workspace.resolve()} | Mode: {mode} | Verification Gates: {gates}"
    )


@app.command()
def tools() -> None:
    """List all registered agent tools."""
    console.print("[bold cyan]Registered Tools:[/bold cyan]")
    console.print("No tools registered yet (will be populated in T2 and T3).")


@app.command()
def serve() -> None:
    """Start the Model Context Protocol (MCP) server over stdin/stdout."""
    console.print("[bold yellow]Starting MCP Server...[/bold yellow]")


@app.command(name="eval")
def run_eval(
    tasks: Optional[int] = typer.Option(
        None, "--tasks", "-t", help="Number of benchmark tasks to run"
    ),
    runs: int = typer.Option(
        3, "--runs", "-r", help="Number of repetitions per task setting"
    ),
) -> None:
    """Run benchmark evaluation suite."""
    console.print(f"[bold magenta]Running Evals:[/bold magenta] tasks={tasks}, runs={runs}")


if __name__ == "__main__":
    app()
