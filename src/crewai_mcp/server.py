"""
CrewAI MCP Server — Main entry point.

Registers all Resources, Tools, and Prompts, then starts the FastMCP
server on the configured transport (stdio | sse | streamable-http).
"""

from __future__ import annotations

import logging
import sys

from crewai_mcp.app import mcp

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("crewai-mcp")

def _register_all():
    logger.info("Registering MCP Resources and Tools...")
    import crewai_mcp.resources.documentation  # noqa
    import crewai_mcp.resources.templates  # noqa
    import crewai_mcp.tools.agent_lifecycle  # noqa
    import crewai_mcp.tools.flow_orchestration  # noqa
    import crewai_mcp.tools.knowledge_memory  # noqa
    import crewai_mcp.tools.observability  # noqa
    import crewai_mcp.tools.project_management  # noqa
    import crewai_mcp.prompts.workflows  # noqa
    logger.info("All resources, tools, and prompts registered.")

if __name__ == "__main__":
    _register_all()
    from crewai_mcp.config import config
    
    transport = config.server.transport
    logger.info(f"Starting CrewAI MCP Server on transport: {transport}")
    logger.info(f"Docs path: {config.paths.docs_path}")
    logger.info(f"Workspace: {config.paths.workspace}")

    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        mcp.run(
            transport="sse",
            host=config.server.host,
            port=config.server.port,
        )
    elif transport in ("streamable-http", "http"):
        mcp.run(
            transport="streamable-http",
            host=config.server.host,
            port=config.server.port,
        )
    else:
        logger.error(f"Unknown transport: {transport}. Falling back to stdio.")
        mcp.run(transport="stdio")

