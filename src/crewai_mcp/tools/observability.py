"""
MCP Tools — Observability.

Tools for testing, training, evaluating, and replaying CrewAI executions.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from pydantic import Field

from crewai_mcp.config import config
from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.tools.observability")


def _get_project_path(project_name: str) -> Path:
    safe_name = Path(project_name).name
    return config.paths.workspace / safe_name


@mcp.tool()
def crewai_test_crew(
    project_name: str = Field(..., description="Project name"),
    iterations: int = Field(default=2, description="Number of testing iterations"),
    model: str = Field(default="openai/gpt-4o", description="LLM to use for evaluation"),
) -> str:
    """
    Test the crew's performance and evaluate outputs.

    Runs `crewai test -n {iterations} -m {model}`.
    This helps in assessing the quality of the crew's execution.
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        cmd = ["crewai", "test", "-n", str(iterations), "-m", model]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return f"Test completed.\n\n{output}"

    except Exception as e:
        logger.exception("Error testing crew")
        return f"Error: {str(e)}"


@mcp.tool()
def crewai_train_crew(
    project_name: str = Field(..., description="Project name"),
    iterations: int = Field(default=5, description="Number of training iterations"),
    filename: str = Field(default="trained_agents_data.pkl", description="Output file for trained weights"),
) -> str:
    """
    Train the crew to improve performance.

    Runs `crewai train -n {iterations} -f {filename}`.
    Agent training provides human-in-the-loop feedback to optimize prompts.
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        cmd = ["crewai", "train", "-n", str(iterations), "-f", filename]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return f"Training run finished.\n\n{output}"

    except Exception as e:
        logger.exception("Error training crew")
        return f"Error: {str(e)}"


@mcp.tool()
def crewai_replay_task(
    project_name: str = Field(..., description="Project name"),
    task_id: str = Field(..., description="ID of the task to replay from"),
) -> str:
    """
    Replay a crew execution from a specific task.

    Runs `crewai replay -t {task_id}`.
    Useful for debugging and retrying specific failed tasks.
    """
    project_path = _get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        cmd = ["crewai", "replay", "-t", task_id]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return f"Replay finished.\n\n{output}"

    except Exception as e:
        logger.exception("Error replaying task")
        return f"Error: {str(e)}"
