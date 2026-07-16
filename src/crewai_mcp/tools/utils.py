"""Shared utilities for CrewAI MCP tools."""

from __future__ import annotations

import functools
import re
import subprocess
from pathlib import Path
from typing import Any, Callable, Optional

import anyio

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


def get_module_dir(project_path: Path) -> Optional[Path]:
    """Find the project's Python package directory under src/.

    CrewAI scaffolds projects as src/{module_name}/ where module_name is the
    underscore-normalized project name — it may differ from the directory name
    of the project itself (e.g. project 'my-crew' → module 'my_crew').

    Args:
        project_path: Project root directory.

    Returns:
        Path to the package dir (contains crew.py / main.py / config/), or None.
    """
    src = project_path / "src"
    if not src.is_dir():
        return None
    candidates = [d for d in src.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))]
    for d in candidates:
        if (d / "crew.py").exists() or (d / "main.py").exists() or (d / "config").is_dir():
            return d
    return candidates[0] if candidates else None


async def to_thread(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run a blocking callable in a worker thread so the MCP event loop stays responsive."""
    return await anyio.to_thread.run_sync(functools.partial(func, *args, **kwargs))


def run_command(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str, str]:
    """Run an external command, returning (exit_code, stdout, stderr).

    Args:
        cmd: Full command as an argv list.
        cwd: Working directory.
        timeout: Max seconds to wait for the command.
    """
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        stdin=subprocess.DEVNULL,
    )
    return result.returncode, result.stdout, result.stderr


async def run_command_async(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str, str]:
    """Async wrapper around run_command — never blocks the server event loop."""
    return await to_thread(run_command, cmd, cwd=cwd, timeout=timeout)


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
    return run_command(["uv", "run", "crewai", *args], cwd=cwd, timeout=timeout)


async def run_crewai_command_async(*args: str, cwd: Path, timeout: int = 300) -> tuple[int, str, str]:
    """Async wrapper around run_crewai_command."""
    return await to_thread(run_crewai_command, *args, cwd=cwd, timeout=timeout)


# ── crewai_tools import helpers ──────────────────────────────────────

KNOWN_CREWAI_TOOLS = {
    "SerperDevTool",
    "WebsiteSearchTool",
    "FileReadTool",
    "FileWriterTool",
    "DirectoryReadTool",
    "CSVSearchTool",
    "JSONSearchTool",
    "XMLSearchTool",
    "PDFSearchTool",
    "CodeDocsSearchTool",
    "GithubSearchTool",
    "ScrapeWebsiteTool",
    "YoutubeVideoSearchTool",
}

_TOOL_NAME_RE = re.compile(r"\b([A-Z]\w*Tool)\b")


def tool_import_line(tools: list[str]) -> Optional[str]:
    """Build the crewai_tools import line needed for a list of tool expressions.

    Args:
        tools: Tool constructor expressions (e.g. ['SerperDevTool()', 'FileReadTool()']).

    Returns:
        A 'from crewai_tools import A, B' line, or None if no known tools found.
    """
    names: set[str] = set()
    for expr in tools:
        for match in _TOOL_NAME_RE.findall(expr):
            if match in KNOWN_CREWAI_TOOLS:
                names.add(match)
    if not names:
        return None
    return f"from crewai_tools import {', '.join(sorted(names))}"


def insert_import(content: str, import_line: str) -> str:
    """Insert an import line after the last top-level import in a Python source string.

    Skips insertion if the import is already present.
    """
    if import_line in content:
        return content
    last_pos = -1
    for m in re.finditer(r"^(?:from\s+\S+\s+import\s+.*|import\s+\S+.*)$", content, re.MULTILINE):
        last_pos = m.end()
    if last_pos == -1:
        return import_line + "\n" + content
    return content[:last_pos] + "\n" + import_line + content[last_pos:]
