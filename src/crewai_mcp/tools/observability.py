"""
MCP Tools — Observability.

Tools for testing, training, evaluating, and replaying CrewAI executions.
"""

from __future__ import annotations

import logging
import subprocess

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import get_project_path, run_crewai_command_async

logger = logging.getLogger("crewai-mcp.tools.observability")


@mcp.tool()
async def crewai_test_crew(
    project_name: str = Field(..., description="Project name"),
    iterations: int = Field(default=2, description="Number of testing iterations", ge=1, le=20),
    model: str = Field(default="openai/gpt-4o", description="LLM to use for evaluation"),
) -> str:
    """
    Test the crew's performance and evaluate outputs.

    Runs `crewai test -n {iterations} -m {model}`.
    This helps in assessing the quality of the crew's execution.
    """
    project_path = get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        code, stdout, stderr = await run_crewai_command_async(
            "test", "-n", str(iterations), "-m", model, cwd=project_path, timeout=600
        )
        return (
            f"Test completed.\n\n"
            f"Exit code: {code}\n\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Crew test timed out after 600 seconds."
    except Exception as e:
        logger.exception("Error testing crew")
        return f"Error: {str(e)}"


@mcp.tool()
async def crewai_train_crew(
    project_name: str = Field(..., description="Project name"),
    iterations: int = Field(default=5, description="Number of training iterations", ge=1, le=50),
    filename: str = Field(default="trained_agents_data.pkl", description="Output file for trained weights"),
) -> str:
    """
    Train the crew to improve performance.

    Runs `crewai train -n {iterations} -f {filename}`.
    Agent training provides human-in-the-loop feedback to optimize prompts.
    """
    project_path = get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        code, stdout, stderr = await run_crewai_command_async(
            "train", "-n", str(iterations), "-f", filename, cwd=project_path, timeout=1200
        )
        return (
            f"Training run finished.\n\n"
            f"Exit code: {code}\n\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Crew training timed out after 1200 seconds."
    except Exception as e:
        logger.exception("Error training crew")
        return f"Error: {str(e)}"


@mcp.tool()
async def crewai_replay_task(
    project_name: str = Field(..., description="Project name"),
    task_id: str = Field(..., description="ID of the task to replay from"),
) -> str:
    """
    Replay a crew execution from a specific task.

    Runs `crewai replay -t {task_id}`.
    Useful for debugging and retrying specific failed tasks.
    """
    project_path = get_project_path(project_name)
    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        code, stdout, stderr = await run_crewai_command_async(
            "replay", "-t", task_id, cwd=project_path, timeout=600
        )
        return (
            f"Replay finished.\n\n"
            f"Exit code: {code}\n\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Task replay timed out after 600 seconds."
    except Exception as e:
        logger.exception("Error replaying task")
        return f"Error: {str(e)}"
