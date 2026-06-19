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
from crewai_mcp.tools.utils import get_project_path

logger = logging.getLogger("crewai-mcp.tools.agent_lifecycle")


@mcp.tool()
def crewai_define_agent(
    project_name: str,
    agent_name: str,
    role: str,
    goal: str,
    backstory: str,
    llm: str = "",
    options: dict[str, Any] = None,
    tools: list[str] = None,
    add_to_crew_py: bool = True,
) -> str:
    if options is None:
        options = {}
    if tools is None:
        tools = []
    """
    Define a new agent in an existing CrewAI project.

    This updates the `agents.yaml` configuration file for the given project.
    Optionally, also adds the agent method to crew.py with the specified tools and LLM.
    """
    import yaml

    project_path = get_project_path(project_name)
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

        result_msg = f"Successfully added agent '{agent_name}' to {agents_yaml.name}"
        
        # Also add to crew.py if requested
        if add_to_crew_py:
            crew_py = project_path / "src" / project_name / "crew.py"
            if crew_py.exists():
                try:
                    crew_content = crew_py.read_text(encoding="utf-8")
                    
                    # Check if agent method already exists
                    import re
                    agent_pattern = rf"@agent\s+def\s+{re.escape(agent_name)}\s*\("
                    if not re.search(agent_pattern, crew_content):
                        # Find the last @agent method to insert after it
                        agent_methods = list(re.finditer(r"@agent\s+def\s+\w+\s*\(self\)\s*->\s*Agent:", crew_content))
                        if agent_methods:
                            last_agent = agent_methods[-1]
                            # Find the end of that method (next @agent, @task, @crew, or end of class)
                            insert_pos = last_agent.end()
                            # Find the end of the method body
                            method_end = crew_content.find("\n\n    @", insert_pos)
                            if method_end == -1:
                                method_end = crew_content.find("\n\n    @crew", insert_pos)
                            if method_end == -1:
                                method_end = crew_content.find("\n\n    @task", insert_pos)
                            if method_end == -1:
                                method_end = len(crew_content)
                            
                            # Build the new agent method
                            tools_str = ""
                            if tools:
                                tools_str = f",\n            tools=[{', '.join(tools)}]"
                            
                            llm_str = ""
                            if llm:
                                llm_str = f',\n            llm="{llm}"'
                            
                            # Check if we need to add imports for the tools
                            imports_to_add = []
                            for tool in tools:
                                if 'SerperDevTool' in tool:
                                    imports_to_add.append("from crewai_tools import SerperDevTool")
                                elif 'WebsiteSearchTool' in tool:
                                    imports_to_add.append("from crewai_tools import WebsiteSearchTool")
                                elif 'FileReadTool' in tool:
                                    imports_to_add.append("from crewai_tools import FileReadTool")
                                elif 'DirectoryReadTool' in tool:
                                    imports_to_add.append("from crewai_tools import DirectoryReadTool")
                                elif 'CSVSearchTool' in tool:
                                    imports_to_add.append("from crewai_tools import CSVSearchTool")
                                elif 'JSONSearchTool' in tool:
                                    imports_to_add.append("from crewai_tools import JSONSearchTool")
                                elif 'CodeDocsSearchTool' in tool:
                                    imports_to_add.append("from crewai_tools import CodeDocsSearchTool")
                                elif 'GithubSearchTool' in tool:
                                    imports_to_add.append("from crewai_tools import GithubSearchTool")
                                elif 'ScrapeWebsiteTool' in tool:
                                    imports_to_add.append("from crewai_tools import ScrapeWebsiteTool")
                            
                            # Add imports to the file if needed
                            if imports_to_add:
                                import_section_end = crew_content.find("\n\n@CrewBase")
                                if import_section_end == -1:
                                    import_section_end = crew_content.find("\n@CrewBase")
                                if import_section_end != -1:
                                    # Find the last import line
                                    last_import = crew_content.rfind("\nfrom ", 0, import_section_end)
                                    if last_import == -1:
                                        last_import = crew_content.rfind("\nimport ", 0, import_section_end)
                                    if last_import != -1:
                                        # Find end of that import line
                                        line_end = crew_content.find("\n", last_import + 1)
                                        if line_end != -1:
                                            import_lines = "\n".join(imports_to_add)
                                            crew_content = crew_content[:line_end + 1] + import_lines + "\n" + crew_content[line_end + 1:]
                                            # Update method_end since we added lines
                                            method_end += len(import_lines) + 1
                            
                            new_method = f'''

    @agent
    def {agent_name}(self) -> Agent:
        return Agent(
            config=self.agents_config['{agent_name}']{tools_str}{llm_str}
        )'''
                            
                            new_content = crew_content[:method_end] + new_method + crew_content[method_end:]
                            crew_py.write_text(new_content, encoding="utf-8")
                            result_msg += f"\nAlso added agent method '{agent_name}' to crew.py"
                        else:
                            result_msg += f"\nWarning: Could not find existing agent methods in crew.py to insert after"
                    else:
                        result_msg += f"\nAgent method '{agent_name}' already exists in crew.py"
                except Exception as e:
                    result_msg += f"\nWarning: Could not update crew.py: {e}"
            else:
                result_msg += f"\nWarning: crew.py not found"
        
        return result_msg
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

    project_path = get_project_path(project_name)
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
    Execute a CrewAI project programmatically with the provided inputs.

    This runs the crew directly using the Python API (crew.kickoff(inputs=...))
    which properly injects inputs into the crew execution. This is the recommended
    way to run crews from the MCP server.
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    try:
        # Add project src to Python path
        import sys
        src_path = project_path / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # Import the crew module dynamically
        # The project structure is: src/{project_name}/crew.py with class {ProjectName}Crew
        project_module_name = project_name.replace("-", "_")
        
        # Try to import the crew class
        try:
            module = __import__(f"{project_module_name}.crew", fromlist=[""])
        except ImportError as e:
            return f"Error importing crew module: {e}. Make sure the project structure is correct."

        # Find the crew class - it's typically named after the project (e.g., TestProject)
        # or ends with Crew/Flow. Exclude imported classes like Crew, Agent, Task, etc.
        crew_class = None
        excluded_names = {"Crew", "Agent", "Task", "Process", "CrewBase", "BaseAgent", "Flow"}
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and attr_name not in excluded_names:
                if attr_name.endswith("Crew") or attr_name.endswith("Flow") or attr_name == project_module_name.title().replace("_", ""):
                    crew_class = attr
                    break
        
        if crew_class is None:
            # Fallback: look for any class with a crew() method (excluding imported classes)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr_name not in excluded_names and hasattr(attr, "crew"):
                    crew_class = attr
                    break
        
        if crew_class is None:
            return f"Error: Could not find a Crew class in {project_module_name}.crew"

        # Instantiate and run the crew
        crew_instance = crew_class()
        
        # Load configurations and map variables (required for CrewBase classes)
        crew_instance.load_configurations()
        crew_instance.map_all_agent_variables()
        crew_instance.map_all_task_variables()
        
        crew = crew_instance.crew()
        
        logger.info(f"Running crew '{project_name}' with inputs: {inputs}")
        
        result = crew.kickoff(inputs=inputs)
        
        return f"Crew execution successful.\n\nResult: {result}"

    except Exception as e:
        logger.exception("Error running crew")
        return f"Error executing crew: {str(e)}"


@mcp.tool()
def crewai_edit_crew_py(
    project_name: str,
    agent_name: str,
    tools: list[str] = None,
    llm: str = None,
    function_calling_llm: str = None,
    other_params: dict[str, Any] = None,
) -> str:
    """
    Edit the crew.py file to add tools, LLM, or other parameters to a specific agent.

    This tool modifies the agent method in crew.py to include custom tools,
    LLM configuration, or other agent parameters that can't be set via YAML alone.

    Args:
        project_name: Name of the project
        agent_name: Name of the agent method to modify (e.g., 'researcher')
        tools: List of tool import strings (e.g., ['SerperDevTool()', 'WebsiteSearchTool()'])
        llm: LLM model string (e.g., 'gpt-4o', 'claude-3-5-sonnet')
        function_calling_llm: Function calling LLM model string
        other_params: Additional parameters to pass to the Agent constructor
    """
    if tools is None:
        tools = []
    if other_params is None:
        other_params = {}

    project_path = get_project_path(project_name)
    crew_py = project_path / "src" / project_name / "crew.py"

    if not crew_py.exists():
        return f"Error: {crew_py} not found. Is {project_name} a valid CrewAI project?"

    try:
        content = crew_py.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading crew.py: {e}"

    # Find the agent method
    import re
    
    # Pattern to find the agent method definition
    agent_pattern = rf"(@agent\s+def\s+{re.escape(agent_name)}\s*\(self\)\s*->\s*Agent:\s*\n\s*return\s+Agent\()"
    match = re.search(agent_pattern, content)
    
    if not match:
        return f"Error: Agent method '{agent_name}' not found in crew.py"

    # Find the Agent() call and its closing parenthesis
    start_pos = match.end() - 1  # Position of the opening parenthesis of Agent(
    
    # Parse the Agent() call to find its end
    paren_count = 0
    end_pos = start_pos
    in_string = False
    string_char = None
    
    for i, char in enumerate(content[start_pos:], start=start_pos):
        if char in ('"', "'") and (i == 0 or content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        elif not in_string:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count == 0:
                    end_pos = i + 1
                    break
    
    if paren_count != 0:
        return f"Error: Could not parse Agent() call for agent '{agent_name}'"

    # Extract the current Agent() call arguments
    agent_call = content[start_pos:end_pos]
    
    # Build new arguments
    new_args = []
    
    # Check if config= is already present
    has_config = "config=" in agent_call
    
    # Add tools if provided
    if tools:
        tools_str = ", ".join(tools)
        new_args.append(f"tools=[{tools_str}]")
    
    # Add llm if provided
    if llm:
        new_args.append(f'llm="{llm}"')
    
    # Add function_calling_llm if provided
    if function_calling_llm:
        new_args.append(f'function_calling_llm="{function_calling_llm}"')
    
    # Add other params
    for key, value in other_params.items():
        if isinstance(value, str):
            new_args.append(f'{key}="{value}"')
        else:
            new_args.append(f"{key}={value}")
    
    if not new_args:
        return "No modifications specified. Provide tools, llm, function_calling_llm, or other_params."

    # Check if we need to add imports for the tools
    imports_to_add = []
    for tool in tools:
        if 'SerperDevTool' in tool:
            imports_to_add.append("from crewai_tools import SerperDevTool")
        elif 'WebsiteSearchTool' in tool:
            imports_to_add.append("from crewai_tools import WebsiteSearchTool")
        elif 'FileReadTool' in tool:
            imports_to_add.append("from crewai_tools import FileReadTool")
        elif 'DirectoryReadTool' in tool:
            imports_to_add.append("from crewai_tools import DirectoryReadTool")
        elif 'CSVSearchTool' in tool:
            imports_to_add.append("from crewai_tools import CSVSearchTool")
        elif 'JSONSearchTool' in tool:
            imports_to_add.append("from crewai_tools import JSONSearchTool")
        elif 'CodeDocsSearchTool' in tool:
            imports_to_add.append("from crewai_tools import CodeDocsSearchTool")
        elif 'GithubSearchTool' in tool:
            imports_to_add.append("from crewai_tools import GithubSearchTool")
        elif 'ScrapeWebsiteTool' in tool:
            imports_to_add.append("from crewai_tools import ScrapeWebsiteTool")
    
    # Add imports to the file if needed
    if imports_to_add:
        # Find the last import line before the class definition
        class_pos = content.find("\n@CrewBase")
        if class_pos == -1:
            class_pos = content.find("\nclass ")
        if class_pos != -1:
            # Find the last import line before the class
            last_import = content.rfind("\nfrom ", 0, class_pos)
            if last_import == -1:
                last_import = content.rfind("\nimport ", 0, class_pos)
            if last_import != -1:
                # Find end of that import line
                line_end = content.find("\n", last_import + 1)
                if line_end != -1:
                    import_lines = "\n".join(imports_to_add)
                    content = content[:line_end + 1] + import_lines + "\n" + content[line_end + 1:]
                    # Update positions since we added lines
                    start_pos += len(import_lines) + 1
                    end_pos += len(import_lines) + 1

    # Insert new arguments into the Agent() call
    # Find the position after "Agent(" or after "config=...,"
    if has_config:
        # Insert after the config argument
        config_match = re.search(r"config\s*=\s*[^,]+,", agent_call)
        if config_match:
            insert_pos = start_pos + config_match.end()
            new_content = content[:insert_pos] + "\n            " + ",\n            ".join(new_args) + "," + content[insert_pos:]
        else:
            # Fallback: insert after Agent(
            insert_pos = start_pos + len("Agent(")
            new_content = content[:insert_pos] + "\n            " + ",\n            ".join(new_args) + "," + content[insert_pos:]
    else:
        # Insert after Agent(
        insert_pos = start_pos + len("Agent(")
        new_content = content[:insert_pos] + "\n            " + ",\n            ".join(new_args) + "," + content[insert_pos:]

    try:
        with crew_py.open("w", encoding="utf-8") as f:
            f.write(new_content)
        
        return f"Successfully updated agent '{agent_name}' in crew.py with: {', '.join(new_args)}"
    except Exception as e:
        return f"Error writing crew.py: {e}"
