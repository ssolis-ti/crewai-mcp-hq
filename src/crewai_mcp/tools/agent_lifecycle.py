"""
MCP Tools — Agent, Task & Crew Lifecycle.

Tools for defining and executing CrewAI components.
"""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Any

from pydantic import Field

from crewai_mcp.config import config
from crewai_mcp.app import mcp

logger = logging.getLogger("crewai-mcp.tools.agent_lifecycle")


def _get_project_path(project_name: str) -> Path:
    safe_name = Path(project_name).name
    return config.paths.workspace / safe_name


@mcp.tool()
def crewai_define_agent(
    project_name: str,
    agent_name: str,
    role: str,
    goal: str,
    backstory: str,
    llm: str = "",
    options: dict[str, Any] = None,
) -> str:
    if options is None:
        options = {}
    """
    Define a new agent in an existing CrewAI project.

    This updates the `agents.yaml` configuration file for the given project.
    Note: You must still manually update the crew.py file to link any tools.
    """
    import yaml

    project_path = _get_project_path(project_name)
    agents_yaml = project_path / "src" / project_name / "config" / "agents.yaml"

    if not agents_yaml.exists():
        return f"Error: {agents_yaml} not found. Is {project_name} a valid CrewAI project?"

    try:
        content = agents_yaml.read_text(encoding="utf-8")
        agents_data = yaml.safe_load(content) or {}
    except Exception as e:
        return f"Error reading agents.yaml: {e}"

    agent_def = {
        "role": role,
        "goal": goal,
        "backstory": backstory,
    }
    if llm:
        agent_def["llm"] = llm

    agent_def.update(options)
    agents_data[agent_name] = agent_def

    try:
        with agents_yaml.open("w", encoding="utf-8") as f:
            yaml.dump(agents_data, f, default_flow_style=False, sort_keys=False)

        return f"Successfully added agent '{agent_name}' to {agents_yaml.name}"
    except Exception as e:
        return f"Error writing agents.yaml: {e}"


@mcp.tool()
def crewai_define_task(
    project_name: str,
    task_name: str,
    description: str,
    expected_output: str,
    agent: str,
    context: list[str] = None,
) -> str:
    if context is None:
        context = []
    """
    Define a new task in an existing CrewAI project.

    This updates the `tasks.yaml` configuration file for the given project.
    """
    import yaml

    project_path = _get_project_path(project_name)
    tasks_yaml = project_path / "src" / project_name / "config" / "tasks.yaml"

    if not tasks_yaml.exists():
        return f"Error: {tasks_yaml} not found."

    try:
        content = tasks_yaml.read_text(encoding="utf-8")
        tasks_data = yaml.safe_load(content) or {}
    except Exception as e:
        return f"Error reading tasks.yaml: {e}"

    task_def = {
        "description": description,
        "expected_output": expected_output,
        "agent": agent,
    }
    if context:
        task_def["context"] = context

    tasks_data[task_name] = task_def

    try:
        with tasks_yaml.open("w", encoding="utf-8") as f:
            yaml.dump(tasks_data, f, default_flow_style=False, sort_keys=False)

        return f"Successfully added task '{task_name}' to {tasks_yaml.name}"
    except Exception as e:
        return f"Error writing tasks.yaml: {e}"


@mcp.tool()
def crewai_kickoff(
    project_name: str,
    inputs: dict[str, Any] = None,
) -> str:
    if inputs is None:
        inputs = {}
    """
    Execute a CrewAI project (`crewai run`) with the provided inputs.

    Note: This runs synchronously. For long-running crews, use CLI directly
    or implement async background execution.
    """
    project_path = _get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        # Write inputs to a temporary JSON file to pass to the CLI
        # (Though crewai CLI doesn't natively accept json file inputs easily without custom script,
        # standard scaffold projects usually read from sys.argv or hardcoded dict.
        # We will attempt `crewai run` directly and pass inputs via env vars or just run it.)

        # Since standard template has `inputs = {'topic': 'AI LLMs'}` hardcoded in main.py,
        # we might need to modify main.py or run it directly.
        # For this tool, we will execute `crewai run` and warn if inputs can't be injected cleanly.

        cmd = ["crewai", "run"]
        logger.info(f"Running: {' '.join(cmd)} in {project_path}")

        # Inject inputs via environment variables as a fallback convention
        import os

        env = os.environ.copy()
        env["CREWAI_INPUTS"] = json.dumps(inputs)

        result = subprocess.run(
            cmd,
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )

        output = f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"

        if result.returncode == 0:
            return f"Crew execution successful.\n\n{output}"
        else:
            return f"Crew execution failed.\n\n{output}"

    except Exception as e:
        logger.exception("Error running crew")
        return f"Error executing crew: {str(e)}"
