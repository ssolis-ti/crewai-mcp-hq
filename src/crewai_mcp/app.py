from mcp.server.fastmcp import FastMCP

from crewai_mcp.config import config

# ── FastMCP instance ─────────────────────────────────────────────────
# host/port must be set here (constructor settings) — FastMCP.run() does
# NOT accept them as kwargs; they only apply to sse / streamable-http.
mcp = FastMCP(
    name="crewai-orchestrator",
    instructions=(
        "You are connected to the CrewAI Orchestrator MCP Server. It lets you "
        "build, run, and debug complete CrewAI multi-agent projects inside a "
        "managed workspace.\n"
        "\n"
        "WORKFLOW — follow these steps in order:\n"
        "1. RESEARCH (optional): call crewai_query_knowledge or read "
        "crewai://docs/index to look up CrewAI patterns before building.\n"
        "2. CREATE: crewai_create_project(name, 'crew'|'flow') scaffolds the "
        "project. Nothing else works until the project exists.\n"
        "3. CONFIGURE — pick one path:\n"
        "   a) Prebuilt team: crewai_apply_template(project, template). List "
        "templates at crewai://templates/prebuilt/index.\n"
        "   b) Custom team: crewai_define_agent(...) for each agent, then "
        "crewai_define_task(...) for each task (tasks reference agents by "
        "name; use context=[...] to chain task outputs).\n"
        "   Fine-tune per-agent LLM/tools afterwards with crewai_edit_crew_py. "
        "Inspect current state anytime with crewai_project_info.\n"
        "4. CONNECT LLMs: crewai_configure_llm_provider(project, provider, "
        "api_base=...) writes the provider credentials layout into the "
        "project .env (openai, anthropic, gemini, groq, ollama, openrouter, "
        "'bifrost', or 'litellm-proxy' for any OpenAI-compatible gateway). "
        "Then route "
        "models with crewai_assign_llms — one agent, a multi-selection "
        "(agents=[...]), all agents (no list), or a per-agent map "
        "(assignments={agent: model}). Discover agent names and current "
        "models first with crewai_list_agents.\n"
        "5. PREPARE: the project's .env needs real LLM API keys (e.g. "
        "OPENAI_API_KEY) — ask the user to set them; you cannot. Then run "
        "crewai_install_deps(project).\n"
        "6. RUN: crewai_kickoff(project, inputs={...}). The inputs keys must "
        "match the {placeholders} used in agents.yaml/tasks.yaml (check them "
        "with crewai_project_info). Flows run with crewai_flow_run and can be "
        "visualized first with crewai_flow_plot.\n"
        "7. DEBUG & IMPROVE: if a run fails, read the returned STDERR, fix "
        "config with the define/edit tools, and resume from the failed task "
        "with crewai_replay_task. Evaluate with crewai_test_crew, improve "
        "prompts with crewai_train_crew, reset state with "
        "crewai_manage_memory.\n"
        "\n"
        "RULES:\n"
        "- Order is mandatory: create -> configure -> install -> kickoff.\n"
        "- kickoff/test/train fail without API keys in the project .env — "
        "surface that to the user instead of retrying.\n"
        "- install/kickoff/test/train are long operations (minutes); call "
        "them once and wait.\n"
        "- Tool errors come back as text starting with 'Error:' — read them, "
        "they state the exact cause and the fix.\n"
        "- Use the prompts (design_crew, design_flow, debug_crew, "
        "create_custom_tool, select_llm) as guided workflows when the user "
        "asks for design help."
    ),
    host=config.server.host,
    port=config.server.port,
)
