"""
MCP Prompts — Guided Workflows.

Pre-defined prompts that guide the AI agent through complex CrewAI tasks,
providing standard operating procedures and best practices.
"""

from __future__ import annotations

from mcp.types import PromptMessage

from crewai_mcp.app import mcp


@mcp.prompt("design_crew")
def design_crew(use_case: str, complexity: str = "medium") -> list[PromptMessage]:
    """
    Step-by-step guide to designing a full CrewAI project.
    """
    return [
        PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"I want to design a CrewAI project for the following use case: '{use_case}'. "
                f"The desired complexity is {complexity}.\n\n"
                "Please guide me through the design process using this structure:\n"
                "1. **Architecture & Process**: Suggest the process type (sequential, hierarchical, etc.).\n"
                "2. **Agent Roster**: List the necessary agents, their roles, goals, and backstories.\n"
                "3. **Task List**: Detail the specific tasks, expected outputs, and agent assignments.\n"
                "4. **Tools Needed**: Recommend standard or custom tools needed for the tasks.\n"
                "5. **State/Memory Requirements**: Do we need flows for state management, or standard crew memory?\n\n"
                "Before answering, use the `crewai_query_knowledge` tool to review "
                "best practices for this use case if needed.",
            },
        )
    ]


@mcp.prompt("design_flow")
def design_flow(workflow_description: str, needs_human_review: str = "false") -> list[PromptMessage]:
    """
    Design a state-managed Flow for event-driven orchestration.
    """
    return [
        PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"Help me design a CrewAI Flow based on this description: '{workflow_description}'.\n"
                f"Needs human-in-the-loop review: {needs_human_review}.\n\n"
                "Please output:\n"
                "1. **State Schema**: A Pydantic BaseModel defining the state.\n"
                "2. **Flow Diagram**: A logical explanation of the `@start`, `@listen`, and `@router` connections.\n"
                "3. **Code Skeleton**: The Python implementation using crewai.flow.\n\n"
                "If you need an example, use the `read_doc` resource to read the flow template.",
            },
        )
    ]


@mcp.prompt("debug_crew")
def debug_crew(error_message: str, project_name: str) -> list[PromptMessage]:
    """
    Diagnose issues in a CrewAI project.
    """
    return [
        PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"I'm encountering the following error in my CrewAI project '{project_name}':\n\n"
                f"```\n{error_message}\n```\n\n"
                "Please help me debug this:\n"
                "1. Use `crewai_project_info` to understand my project structure.\n"
                "2. Use `crewai_query_knowledge` to search for known issues related to this error.\n"
                "3. Provide a step-by-step fix, and use the agent/task definition tools to apply it if necessary.",
            },
        )
    ]


@mcp.prompt("create_custom_tool")
def create_custom_tool(tool_purpose: str, needs_async: str = "false") -> list[PromptMessage]:
    """
    Guide for creating a custom CrewAI tool.
    """
    return [
        PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"I need to build a custom CrewAI tool that does the following: '{tool_purpose}'.\n"
                f"Needs async support: {needs_async}.\n\n"
                "Please do the following:\n"
                "1. Read the custom tool template from the MCP resources (`crewai://templates/tool/custom`).\n"
                "2. Decide whether to use the `@tool` decorator or subclass `BaseTool`.\n"
                "3. Write the exact Python code for the tool, including standard pydantic input schemas.\n"
                "4. Explain how to import and assign this tool to an agent.",
            },
        )
    ]


@mcp.prompt("select_llm")
def select_llm(use_case: str, requirements: str = "fast and cheap") -> list[PromptMessage]:
    """
    Recommend the appropriate LLM provider and configuration for a crew.
    """
    return [
        PromptMessage(
            role="user",
            content={
                "type": "text",
                "text": f"I am building a crew for: '{use_case}'.\n"
                f"My key requirements are: {requirements}.\n\n"
                "Based on CrewAI's documentation for LLM connections:\n"
                "1. Suggest the top 2 LLM providers and specific models.\n"
                "2. Provide the exact environment variables I need to set.\n"
                "3. Show me how to configure the `llm` attribute in the agent's definition or yaml config.",
            },
        )
    ]
