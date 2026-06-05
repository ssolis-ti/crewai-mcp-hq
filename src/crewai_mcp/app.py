from mcp.server.fastmcp import FastMCP

# ── FastMCP instance ─────────────────────────────────────────────────
mcp = FastMCP(
    name="crewai-orchestrator",
    instructions=(
        "You are connected to the CrewAI Orchestrator MCP Server. "
        "This server gives you full access to CrewAI documentation, "
        "project management tools, agent/crew/task lifecycle management, "
        "flow orchestration, knowledge & memory management, and observability. "
        "Use the resources to read documentation, the tools to create and manage "
        "CrewAI projects, and the prompts for guided workflows."
    ),
)
