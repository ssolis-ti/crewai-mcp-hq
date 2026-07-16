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

def _preload_native_libs():
    """Import heavy C-extension dependencies on the main thread.

    The knowledge retriever lazily imports chromadb → numpy/onnxruntime on
    first search, which runs inside an anyio worker thread. On Windows,
    loading those extension DLLs from a non-main thread while the process
    runs as a stdio subprocess deadlocks the DLL loader — so we pay the
    import cost once here, before the event loop starts.
    """
    import importlib

    for lib in ("numpy", "onnxruntime", "tokenizers", "chromadb"):
        try:
            importlib.import_module(lib)
        except ImportError:
            logger.warning(f"Optional native lib not available: {lib}")


def _register_all():
    logger.info("Registering MCP Resources and Tools...")
    import crewai_mcp.resources.documentation  # noqa
    import crewai_mcp.resources.templates  # noqa
    import crewai_mcp.resources.crew_templates  # noqa
    import crewai_mcp.tools.agent_lifecycle  # noqa
    import crewai_mcp.tools.flow_orchestration  # noqa
    import crewai_mcp.tools.knowledge_memory  # noqa
    import crewai_mcp.tools.llm_config  # noqa
    import crewai_mcp.tools.observability  # noqa
    import crewai_mcp.tools.project_management  # noqa
    import crewai_mcp.tools.crew_templates  # noqa
    import crewai_mcp.prompts.workflows  # noqa
    logger.info("All resources, tools, and prompts registered.")

def main():
    _preload_native_libs()
    _register_all()
    from crewai_mcp.config import config

    transport = config.server.transport
    logger.info(f"Starting CrewAI MCP Server on transport: {transport}")
    logger.info(f"Docs path: {config.paths.docs_path}")
    logger.info(f"Workspace: {config.paths.workspace}")

    # host/port are configured on the FastMCP instance (see app.py);
    # run() only accepts the transport name.
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        logger.info(f"Listening on {config.server.host}:{config.server.port} (sse)")
        mcp.run(transport="sse")
    elif transport in ("streamable-http", "http"):
        logger.info(f"Listening on {config.server.host}:{config.server.port} (streamable-http)")
        mcp.run(transport="streamable-http")
    else:
        logger.error(f"Unknown transport: {transport}. Falling back to stdio.")
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

