"""
MCP Tools — Flow Orchestration.

Tools for visualizing and executing Flows.
"""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Any, Optional

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import (
    get_module_dir,
    get_project_path,
    run_command_async,
    run_crewai_command_async,
)

logger = logging.getLogger("crewai-mcp.tools.flow_orchestration")


@mcp.tool()
async def crewai_flow_plot(
    project_name: str = Field(..., description="Project name"),
) -> str:
    """
    Generate an HTML visualization of a Flow project.

    Runs `crewai flow plot` which outputs an interactive HTML file
    mapping out the flow states and transitions.
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        code, stdout, stderr = await run_crewai_command_async(
            "flow", "plot", cwd=project_path, timeout=120
        )

        if code == 0:
            html_files = list(project_path.glob("*.html"))
            files_str = ", ".join(f.name for f in html_files)
            return (
                f"Flow plotted successfully.\n"
                f"Generated files: {files_str}\n\n"
                f"STDOUT:\n{stdout}"
            )
        return f"Failed to plot flow.\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"

    except subprocess.TimeoutExpired:
        return "Error: Flow plot timed out after 120 seconds."
    except Exception as e:
        logger.exception("Error plotting flow")
        return f"Error: {str(e)}"


# Runner executed inside the project's own environment via `uv run python -c`.
# Finds the Flow subclass defined in the project and kicks it off with the
# JSON inputs passed as argv[1].
_FLOW_RUNNER = """
import json, sys, importlib

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

inputs = json.loads(sys.argv[1])
module_name = sys.argv[2]

from crewai.flow.flow import Flow

mod = None
for candidate in (module_name + ".main", module_name + ".flow", module_name):
    try:
        mod = importlib.import_module(candidate)
    except ImportError:
        continue
    if any(
        isinstance(getattr(mod, n), type)
        and getattr(mod, n).__module__ == mod.__name__
        and issubclass(getattr(mod, n), Flow)
        for n in dir(mod)
    ):
        break
    mod = None

if mod is None:
    print("RUNNER_ERROR: no module with a Flow subclass found", file=sys.stderr)
    sys.exit(2)

flow_cls = None
for name in dir(mod):
    attr = getattr(mod, name)
    if isinstance(attr, type) and attr.__module__ == mod.__name__ and issubclass(attr, Flow):
        flow_cls = attr
        break

result = flow_cls().kickoff(inputs=inputs)
print("=== FLOW RESULT ===")
print(result)
"""


@mcp.tool()
async def crewai_flow_run(
    project_name: str = Field(..., description="Project name"),
    inputs: Optional[dict[str, Any]] = Field(
        default=None, description="Optional inputs for the flow"
    ),
    timeout: int = Field(default=600, description="Max seconds to wait for the flow run", le=3600),
) -> str:
    """
    Execute a Flow project with the provided inputs.

    Runs the flow in a subprocess inside the project's own environment
    (`uv run python`), so the project's dependencies, .env, and Python
    version are used — the MCP server stays isolated and responsive.
    """
    inputs = inputs or {}

    project_path = get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return f"Error: Could not find the source module of '{project_name}'."

    cmd = ["uv", "run", "python", "-c", _FLOW_RUNNER, json.dumps(inputs), module_dir.name]
    logger.info("Running flow '%s' with inputs: %s", project_name, inputs)

    try:
        code, stdout, stderr = await run_command_async(cmd, cwd=project_path, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"Error: Flow execution timed out after {timeout} seconds."
    except Exception as e:
        logger.exception("Error running flow")
        return f"Error executing flow: {e}"

    if code != 0:
        return f"Flow execution failed (exit {code}).\n\nSTDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"

    return f"Flow execution successful.\n\n{stdout}"
