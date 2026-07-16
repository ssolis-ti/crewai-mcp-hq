# 🚀 CrewAI MCP Orchestrator

MCP server that turns any LLM into a [CrewAI](https://docs.crewai.com/) orchestrator. **18 tools**, prebuilt crew templates, multi-agent LLM routing, and RAG engine with 266+ indexed docs.

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

## 🧰 Tools (18)

| Domain | Tools |
|---|---|
| **Projects** | `crewai_create_project`, `crewai_install_deps`, `crewai_project_info` |
| **Templates** | `crewai_apply_template` |
| **Agents & Tasks** | `crewai_define_agent`, `crewai_define_task`, `crewai_edit_crew_py`, `crewai_kickoff` |
| **LLM Routing** | `crewai_configure_llm_provider`, `crewai_assign_llms`, `crewai_list_agents` |
| **Flows** | `crewai_flow_plot`, `crewai_flow_run` |
| **Knowledge** | `crewai_query_knowledge`, `crewai_manage_memory` |
| **Observability** | `crewai_test_crew`, `crewai_train_crew`, `crewai_replay_task` |

---

## 🔀 LLM Routing (multi-agent, multi-select)

Connect a provider once, then route models to any subset of agents:

```python
# 1. Connect the project to a provider (writes the .env layout)
crewai_configure_llm_provider("my-team", provider="litellm-proxy",
                              api_base="http://localhost:4000")
# presets: openai · anthropic · gemini · groq · ollama · openrouter · bifrost · litellm-proxy

# Bifrost gateway in Docker? One call — default base http://localhost:8080/v1,
# and the gateway holds the real provider keys (client key can be a dummy):
crewai_configure_llm_provider("my-team", provider="bifrost")

# 2. See agent names and current models
crewai_list_agents("my-team")

# 3. Route — three modes:
crewai_assign_llms("my-team", llm="openai/gpt-4o")                        # ALL agents
crewai_assign_llms("my-team", llm="groq/llama-3.3-70b-versatile",
                   agents=["researcher", "writer"])                       # multi-select
crewai_assign_llms("my-team", assignments={                               # per-agent map
    "prd_architect": "openai/deepseek-ai/deepseek-v4-pro",
    "ai_developer":  "openai/meta/llama-4-maverick-17b-128e-instruct",
    "qa_reviewer":   "openai/meta/llama-3.1-70b-instruct",
})
```

Routing updates `agents.yaml` **and** any hardcoded `llm=` override in `crew.py` (which would otherwise silently win over YAML). API keys are never required in the tool call — placeholders are written to `.env` for the user to fill in.

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

## 🤖 LLM Playbook — step-by-step instructions for the agent using this MCP

> The server ships these instructions in its MCP `instructions` field, so any compliant client injects them into the LLM automatically. This section documents the same contract for humans and for system prompts.

### Golden path (mandatory order)

| # | Step | Tool | Precondition | Postcondition |
|---|---|---|---|---|
| 1 | **Research** *(optional)* | `crewai_query_knowledge(query)` | — | Relevant CrewAI patterns known |
| 2 | **Create** | `crewai_create_project(name, "crew"\|"flow")` | Project must not exist | Scaffold in workspace |
| 3 | **Configure** | `crewai_apply_template` **or** `crewai_define_agent` + `crewai_define_task` | Project exists | `agents.yaml`, `tasks.yaml`, `crew.py` ready |
| 4 | **Connect LLMs** | `crewai_configure_llm_provider(project, provider, api_base=...)`, then `crewai_assign_llms` (see [LLM Routing](#-llm-routing-multi-agent-multi-select)) | Step 3 done | Provider in `.env`, models routed per agent |
| 5 | **Tune** *(optional)* | `crewai_edit_crew_py(project, agent, llm=..., tools=[...])` | Agent method exists in `crew.py` | Per-agent LLM/tools set |
| 6 | **Prepare** | User sets API keys in project `.env`, then `crewai_install_deps(project)` | Step 3 done | Venv ready, deps resolved |
| 7 | **Run** | `crewai_kickoff(project, inputs={...})` | Steps 3+6 done, keys set | Crew output returned |
| 8 | **Debug / improve** | `crewai_replay_task`, `crewai_test_crew`, `crewai_train_crew`, `crewai_manage_memory` | A previous run exists | Iterated quality |

### Decision guide

- **User wants a full team fast** → step 3a: `crewai_apply_template`. List options first: read `crewai://templates/prebuilt/index`.
- **User describes a custom workflow** → step 3b: one `crewai_define_agent` per role, then one `crewai_define_task` per task (`agent=` references the agent name; `context=[...]` chains outputs between tasks).
- **User has a flow (event-driven, stateful)** → `crewai_create_project(name, "flow")`, visualize with `crewai_flow_plot`, execute with `crewai_flow_run`.
- **Unsure how something works in CrewAI** → `crewai_query_knowledge` before guessing; cite the returned `crewai://docs/...` URIs.

### Invariants (do not violate)

1. `create → configure → install → kickoff` — never skip or reorder.
2. `inputs` keys in `kickoff` **must match** the `{placeholders}` in the YAML files — verify with `crewai_project_info` before running.
3. The LLM **cannot** set API keys: ask the user to edit the project's `.env`. A kickoff without keys fails with an auth error — report it, don't retry.
4. `install / kickoff / test / train` take minutes — call once and wait; don't fire duplicates.

### Error recovery

| Symptom | Action |
|---|---|
| `Error: Project '<x>' not found` | Wrong name or not created yet → `crewai_create_project` |
| Kickoff fails with auth/API-key error in STDERR | Ask the user to fill the project `.env`, then retry |
| Kickoff fails mid-run on one task | Fix the config, then `crewai_replay_task(project, task_id)` |
| `Error: Agent method '<x>' not found in crew.py` | List real names with `crewai_project_info`, retry |
| Stale or corrupted agent memory | `crewai_manage_memory(project, "reset")` |

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
├── tools/              ← 18 tools + shared utils.py
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
| [Playbook para el LLM](#-llm-playbook--step-by-step-instructions-for-the-agent-using-this-mcp) | Instrucciones paso a paso que recibe el agente (orden obligatorio, invariantes, recuperación de errores) |
| [CyberOps template](#cyberops--mvp-development-team) | Equipo de 5 agentes para crear MVPs desde cero |
| [Herramientas](#-tools-15) | Referencia completa de las 15 herramientas |
| [Ejemplo: crear un proyecto](#-prebuilt-crew-templates) | `create_project` + `apply_template` en 2 pasos |

---

## 📝 License

MIT
