from typer.testing import CliRunner
from forge.cli import app

runner = CliRunner()


def test_cli_help() -> None:
    """Check that forge --help lists all 4 required subcommands."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "run" in result.output
    assert "tools" in result.output
    assert "serve" in result.output
    assert "eval" in result.output
