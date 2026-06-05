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
) -> str:
    """
    Execute a Flow project.

    Runs `crewai run` for a flow project (which resolves to the Flow's kickoff).
    """
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        cmd = ["crewai", "run"]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"

        if result.returncode == 0:
            return f"Flow execution successful.\n\n{output}"
        else:
            return f"Flow execution failed.\n\n{output}"

    except Exception as e:
        logger.exception("Error running flow")
        return f"Error executing flow: {str(e)}"
