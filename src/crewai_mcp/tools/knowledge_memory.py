"""
MCP Tools — Knowledge & Memory.

Tools for querying the CrewAI documentation RAG engine and configuring project memory.
"""

from __future__ import annotations

import json
import logging
import subprocess
from typing import Optional

from pydantic import Field

from crewai_mcp.knowledge.retriever import get_retriever
from crewai_mcp.app import mcp
from crewai_mcp.tools.utils import get_project_path

logger = logging.getLogger("crewai-mcp.tools.knowledge_memory")


@mcp.tool()
def crewai_query_knowledge(
    query: str,
    limit: int = 5,
    category: Optional[str] = None,
) -> str:
    """
    Query the internal CrewAI documentation RAG engine.

    Use this when you need to look up how to use a specific CrewAI feature,
    tool, or pattern. It searches the official documentation and returns
    relevant snippets with their source URIs.
    """
    retriever = get_retriever()
    results = retriever.search(query=query, limit=limit, category_filter=category)

    if not results:
        return f"No documentation found answering: '{query}'"

    lines = [f"# Documentation Search Results: '{query}'\n"]

    for i, r in enumerate(results, 1):
        uri = f"crewai://docs/{r.category}/{r.topic}"
        lines.append(f"## {i}. {r.section} (Score: {r.score:.2f})")
        lines.append(f"Source: [{uri}]({uri})")
        lines.append(f"\n{r.content}\n")
        lines.append("-" * 40 + "\n")

    return "\n".join(lines)


@mcp.tool()
def crewai_manage_memory(
    project_name: str = Field(..., description="Project name"),
    action: str = Field(..., description="Action: 'reset' or 'status'"),
) -> str:
    """
    Manage CrewAI memory for a specific project.

    Use 'reset' to run `crewai reset-memories` (requires --all flag or specific options).
    Use 'status' to check if the project has memory enabled.
    """
    project_path = get_project_path(project_name)

    if not project_path.exists():
        return f"Error: Project '{project_name}' not found."

    if action == "reset":
        try:
            cmd = ["uv", "run", "crewai", "reset-memories", "--all"]
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
                return f"Memories reset successfully.\n{result.stdout}"
            return (
                f"Failed to reset memories.\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        except subprocess.TimeoutExpired:
            return "Error: Memory reset timed out after 120 seconds."
        except Exception as e:
            return f"Error: {str(e)}"

    if action == "status":
        crew_file = project_path / "src" / project_name / "crew.py"
        if not crew_file.exists():
            return "Cannot find crew.py to check memory status."

        content = crew_file.read_text(errors="replace")
        has_memory = "memory=True" in content.replace(" ", "")

        return json.dumps(
            {
                "project": project_name,
                "memory_enabled_in_code": has_memory,
                "db_paths": [str(p) for p in project_path.rglob("*.db")],
            },
            indent=2,
        )

    return f"Unknown action: {action}"
