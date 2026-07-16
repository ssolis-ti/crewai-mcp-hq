"""
MCP Tools — Agent, Task & Crew Lifecycle.

Tools for defining and executing CrewAI components.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
from typing import Any, Optional

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import (
    get_module_dir,
    get_project_path,
    insert_import,
    run_command_async,
    tool_import_line,
)

logger = logging.getLogger("crewai-mcp.tools.agent_lifecycle")


@mcp.tool()
def crewai_define_agent(
    project_name: str = Field(..., description="Name of the project in the workspace"),
    agent_name: str = Field(..., description="Snake_case identifier for the agent (YAML key and method name)"),
    role: str = Field(..., description="Agent role (job title)"),
    goal: str = Field(..., description="Agent goal (measurable objective)"),
    backstory: str = Field(..., description="Agent backstory (context and expertise)"),
    llm: str = Field(default="", description="Optional LLM model string (e.g., 'openai/gpt-4o')"),
    options: Optional[dict[str, Any]] = Field(
        default=None, description="Extra YAML options (e.g., {'verbose': true, 'max_iter': 25})"
    ),
    tools: Optional[list[str]] = Field(
        default=None, description="Tool constructor expressions for crew.py (e.g., ['SerperDevTool()'])"
    ),
    add_to_crew_py: bool = Field(default=True, description="Also add the @agent method to crew.py"),
) -> str:
    """
    Define a new agent in an existing CrewAI project.

    Updates the `agents.yaml` configuration file for the given project.
    Optionally also adds the @agent method to crew.py with the specified
    tools and LLM (including the required crewai_tools imports).
    """
    import yaml

    options = options or {}
    tools = tools or []

    project_path = get_project_path(project_name)
    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return f"Error: Could not find the source module of '{project_name}'. Is it a valid CrewAI project?"

    agents_yaml = module_dir / "config" / "agents.yaml"
    if not agents_yaml.exists():
        return f"Error: {agents_yaml} not found. Is {project_name} a valid CrewAI project?"

    try:
        agents_data = yaml.safe_load(agents_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return f"Error reading agents.yaml: {e}"

    agent_def: dict[str, Any] = {"role": role, "goal": goal, "backstory": backstory}
    if llm:
        agent_def["llm"] = llm
    agent_def.update(options)
    agents_data[agent_name] = agent_def

    try:
        with agents_yaml.open("w", encoding="utf-8") as f:
            yaml.dump(agents_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    except Exception as e:
        return f"Error writing agents.yaml: {e}"

    result_msg = f"Successfully added agent '{agent_name}' to {agents_yaml.name}"

    if add_to_crew_py:
        crew_py = module_dir / "crew.py"
        if crew_py.exists():
            try:
                result_msg += "\n" + _add_agent_method(crew_py, agent_name, tools, llm)
            except Exception as e:
                result_msg += f"\nWarning: Could not update crew.py: {e}"
        else:
            result_msg += "\nWarning: crew.py not found"

    return result_msg


def _add_agent_method(crew_py, agent_name: str, tools: list[str], llm: str) -> str:
    """Insert a new @agent method into crew.py, before the first @task/@crew method."""
    content = crew_py.read_text(encoding="utf-8")

    if re.search(rf"@agent\s+def\s+{re.escape(agent_name)}\s*\(", content):
        return f"Agent method '{agent_name}' already exists in crew.py"

    # Add crewai_tools imports if needed
    import_line = tool_import_line(tools)
    if import_line:
        content = insert_import(content, import_line)

    tools_str = f",\n            tools=[{', '.join(tools)}]" if tools else ""
    llm_str = f',\n            llm="{llm}"' if llm else ""

    new_method = f'''
    @agent
    def {agent_name}(self) -> Agent:
        return Agent(
            config=self.agents_config['{agent_name}']{tools_str}{llm_str}
        )
'''

    # Insert before the first @task or @crew decorator; else append at EOF
    marker = re.search(r"\n(?=[ \t]+@(?:task|crew)\b)", content)
    if marker:
        pos = marker.start()
        new_content = content[:pos] + "\n" + new_method + content[pos:]
    else:
        new_content = content.rstrip() + "\n" + new_method

    crew_py.write_text(new_content, encoding="utf-8")
    return f"Also added agent method '{agent_name}' to crew.py"


@mcp.tool()
def crewai_define_task(
    project_name: str = Field(..., description="Name of the project in the workspace"),
    task_name: str = Field(..., description="Snake_case identifier for the task"),
    description: str = Field(..., description="What the task should accomplish"),
    expected_output: str = Field(..., description="Expected output format and content"),
    agent: str = Field(..., description="Name of the agent responsible for this task"),
    context: Optional[list[str]] = Field(
        default=None, description="Names of tasks whose output feeds this task"
    ),
) -> str:
    """
    Define a new task in an existing CrewAI project.

    Updates the `tasks.yaml` configuration file for the given project.
    """
    import yaml

    context = context or []

    project_path = get_project_path(project_name)
    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return f"Error: Could not find the source module of '{project_name}'. Is it a valid CrewAI project?"

    tasks_yaml = module_dir / "config" / "tasks.yaml"
    if not tasks_yaml.exists():
        return f"Error: {tasks_yaml} not found."

    try:
        tasks_data = yaml.safe_load(tasks_yaml.read_text(encoding="utf-8")) or {}
    except Exception as e:
        return f"Error reading tasks.yaml: {e}"

    task_def: dict[str, Any] = {
        "description": description,
        "expected_output": expected_output,
        "agent": agent,
    }
    if context:
        task_def["context"] = context

    tasks_data[task_name] = task_def

    try:
        with tasks_yaml.open("w", encoding="utf-8") as f:
            yaml.dump(tasks_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return f"Successfully added task '{task_name}' to {tasks_yaml.name}"
    except Exception as e:
        return f"Error writing tasks.yaml: {e}"


# Runner executed inside the project's own environment via `uv run python -c`.
# Finds the @CrewBase class defined in <module>.crew and kicks it off with
# the JSON inputs passed as argv[1].
_CREW_RUNNER = """
import json, sys, importlib

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

inputs = json.loads(sys.argv[1])
module_name = sys.argv[2]

mod = importlib.import_module(module_name + ".crew")

crew_cls = None
for name in dir(mod):
    attr = getattr(mod, name)
    if isinstance(attr, type) and attr.__module__ == mod.__name__ and hasattr(attr, "crew"):
        crew_cls = attr
        break

if crew_cls is None:
    print("RUNNER_ERROR: no crew class found in " + mod.__name__, file=sys.stderr)
    sys.exit(2)

result = crew_cls().crew().kickoff(inputs=inputs)
print("=== CREW RESULT ===")
print(result.raw if hasattr(result, "raw") else result)
"""


@mcp.tool()
async def crewai_kickoff(
    project_name: str = Field(..., description="Name of the project in the workspace"),
    inputs: Optional[dict[str, Any]] = Field(
        default=None, description="Input variables injected into the crew (e.g., {'topic': 'AI'})"
    ),
    timeout: int = Field(default=600, description="Max seconds to wait for the crew run", le=3600),
) -> str:
    """
    Execute a CrewAI project with the provided inputs.

    Runs the crew in a subprocess inside the project's own environment
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
    if not (module_dir / "crew.py").exists():
        return f"Error: {module_dir / 'crew.py'} not found. Is this a crew project?"

    cmd = ["uv", "run", "python", "-c", _CREW_RUNNER, json.dumps(inputs), module_dir.name]
    logger.info("Kicking off crew '%s' with inputs: %s", project_name, inputs)

    try:
        code, stdout, stderr = await run_command_async(cmd, cwd=project_path, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"Error: Crew execution timed out after {timeout} seconds."
    except Exception as e:
        logger.exception("Error running crew")
        return f"Error executing crew: {e}"

    if code != 0:
        return f"Crew execution failed (exit {code}).\n\nSTDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"

    return f"Crew execution successful.\n\n{stdout}"


@mcp.tool()
def crewai_edit_crew_py(
    project_name: str = Field(..., description="Name of the project in the workspace"),
    agent_name: str = Field(..., description="Name of the agent method to modify (e.g., 'researcher')"),
    tools: Optional[list[str]] = Field(
        default=None, description="Tool constructor expressions (e.g., ['SerperDevTool()'])"
    ),
    llm: Optional[str] = Field(default=None, description="LLM model string (e.g., 'openai/gpt-4o')"),
    function_calling_llm: Optional[str] = Field(default=None, description="Function-calling LLM model string"),
    other_params: Optional[dict[str, Any]] = Field(
        default=None, description="Additional Agent constructor parameters"
    ),
) -> str:
    """
    Edit crew.py to add tools, LLM, or other parameters to a specific agent.

    Modifies the agent method in crew.py to include custom tools, LLM
    configuration, or other Agent parameters that can't be set via YAML alone.
    Automatically adds the required crewai_tools imports.
    """
    tools = tools or []
    other_params = other_params or {}

    project_path = get_project_path(project_name)
    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return f"Error: Could not find the source module of '{project_name}'."

    crew_py = module_dir / "crew.py"
    if not crew_py.exists():
        return f"Error: {crew_py} not found. Is {project_name} a valid CrewAI project?"

    try:
        content = crew_py.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading crew.py: {e}"

    # Build new arguments
    new_args: list[str] = []
    if tools:
        new_args.append(f"tools=[{', '.join(tools)}]")
    if llm:
        new_args.append(f'llm="{llm}"')
    if function_calling_llm:
        new_args.append(f'function_calling_llm="{function_calling_llm}"')
    for key, value in other_params.items():
        new_args.append(f'{key}="{value}"' if isinstance(value, str) else f"{key}={value}")

    if not new_args:
        return "No modifications specified. Provide tools, llm, function_calling_llm, or other_params."

    # Find the agent method's Agent( call
    agent_pattern = rf"(@agent\s+def\s+{re.escape(agent_name)}\s*\(self\)\s*->\s*Agent:\s*\n\s*return\s+Agent\()"
    match = re.search(agent_pattern, content)
    if not match:
        return f"Error: Agent method '{agent_name}' not found in crew.py"

    # Add crewai_tools imports if needed (before locating positions, then re-find)
    import_line = tool_import_line(tools)
    if import_line and import_line not in content:
        content = insert_import(content, import_line)
        match = re.search(agent_pattern, content)

    start_pos = match.end() - 1  # position of the opening '(' of Agent(

    # Balance parentheses to find the end of the Agent(...) call
    paren_count = 0
    end_pos = start_pos
    in_string = False
    string_char = None
    for i in range(start_pos, len(content)):
        char = content[i]
        if char in ('"', "'") and content[i - 1] != "\\":
            if not in_string:
                in_string, string_char = True, char
            elif char == string_char:
                in_string, string_char = False, None
        elif not in_string:
            if char == "(":
                paren_count += 1
            elif char == ")":
                paren_count -= 1
                if paren_count == 0:
                    end_pos = i + 1
                    break

    if paren_count != 0:
        return f"Error: Could not parse Agent() call for agent '{agent_name}'"

    agent_call = content[start_pos:end_pos]
    args_block = "\n            " + ",\n            ".join(new_args) + ","

    # Insert after config=... if present, else right after Agent(
    config_match = re.search(r"config\s*=\s*[^,)]+,", agent_call)
    if config_match:
        insert_pos = start_pos + config_match.end()
    else:
        insert_pos = start_pos + 1

    new_content = content[:insert_pos] + args_block + content[insert_pos:]

    try:
        crew_py.write_text(new_content, encoding="utf-8")
        return f"Successfully updated agent '{agent_name}' in crew.py with: {', '.join(new_args)}"
    except Exception as e:
        return f"Error writing crew.py: {e}"
