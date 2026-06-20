# 🚀 CrewAI MCP Orchestrator

MCP server that turns any LLM into a [CrewAI](https://docs.crewai.com/) orchestrator. **15 tools**, prebuilt crew templates, and RAG engine with 266+ indexed docs.

📖 **Documentation**: [English](https://docs.crewai.com) · [Español](#-documentación-en-español)

---

## ⚡ Install

```bash
git clone https://github.com/ssolis-ti/crewai-mcp-hq.git
cd crewai-mcp-hq
uv sync
```

---

## 🔌 Connect to MCP Clients

### Hermes Agent
```bash
hermes mcp add crewai-orchestrator \
  --command "/path/to/crewai-mcp-hq/.venv/Scripts/python.exe"
  --args "-X utf8 -m crewai_mcp.server"
```

### Claude Desktop / Cursor / Roo Code
```json
{
  "mcpServers": {
    "crewai-orchestrator": {
      "command": "/path/to/crewai-mcp-hq/.venv/bin/python",
      "args": ["-m", "crewai_mcp.server"],
      "cwd": "/path/to/crewai-mcp-hq",
      "env": { "CREWAI_MCP_TRANSPORT": "stdio" }
    }
  }
}
```

### Docker (SSE)
```bash
docker-compose up -d
# Available at http://localhost:8808/sse
```

---

## 🧰 Tools (15)

| Domain | Tools |
|---|---|
| **Projects** | `crewai_create_project`, `crewai_install_deps`, `crewai_project_info` |
| **Templates** | `crewai_apply_template` |
| **Agents & Tasks** | `crewai_define_agent`, `crewai_define_task`, `crewai_edit_crew_py`, `crewai_kickoff` |
| **Flows** | `crewai_flow_plot`, `crewai_flow_run` |
| **Knowledge** | `crewai_query_knowledge`, `crewai_manage_memory` |
| **Observability** | `crewai_test_crew`, `crewai_train_crew`, `crewai_replay_task` |

---

## 🧩 Prebuilt Crew Templates

Deploy a full team in one call — no per-agent setup:

```python
crewai_create_project(name="my-mvp", project_type="crew")
crewai_apply_template(project_name="my-mvp", template_name="cyberops")
# agents.yaml, tasks.yaml, and crew.py ready to run
```

### CyberOps — MVP Development Team

5-agent sequential crew. Input: project description. Output: PRD + architecture + code + docs + QA.

| Agent | Role | Configurable |
|---|---|---|
| PRD_Architect | Requirements & user stories | LLM, tools, max_iter |
| System_Designer | Architecture (ADRs, C4, API) | LLM, tools, max_iter |
| AI_Developer | AI-first code (<100 lines/file) | LLM, tools, max_iter |
| Doc_Engineer | LLM-optimized documentation | LLM, tools, max_iter |
| QA_Reviewer | Quality audit & traceability | LLM, tools, max_iter |

---

## 🗺️ Deployment Workflow (with your AI assistant)

The logical order to deploy a team of agents using the MCP. Just tell your assistant "I need a team for X" and it handles the rest:

```
1. CREATE      crewai_create_project("my-team", "crew")
                ↓
2. TEMPLATE    crewai_apply_template("my-team", "cyberops")
                ↓
3. INSTALL     crewai_install_deps("my-team")
                ↓
4. KICKOFF     crewai_kickoff("my-team", inputs={...})
                ↓
5. ITERATE     crewai_test_crew / crewai_replay_task / crewai_train_crew
```

### Step-by-step with your AI assistant

| Step | What you say | Tool called |
|---|---|---|
| **Research** | *"I need a team to build [project]"* | `crewai_query_knowledge` — assistant researches CrewAI docs |
| **Scaffold** | *"Create the project"* | `crewai_create_project` — directory + pyproject.toml |
| **Template** | *"Apply CyberOps template"* | `crewai_apply_template` — agents + tasks + crew.py |
| **Customize** | *"Change AI_Developer to use gpt-4"* | `crewai_edit_crew_py` — per-agent LLM/tools config |
| **Install** | *"Install dependencies"* | `crewai_install_deps` — pip/uv sync |
| **Run** | *"Execute the crew"* | `crewai_kickoff` — agents work sequentially |
| **Debug** | *"QA agent failed — retry it"* | `crewai_replay_task` — resumes from failed task |
| **Improve** | *"Test and train"* | `crewai_test_crew` / `crewai_train_crew` |

### Building a custom team from scratch

No prebuilt template? Define agents and tasks one by one:

```
1. CREATE     crewai_create_project("my-custom", "crew")
2. AGENTS     crewai_define_agent("my-custom", "researcher", role="...")
              crewai_define_agent("my-custom", "writer", role="...")
3. TASKS      crewai_define_task("my-custom", "research", agent="researcher")
              crewai_define_task("my-custom", "write", agent="writer")
4. INSTALL    crewai_install_deps("my-custom")
5. KICKOFF    crewai_kickoff("my-custom", inputs={...})
```

---

## 📚 Documentation Resources

| URI | Content |
|---|---|
| `crewai://docs/index` | 266+ docs across 31 categories |
| `crewai://docs/concepts/agents` | Specific documentation pages |
| `crewai://docs/search/{query}` | Keyword search |
| `crewai://templates/index` | Agent, crew & flow templates |
| `crewai://templates/prebuilt/index` | Full crew templates (CyberOps + extensible) |

---

## 🛡️ Robustness

- **Auto-patch versions**: `crewai create` outputs pre-release pins → auto-patched to `>=1.14.0`
- **Name normalization**: hyphens/underscores handled transparently
- **Timeouts on all subprocess calls**: 120s–1200s depending on operation
- **Standardized CLI**: always `uv run crewai`, no PATH dependency

---

## 📁 Structure

```
src/crewai_mcp/
├── server.py           ← Entry point (stdio/sse/streamable-http)
├── resources/          ← Docs, templates, prebuilt crews
├── tools/              ← 15 tools + shared utils.py
├── prompts/            ← Guided workflows (design_crew, debug_crew)
└── knowledge/          ← ChromaDB indexer + retriever
```

---

## 📖 Documentación en Español

La documentación de CrewAI está disponible en inglés en [docs.crewai.com](https://docs.crewai.com). Para usar el MCP en español:

- El motor RAG indexa docs en inglés pero responde preguntas en cualquier idioma
- Los templates de crews aceptan descripciones de proyecto en español
- Las herramientas retornan mensajes en inglés; el LLM que consume el MCP traduce al contexto del usuario

Guías rápidas en español:

| Guía | Descripción |
|---|---|
| [Instalación y setup](#-install) | Clonar, instalar dependencias, conectar a tu IDE |
| [CyberOps template](#cyberops--mvp-development-team) | Equipo de 5 agentes para crear MVPs desde cero |
| [Herramientas](#-tools-15) | Referencia completa de las 15 herramientas |
| [Ejemplo: crear un proyecto](#-prebuilt-crew-templates) | `create_project` + `apply_template` en 2 pasos |

---

## 📝 License

MIT
