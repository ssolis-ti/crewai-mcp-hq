"""Shared utilities for CrewAI MCP tools."""

from __future__ import annotations

from pathlib import Path

from crewai_mcp.config import config


def get_project_path(project_name: str) -> Path:
    """Resolve a project name to its absolute path in the workspace.

    Sanitizes the project name to prevent directory traversal and
    resolves it against the configured workspace directory.
    Tries the original name first, then the underscore-normalized version
    (CrewAI CLI converts hyphens to underscores).

    Args:
        project_name: Name of the project directory.

    Returns:
        Absolute Path to the project root.
    """
    safe_name = Path(project_name).name
    path = config.paths.workspace / safe_name
    if path.exists():
        return path
    # CrewAI CLI normalizes hyphens → underscores
    normalized = safe_name.replace("-", "_")
    if normalized != safe_name:
        alt_path = config.paths.workspace / normalized
        if alt_path.exists():
            return alt_path
    return path


def run_crewai_command(*args: str, cwd: Path, timeout: int = 300) -> tuple[int, str, str]:
    """Run a crewai CLI command via uv inside a project directory.

    All CLI commands use `uv run crewai` for consistency — this ensures
    the project's own venv and dependencies are used, not the system's.

    Args:
        *args: Command arguments (e.g. 'test', '-n', '2').
        cwd: Working directory (project root).
        timeout: Max seconds to wait for the command.

    Returns:
        Tuple of (exit_code, stdout, stderr).
    """
    import subprocess

    cmd = ["uv", "run", "crewai", *args]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        stdin=subprocess.DEVNULL,
    )
    return result.returncode, result.stdout, result.stderr
