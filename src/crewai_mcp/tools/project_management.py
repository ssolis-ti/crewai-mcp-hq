"""
MCP Tools — Project Management.

Tools for creating and managing CrewAI projects (crews and flows).
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from pathlib import Path

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.config import config
from crewai_mcp.tools.utils import (
    get_module_dir,
    get_project_path,
    run_command_async,
    run_crewai_command_async,
)

logger = logging.getLogger("crewai-mcp.tools.project_management")


def _get_workspace() -> Path:
    """Get the configured workspace path, creating it if needed."""
    workspace = config.paths.workspace
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


@mcp.tool()
async def crewai_create_project(
    name: str = Field(..., description="Name of the project directory"),
    project_type: str = Field(
        default="crew",
        description="Type of project to create ('crew' or 'flow')",
    ),
    provider: str = Field(
        default="openai",
        description="LLM provider to use (e.g., 'openai', 'anthropic', 'gemini', 'ollama'). "
        "Note: This sets up the provider non-interactively via --skip_provider; "
        "you'll need to configure API keys in the project's .env file after creation.",
    ),
) -> str:
    """
    Create a new CrewAI project using the official CLI.

    This generates the standard scaffolding for a CrewAI project,
    including pyproject.toml, src directory, yaml configs, and entry points.
    The project is created inside the configured CrewAI workspace.

    Note: The --skip_provider flag is used to avoid interactive prompts.
    You will need to manually configure the provider API keys in the project's .env file.
    """
    if project_type not in ("crew", "flow"):
        return f"Error: Invalid project_type '{project_type}'. Use 'crew' or 'flow'."

    workspace = _get_workspace()

    # Sanitize: strip any path components so the CLI can't create the
    # project outside the workspace (e.g. name='../evil').
    safe_name = Path(name).name

    # get_project_path also checks the underscore-normalized variant the
    # CLI actually creates (my-crew → my_crew), so duplicates are caught.
    project_path = get_project_path(safe_name)
    if project_path.exists():
        return f"Error: Project '{safe_name}' already exists at {project_path}"

    try:
        code, stdout, stderr = await run_crewai_command_async(
            "create", project_type, safe_name, "--skip_provider", cwd=workspace, timeout=120
        )

        if code != 0:
            return f"Failed to create project.\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"

        # The CLI normalizes hyphens → underscores; resolve what it actually created
        project_path = get_project_path(safe_name)

        # Create a basic .env file with provider hints
        _write_env_file(project_path, provider)

        # Fix pyproject.toml: --skip_provider generates pre-release pins
        # (e.g. 1.14.5a2) that don't resolve on PyPI → patch to stable range
        _patch_pyproject_version(project_path)

        module_dir = get_module_dir(project_path)
        module_name = module_dir.name if module_dir else name

        return (
            f"Successfully created CrewAI {project_type} '{name}' at {project_path}\n"
            f"Next steps:\n"
            f"1. Update src/{module_name}/config/agents.yaml and tasks.yaml\n"
            f"2. Add custom tools in src/{module_name}/tools/\n"
            f"3. Configure API keys in the project's .env file\n"
            f"4. Run crewai_install_deps tool to set up the environment."
        )

    except subprocess.TimeoutExpired:
        return "Error: Project creation timed out after 120 seconds."
    except Exception as e:
        logger.exception("Error creating project")
        return f"Error executing crewai cli: {str(e)}"


@mcp.tool()
async def crewai_install_deps(
    project_name: str = Field(..., description="Name of the project in the workspace"),
    extra_packages: list[str] = Field(
        default_factory=list,
        description="Optional additional packages to install (via 'uv add')",
    ),
) -> str:
    """
    Install project dependencies.

    Runs `crewai install` inside the project directory and optionally
    installs additional packages (e.g., specific crewai-tools).
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found at {project_path}"

    output_lines = []

    try:
        # 1. Run crewai install
        code, stdout, stderr = await run_crewai_command_async(
            "install", cwd=project_path, timeout=300
        )
        output_lines.append(f"crewai install (exit {code}):\n{stdout}\n{stderr}")

        # 2. Install extra packages if requested — projects are uv-managed
        if extra_packages:
            cmd = ["uv", "add", *extra_packages]
            logger.info("Running: %s in %s", " ".join(cmd), project_path)
            code2, stdout2, stderr2 = await run_command_async(cmd, cwd=project_path, timeout=300)
            output_lines.append(f"installing extras (exit {code2}):\n{stdout2}\n{stderr2}")

        return "\n\n".join(output_lines)

    except subprocess.TimeoutExpired:
        return "Error: Dependency installation timed out after 300 seconds."
    except Exception as e:
        logger.exception("Error installing dependencies")
        return f"Error: {str(e)}"


@mcp.tool()
def crewai_project_info(
    project_name: str = Field(..., description="Name of the project"),
) -> str:
    """
    Read the structure and core configurations of a CrewAI project.

    Returns the pyproject.toml dependencies, available YAML configs,
    and Python source files to understand the current state of the project.
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found at {project_path}"

    info = {"name": project_name, "path": str(project_path), "files": {}, "configs": {}}

    # Read pyproject.toml
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        info["files"]["pyproject.toml"] = pyproject.read_text(errors="replace")

    module_dir = get_module_dir(project_path)
    if module_dir:
        info["module"] = module_dir.name

        # Read YAML configs
        config_dir = module_dir / "config"
        if config_dir.exists():
            for yaml_file in config_dir.glob("*.yaml"):
                info["configs"][yaml_file.name] = yaml_file.read_text(errors="replace")

        # List python files
        info["files"]["python_sources"] = [
            str(f.relative_to(project_path)) for f in module_dir.rglob("*.py")
        ]

    return json.dumps(info, indent=2)


# ── Internal helpers ─────────────────────────────────────────────────


def _write_env_file(project_path: Path, provider: str) -> None:
    """Create a .env file with provider-specific template."""
    env_file = project_path / ".env"
    content = (
        f"# CrewAI Project Configuration\n"
        f"# Provider: {provider}\n"
        f"# Add your API keys below:\n"
    )
    if provider == "openai":
        content += "OPENAI_API_KEY=your-api-key-here\nOPENAI_MODEL_NAME=gpt-4o\n"
    elif provider == "anthropic":
        content += "ANTHROPIC_API_KEY=your-api-key-here\nANTHROPIC_MODEL_NAME=claude-opus-4-8\n"
    elif provider == "gemini":
        content += "GEMINI_API_KEY=your-api-key-here\nGEMINI_MODEL_NAME=gemini-1.5-pro\n"
    elif provider == "ollama":
        content += "OLLAMA_BASE_URL=http://localhost:11434\nOLLAMA_MODEL_NAME=llama3.1\n"
    try:
        env_file.write_text(content, encoding="utf-8")
    except OSError:
        logger.warning("Could not write .env file at %s", env_file)


def _patch_pyproject_version(project_path: Path) -> None:
    """Replace pre-release crewai pin with stable version range."""
    pyproject = project_path / "pyproject.toml"
    try:
        content = pyproject.read_text(encoding="utf-8")
        content = re.sub(
            r'"crewai\[tools\]==\d+\.\d+\.\d+[a-z]*\d*"',
            '"crewai[tools]>=1.14.0"',
            content,
        )
        pyproject.write_text(content, encoding="utf-8")
        logger.info("Patched pyproject.toml to use stable crewai version")
    except OSError:
        logger.warning("Could not patch pyproject.toml at %s", pyproject)
