"""
MCP Tool — Apply Prebuilt Crew Templates.

Apply a saved crew configuration (agents, tasks, crew.py) to an existing project.
"""

from __future__ import annotations

import logging

from pydantic import Field

from crewai_mcp.app import mcp
from crewai_mcp.resources.crew_templates import get_prebuilt_crew, list_prebuilt_crew_names
from crewai_mcp.tools.utils import get_module_dir, get_project_path

logger = logging.getLogger("crewai-mcp.tools.crew_templates")

_AVAILABLE = ", ".join(list_prebuilt_crew_names())


@mcp.tool(
    description=(
        "Apply a prebuilt crew template to an existing project. "
        "This writes agents.yaml, tasks.yaml, and crew.py based on the saved "
        "template configuration. The project must already exist (created with "
        f"crewai_create_project). Available templates: {_AVAILABLE}. "
        "Browse them via the resource crewai://templates/prebuilt/index."
    )
)
def crewai_apply_template(
    project_name: str = Field(..., description="Target project name"),
    template_name: str = Field(..., description=f"Template name. Available: {_AVAILABLE}"),
    class_name: str = Field(
        default="",
        description="Python class name for crew.py. Defaults to project_name in PascalCase.",
    ),
    description: str = Field(
        default="",
        description="Docstring for the crew class. Defaults to template description.",
    ),
) -> str:
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found. Create it first with crewai_create_project."

    crew = get_prebuilt_crew(template_name)
    if crew is None:
        return f"Unknown template '{template_name}'. Available: {_AVAILABLE}"

    module_dir = get_module_dir(project_path)
    if module_dir is None:
        return f"Error: Could not find the source module of '{project_name}'. Is it a valid CrewAI project?"

    # Resolve class name
    if not class_name:
        class_name = project_name.replace("-", " ").replace("_", " ").title().replace(" ", "")

    # Resolve description
    if not description:
        description = crew.get("name", f"{project_name} crew")

    config_dir = module_dir / "config"
    crew_py_path = module_dir / "crew.py"

    config_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Write agents.yaml
        agents_path = config_dir / "agents.yaml"
        agents_path.write_text(crew["agents_yaml"], encoding="utf-8")
        logger.info("Wrote agents.yaml (%d chars)", len(crew["agents_yaml"]))

        # 2. Write tasks.yaml
        tasks_path = config_dir / "tasks.yaml"
        tasks_path.write_text(crew["tasks_yaml"], encoding="utf-8")
        logger.info("Wrote tasks.yaml (%d chars)", len(crew["tasks_yaml"]))

        # 3. Write crew.py — interpolate placeholders with .replace() so that
        # literal braces in the template code never break (unlike .format())
        crew_py_content = (
            crew["crew_py"]
            .replace("{class_name}", class_name)
            .replace("{description}", description)
        )
        crew_py_path.write_text(crew_py_content, encoding="utf-8")
        logger.info("Wrote crew.py (class: %s)", class_name)

    except Exception as e:
        logger.exception("Error writing template files")
        return f"Error applying template: {str(e)}"

    return (
        f"✅ Template '{template_name}' applied to project '{project_name}'.\n\n"
        f"Files written:\n"
        f"  - {agents_path}\n"
        f"  - {tasks_path}\n"
        f"  - {crew_py_path}\n\n"
        f"Crew class: {class_name}\n"
        f"Next: run crewai_install_deps('{project_name}') to set up the environment."
    )
