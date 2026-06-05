# 🚀 CrewAI MCP Orchestrator

The **CrewAI MCP Orchestrator** is a highly capable Model Context Protocol (MCP) server that transforms any compatible LLM or AI Assistant into a master orchestrator of the [CrewAI](https://docs.crewai.com/) framework. 

This server provides **13 dynamic tools**, integrated RAG documentation search (ChromaDB), and programmatic control over CrewAI projects, enabling LLMs to dynamically generate, edit, test, and execute multi-agent systems.

---

## 🌟 Key Features

1. **Integrated Knowledge Base (RAG)**: Automatically chunks and indexes CrewAI Markdown documentation so the AI can read guides and concepts via `crewai_query_knowledge`.
2. **Project Scaffolding**: Create native CrewAI projects and flows isolated in a `/workspace` directory.
3. **YAML Lifecycle Management**: Define agents, tasks, and flows directly using Python and Pydantic without breaking the CLI structures.
4. **Observability & Debugging**: Automatically run tests, train models, and replay failed tasks.
5. **Multi-Transport Support**: Works locally via `stdio` for IDEs or via `SSE/HTTP` using the included Docker configuration.

---

## 🛠️ Installation & Setup

We recommend using [`uv`](https://github.com/astral-sh/uv) for lightning-fast dependency management.

```bash
# 1. Clone the repository
git clone https://github.com/tu-usuario/cwai-mcp.git
cd cwai-mcp

# 2. Sync and install dependencies (creates isolated .venv)
uv sync

# 3. Add documentation (Optional but recommended)
# Place CrewAI markdown files inside the /docs folder to be automatically indexed.
```

---

## 🔌 IDE & Client Integration (MCP)

To connect your favorite AI IDE or Assistant to this server, you need to configure an MCP connection over `stdio`. Since the server uses `uv` and its own virtual environment, it's highly recommended to point directly to the `.venv` Python executable for speed and clean stdout streams.

### 🌌 Antigravity
Open your `mcp_config.json` (usually located in `.gemini/config/mcp_config.json`) and add:

```json
{
  "mcpServers": {
    "crewai-orchestrator": {
      "command": "C:\\Ruta\\Absoluta\\cwai-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-X", "utf8", "-m", "crewai_mcp.server"],
      "cwd": "C:/Ruta/Absoluta/cwai-mcp",
      "env": {
        "CREWAI_MCP_TRANSPORT": "stdio",
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

### 🤖 Claude Desktop / Claude Code
Open your Claude Desktop config file (Windows: `%APPDATA%\Claude\claude_desktop_config.json`, Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "crewai-orchestrator": {
      "command": "/absolute/path/to/cwai-mcp/.venv/bin/python",
      "args": ["-m", "crewai_mcp.server"],
      "cwd": "/absolute/path/to/cwai-mcp",
      "env": {
        "CREWAI_MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

### 💻 Roo Code / Cline (VS Code)
Open your MCP settings from the extension UI or edit `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "crewai-orchestrator": {
      "command": "C:\\Ruta\\Absoluta\\cwai-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-X", "utf8", "-m", "crewai_mcp.server"],
      "cwd": "C:/Ruta/Absoluta/cwai-mcp",
      "env": {
        "CREWAI_MCP_TRANSPORT": "stdio",
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

### 🐾 OpenClaw / Generic Stdio
For OpenClaw or any other generic MCP client, simply configure a local process executing:
- **Command:** `/absolute/path/to/.venv/bin/python` (or `python.exe` on Windows)
- **Args:** `["-m", "crewai_mcp.server"]`
- **Env:** `CREWAI_MCP_TRANSPORT=stdio`

---

## 🐳 Docker Deployment (SSE)

If you wish to deploy the MCP orchestrator as a standalone microservice (e.g., inside a Docker Triad architecture), it supports Server-Sent Events (SSE).

```bash
# Build and run using Docker Compose
docker-compose up --build -d
```
The server will be available at `http://localhost:8000/sse`.

---

## 🧰 Available Tools

| Domain | Tools |
|---|---|
| **Project Management** | `crewai_create_project`, `crewai_install_deps`, `crewai_project_info` |
| **Agent Lifecycle** | `crewai_define_agent`, `crewai_define_task`, `crewai_kickoff` |
| **Flow Orchestration**| `crewai_flow_plot`, `crewai_flow_run` |
| **Knowledge/Memory** | `crewai_query_knowledge`, `crewai_manage_memory` |
| **Observability** | `crewai_test_crew`, `crewai_train_crew`, `crewai_replay_task` |

## 📝 License
MIT License. Created to supercharge AI-driven multi-agent orchestration.
