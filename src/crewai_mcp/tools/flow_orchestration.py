"""
MCP Tools — Flow Orchestration.

Tools for visualizing and executing Flows.
"""

from __future__ import annotations

import logging
import subprocess

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import get_project_path

logger = logging.getLogger("crewai-mcp.tools.flow_orchestration")


@mcp.tool()
def crewai_flow_plot(
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
        cmd = ["uv", "run", "crewai", "flow", "plot"]
        logger.info("Running: %s in %s", " ".join(cmd), project_path)

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
            stdin=subprocess.DEVNULL,
        )

        if result.returncode == 0:
            html_files = list(project_path.glob("*.html"))
            files_str = ", ".join(f.name for f in html_files)
            return (
                f"Flow plotted successfully.\n"
                f"Generated files: {files_str}\n\n"
                f"STDOUT:\n{result.stdout}"
            )
        return (
            f"Failed to plot flow.\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Flow plot timed out after 120 seconds."
    except Exception as e:
        logger.exception("Error plotting flow")
        return f"Error: {str(e)}"


@mcp.tool()
def crewai_flow_run(
    project_name: str = Field(..., description="Project name"),
    inputs: dict = Field(default_factory=dict, description="Optional inputs for the flow"),
) -> str:
    """
    Execute a Flow project using the Python API.

    This runs the flow directly using the Python API (flow.kickoff(inputs=...))
    instead of the CLI, ensuring proper tool execution and avoiding interactive prompts.
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        import sys

        src_path = project_path / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        project_module_name = project_name.replace("-", "_")

        try:
            module = __import__(f"{project_module_name}.flow", fromlist=[""])
        except ImportError as e:
            return f"Error importing flow module: {e}. Make sure the project structure is correct."

        # Find the flow class — prefer class ending with Flow or having kickoff()
        flow_class = None
        excluded = {"Flow", "Crew", "Agent", "Task", "Process", "CrewBase", "BaseAgent"}
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and attr_name not in excluded:
                if attr_name.endswith("Flow") or hasattr(attr, "kickoff"):
                    flow_class = attr
                    break

        if flow_class is None:
            return f"Error: Could not find a Flow class in {project_module_name}.flow"

        flow_instance = flow_class()

        if hasattr(flow_instance, "load_configurations"):
            flow_instance.load_configurations()

        logger.info("Running flow '%s' with inputs: %s", project_name, inputs)

        if hasattr(flow_instance, "flow"):
            flow = flow_instance.flow()
            result = flow.kickoff(inputs=inputs)
        elif hasattr(flow_instance, "kickoff"):
            result = flow_instance.kickoff(inputs=inputs)
        else:
            return "Error: Flow class does not have 'kickoff' or 'flow' method"

        return f"Flow execution successful.\n\nResult: {result}"

    except Exception as e:
        logger.exception("Error running flow")
        return f"Error executing flow: {str(e)}"
