"""
MCP Tools — Flow Orchestration.

Tools for visualizing and executing Flows.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from pydantic import Field

from crewai_mcp.config import config
from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.tools.flow_orchestration")


def _get_project_path(project_name: str) -> Path:
    safe_name = Path(project_name).name
    return config.paths.workspace / safe_name


@mcp.tool()
def crewai_flow_plot(
    project_name: str = Field(..., description="Project name"),
) -> str:
    """
    Generate an HTML visualization of a Flow project.

    Runs `crewai flow plot` which outputs an interactive HTML file
    mapping out the flow states and transitions.
    """
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        cmd = ["crewai", "flow", "plot"]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
            stdin=subprocess.DEVNULL,
        )

        if result.returncode == 0:
            # Usually creates a file like flow_plot.html
            html_files = list(project_path.glob("*.html"))
            files_str = ", ".join(f.name for f in html_files)
            return f"Flow plotted successfully.\nGenerated files: {files_str}\n\nSTDOUT:\n{result.stdout}"
        else:
            return f"Failed to plot flow.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

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
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        # Add project src to Python path
        import sys
        src_path = project_path / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # Import the flow module dynamically
        project_module_name = project_name.replace("-", "_")
        
        try:
            module = __import__(f"{project_module_name}.flow", fromlist=[""])
        except ImportError as e:
            return f"Error importing flow module: {e}. Make sure the project structure is correct."

        # Find the flow class
        flow_class = None
        excluded_names = {"Flow", "Crew", "Agent", "Task", "Process", "CrewBase", "BaseAgent"}
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and attr_name not in excluded_names:
                if attr_name.endswith("Flow") or hasattr(attr, "kickoff"):
                    flow_class = attr
                    break
        
        if flow_class is None:
            return f"Error: Could not find a Flow class in {project_module_name}.flow"

        # Instantiate and run the flow
        flow_instance = flow_class()
        
        # Load configurations if available (for CrewBase-style flows)
        if hasattr(flow_instance, "load_configurations"):
            flow_instance.load_configurations()
        
        logger.info(f"Running flow '{project_name}' with inputs: {inputs}")
        
        # Try to get the flow object and kickoff
        if hasattr(flow_instance, "flow"):
            flow = flow_instance.flow()
            result = flow.kickoff(inputs=inputs)
        elif hasattr(flow_instance, "kickoff"):
            result = flow_instance.kickoff(inputs=inputs)
        else:
            return f"Error: Flow class does not have 'kickoff' or 'flow' method"
        
        return f"Flow execution successful.\n\nResult: {result}"

    except Exception as e:
        logger.exception("Error running flow")
        return f"Error executing flow: {str(e)}"
